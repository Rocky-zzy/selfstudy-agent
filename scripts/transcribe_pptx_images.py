# -*- coding: utf-8 -*-
"""临时素材：把 PPTX 里的**代码/图表截图**视觉转写为文本。

为什么必须做（实测理由，不是偏好）：
    `Machine Learning I.pptx` 的正文能直接抽到（23,845 字符），
    但**所有代码块都是图片**——例如第 9 页的 `for` 循环版与向量化版对比、
    第 20 页的 `np.einsum('ij,jk->ik', A, B)`。
    只给散文、不给代码，讲"向量化为什么快"就只能是空话。
    这与 AIAA 2711 正课 PDF「字形转成矢量轮廓、取不到文本」是同一类问题，
    处置方式沿用 `scripts/transcribe_pages.py`：**渲染成图 → 视觉转写**。

约束：
    - **不写入 knowledge_base/**（用户明确：这份课件只是临时测试样本）
    - 产物落 `temp_material/ml1/`，与知识库物理隔离
    - 断点续跑：已转写且非空的图会跳过
    - 失败逐条记录，不静默填充

用法：
    python scripts/transcribe_pptx_images.py            # 全部
    python scripts/transcribe_pptx_images.py --slides 9 20 72
    python scripts/transcribe_pptx_images.py --limit 5  # 只跑前 5 张（试水）
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import time
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
sys.path.insert(0, str(ROOT / "scripts"))

from extract_pptx_temp import PPTX, load  # noqa: E402

OUT = ROOT / "temp_material" / "ml1"
IMGS = ROOT / "temp_material" / "_imgs_all"
STATE = OUT / "_transcribe_state.json"
REPORT = OUT / "_transcribe_report.json"

PROMPT = """这是一页教学幻灯片里的一张插图。请把它的内容转写成文本，供后续讲解使用。

规则：
1. 如果图里是**代码**：逐字转写为 markdown 代码块，保留缩进与注释，**不要改写、不要补全、不要加解释**。
2. 如果图里是**公式**：用 LaTeX 转写。
3. 如果图里是**表格/列表**：转写成 markdown 表格或列表。
4. 如果图里是**纯示意图/流程图/结果截图**：用一两句中文描述它画的是什么（有哪些方框、箭头、坐标轴、数值），
   不要臆造图里没有的数值或文字。
5. 如果图里同时有多种内容，按上面规则分别转写，用小标题标明（如 `代码：`、`描述：`）。
6. 看不清的地方写 `[不清晰]`，**不要猜**。

直接输出转写结果，不要任何额外说明。"""


def extract_all_media(z: zipfile.ZipFile) -> dict[int, list[str]]:
    """每页引用的图片（按 rels 里的顺序 = 通常的阅读顺序）。"""
    per: dict[int, list[str]] = {}
    for name in z.namelist():
        m = re.match(r"ppt/slides/_rels/slide(\d+)\.xml\.rels$", name)
        if not m:
            continue
        num = int(m.group(1))
        xml = z.read(name).decode("utf-8")
        tgts = re.findall(r'Target="\.\./media/([^"]+)"', xml)
        keep = []
        for t in tgts:
            src = "ppt/media/" + t
            if src in z.namelist() and t.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
                keep.append(t)
        per[num] = keep
    return per


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slides", nargs="*", type=int)
    ap.add_argument("--limit", type=int)
    ap.add_argument("--model", default=os.environ.get("DEEPSEEK_MODEL", "deepseek-chat"))
    ap.add_argument("--force", action="store_true", help="忽略断点，重跑")
    args = ap.parse_args()

    from demo_app import load_dotenv

    load_dotenv(ROOT / ".env")
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        print("没有 DEEPSEEK_API_KEY")
        return 2
    from openai import OpenAI

    client = OpenAI(api_key=key, base_url="https://api.deepseek.com", timeout=180)

    OUT.mkdir(parents=True, exist_ok=True)
    IMGS.mkdir(parents=True, exist_ok=True)
    state: dict[str, str] = {}
    if STATE.exists() and not args.force:
        state = json.loads(STATE.read_text(encoding="utf-8"))

    z = zipfile.ZipFile(PPTX)
    per_slide = extract_all_media(z)
    targets = sorted(per_slide) if not args.slides else [s for s in sorted(per_slide) if s in args.slides]

    jobs: list[tuple[int, str]] = []
    for num in targets:
        for t in per_slide[num]:
            jobs.append((num, t))
    if args.limit:
        jobs = jobs[: args.limit]

    print(f"待转写图片：{len(jobs)} 张（共 {sum(len(v) for v in per_slide.values())} 张）")
    ok = skip = fail = 0
    t0 = time.time()
    for i, (num, t) in enumerate(jobs, 1):
        key_ = f"s{num:02d}_{t}"
        if state.get(key_) and not args.force:
            skip += 1
            continue
        src = "ppt/media/" + t
        raw = z.read(src)
        ext = Path(t).suffix.lower().lstrip(".")
        mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
                "gif": "image/gif", "bmp": "image/bmp"}.get(ext, "image/png")
        # 落一份原图便于人工抽查
        img_path = IMGS / key_
        if not img_path.exists():
            img_path.write_bytes(raw)

        b64 = base64.b64encode(raw).decode()
        text = ""
        err = ""
        for attempt in range(1, 4):
            try:
                resp = client.chat.completions.create(
                    model=args.model,
                    messages=[{"role": "user", "content": [
                        {"type": "text", "text": PROMPT},
                        {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                    ]}],
                    temperature=0,
                    max_tokens=2000,
                )
                choice = resp.choices[0]
                if getattr(choice, "finish_reason", "") == "length":
                    raise RuntimeError("被 max_tokens 截断——截断是静默的，必须显式失败")
                text = (choice.message.content or "").strip()
                break
            except Exception as e:
                err = f"{type(e).__name__}: {e}"
                time.sleep(1.5 * attempt)
        if text:
            state[key_] = text
            ok += 1
            print(f"[{i}/{len(jobs)}] OK   slide {num:02d} {t}  ({len(text)} 字符)")
        else:
            fail += 1
            state[key_] = ""
            print(f"[{i}/{len(jobs)}] FAIL slide {num:02d} {t}  {err[:120]}")
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")

    elapsed = time.time() - t0
    report = {
        "model": args.model,
        "images_total": sum(len(v) for v in per_slide.values()),
        "images_done_nonempty": sum(1 for v in state.values() if v),
        "images_empty_or_failed": sum(1 for v in state.values() if not v),
        "this_run": {"ok": ok, "skipped": skip, "failed": fail, "seconds": round(elapsed, 1)},
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"状态文件：{STATE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
