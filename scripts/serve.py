# -*- coding: utf-8 -*-
"""完全脱离地启动本地服务（关键：子进程不继承父进程的任何管道）。

为什么需要这个脚本（两次真实故障换来的）：
    1) 先用「临时后台任务」起服务 → 任务结束就被回收 → 用户"打不开网页"。
    2) 改用 PowerShell 的 `Start-Process` → 子进程仍继承启动命令的输出句柄，
       命令一超时被强杀，子进程跟着一起死。

    Windows 上要真正独立，必须同时做到：
      · 不要 `|` 管道、不要 `-RedirectStandardOutput`（这些会让父进程等子进程）
      · 用 DETACHED_PROCESS + CREATE_NEW_PROCESS_GROUP 脱离父进程组
      · 给子进程**独立的文件句柄**（stdout/stderr 直接指向日志文件）
    这样父进程可以立刻退出，子进程继续跑。

用法：
    python scripts/serve.py                 # 启动（若已在跑则不重复启动）
    python scripts/serve.py --port 5050
    python scripts/serve.py --restart       # 先停旧的再启动
    python scripts/serve.py --stop          # 只停
    python scripts/serve.py --status        # 只看状态
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = ROOT / "logs"
PID_FILE = LOG_DIR / "server.pid"


def http_ok(port: int, timeout: float = 2.0) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/materials", timeout=timeout) as r:
            return r.status == 200
    except (urllib.error.URLError, OSError):
        return False


def listen_pid(port: int) -> int | None:
    """谁在监听这个端口（用 netstat 解析，避免依赖 psutil）。"""
    try:
        out = subprocess.run(
            ["netstat", "-ano", "-p", "TCP"],
            capture_output=True, text=True, timeout=10,
        ).stdout
    except Exception:
        return None
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 5 and parts[0].upper() == "TCP" and parts[3].upper() == "LISTENING":
            if parts[1].endswith(f":{port}"):
                try:
                    return int(parts[4])
                except ValueError:
                    return None
    return None


def status(port: int) -> int:
    pid = listen_pid(port)
    if pid:
        print(f"运行中：端口 {port} 被 PID {pid} 监听；HTTP 检查 {'通过' if http_ok(port) else '失败'}")
        return 0
    print(f"未运行：端口 {port} 无人监听")
    return 1


def stop(port: int) -> int:
    pid = listen_pid(port)
    if not pid:
        print(f"端口 {port} 上没有服务在跑")
        return 0
    subprocess.run(["taskkill", "/PID", str(pid), "/F", "/T"],
                   capture_output=True, text=True)
    time.sleep(0.8)
    if listen_pid(port):
        print(f"⚠️ 端口 {port} 仍在监听")
        return 1
    print(f"已停止 PID {pid}，端口 {port} 已释放")
    if PID_FILE.exists():
        PID_FILE.unlink()
    return 0


def start(port: int, wait: float = 25.0) -> int:
    if listen_pid(port):
        print(f"端口 {port} 已有服务在跑（可直接访问 http://127.0.0.1:{port}）")
        return 0

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    out_path = LOG_DIR / "server.out.log"
    err_path = LOG_DIR / "server.err.log"

    # 关键：文件句柄交给子进程自己持有，父进程不保留管道
    out_f = open(out_path, "ab", buffering=0)
    err_f = open(err_path, "ab", buffering=0)

    flags = 0
    flags |= getattr(subprocess, "DETACHED_PROCESS", 0x00000008)
    flags |= getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0x00000200)
    flags |= getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)

    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUNBUFFERED"] = "1"

    proc = subprocess.Popen(
        [sys.executable, str(ROOT / "app" / "demo_app.py"), "--port", str(port)],
        cwd=str(ROOT),
        stdin=subprocess.DEVNULL,
        stdout=out_f,
        stderr=err_f,
        creationflags=flags,
        close_fds=True,
        env=env,
    )
    PID_FILE.write_text(str(proc.pid), encoding="utf-8")
    print(f"启动中（PID {proc.pid}）…")

    deadline = time.time() + wait
    while time.time() < deadline:
        if proc.poll() is not None:
            print(f"❌ 进程立刻退出（code {proc.returncode}）。日志尾部：")
            print(err_path.read_text(encoding="utf-8", errors="replace")[-2000:])
            return 1
        if http_ok(port):
            print(f"✅ 服务已就绪：http://127.0.0.1:{port}")
            print(f"   PID   : {proc.pid}")
            print(f"   日志  : {err_path}")
            print(f"   停止  : python scripts/serve.py --stop")
            return 0
        time.sleep(0.5)

    print(f"⚠️ {wait:.0f} 秒内未就绪，看日志：{err_path}")
    print(err_path.read_text(encoding="utf-8", errors="replace")[-2000:])
    return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=5000)
    ap.add_argument("--stop", action="store_true")
    ap.add_argument("--restart", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    if args.status:
        return status(args.port)
    if args.stop:
        return stop(args.port)
    if args.restart:
        stop(args.port)
    return start(args.port)


if __name__ == "__main__":
    raise SystemExit(main())
