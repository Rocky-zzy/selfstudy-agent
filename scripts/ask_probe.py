# -*- coding: utf-8 -*-
r"""从正在运行的服务问一个问题，把**两段讲解原文**存下来，供人工核对。

为什么单独写一个（而不是每次现敲 curl/python -c）：
    评估"模型有没有照注入的步骤标签来组织讲解"必须**看真实输出**，
    而输出又长又带 LaTeX，直接打在控制台里没法读。存成文件才能逐段比对。

用法：
    python scripts/ask_probe.py --lecture 1.7 --question "怎么用反证法证明？"
    python scripts/ask_probe.py --lecture 1.7 --question "..." --no-graph   # 关掉知识结构对照
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "logs" / "probes"

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE = "http://127.0.0.1:5000"


def post(path: str, body: dict) -> dict:
    req = urllib.request.Request(
        BASE + path, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))


def strip_math(text: str, items: list[str]) -> str:
    """把占位符换回公式原文——存盘是给人读的，不该存一堆 \\u2981MATH0\\u2981。"""
    def sub(m: re.Match) -> str:
        i = int(m.group(1))
        return items[i] if 0 <= i < len(items) else m.group(0)
    return re.sub("\u2981MATH(\\d+)\u2981", sub, text or "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--question", required=True)
    ap.add_argument("--lecture", default="1.7")
    ap.add_argument("--material", default="rosen-ch1")
    ap.add_argument("--teaching", default="detailed")
    ap.add_argument("--top-k", type=int, default=4)
    ap.add_argument("--no-graph", action="store_true")
    args = ap.parse_args()

    d = post("/api/ask", {
        "question": args.question, "material": args.material, "lecture": args.lecture,
        "teaching": args.teaching, "top_k": args.top_k,
        "use_graph": not args.no_graph,
    })
    if d.get("error"):
        print("失败：" + d["error"])
        return 1
    reveal = post("/api/reveal", {"trace_id": d["trace_id"]})
    cond_of = {s: (lab or {}).get("condition")
               for s, lab in (reveal.get("labels") or {}).items()}

    OUT.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    lines = [
        f"# 探针 {stamp}",
        f"- 素材 {args.material} / 节 {args.lecture} / 讲法 {args.teaching}",
        f"- 问题：{args.question}",
        f"- 知识结构注入：{'关' if args.no_graph else '开'}"
        f"（{d.get('graph_used')}｜{d.get('graph_note')}）",
        f"- 检索：{d.get('mode')} / {len(d.get('citations') or [])} 页 / "
        f"{d.get('ctx_chars')} 字符 / 降级={bool(d.get('downgrade'))}",
        "",
    ]
    for slot in ("A", "B"):
        a = (d.get("answers") or {}).get(slot) or {}
        cond = cond_of.get(slot) or "?"
        body = strip_math(a.get("text") or "", a.get("math") or [])
        lines += [f"{'=' * 78}", f"## 槽位 {slot}（真实条件：{cond}）  {len(body)} 字符",
                  f"{'=' * 78}", "", body, ""]
    p = OUT / f"probe-{stamp}.md"
    p.write_text("\n".join(lines), encoding="utf-8")
    print(f"已存 {p}")
    print(f"  注入节点：{d.get('graph_used')}")
    print(f"  长度：A {len((d['answers'].get('A') or {}).get('text') or '')} / "
          f"B {len((d['answers'].get('B') or {}).get('text') or '')} 字符")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
