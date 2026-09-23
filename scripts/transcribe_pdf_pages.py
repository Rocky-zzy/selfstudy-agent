# -*- coding: utf-8 -*-
"""临时素材：PDF 逐页**整页渲染 + 视觉转写**。

什么时候需要（实测依据，不是偏好）：
    `lecture-6-qa.pdf` 有文本层（31 页 / 13,516 字符），但**关键内容仍在图里**。
    例：第 7 页「Context-free grammar」的正文只有几个空标题
        （"A CFG consists of 4 elements:" 后面什么都没有），
        而 N/Σ/R/S 的完整定义全在一张 1196×405 的图里。
    只抽文本层会得到"有标题、没内容"的课件——这正是最坏的失败：
    看起来有料，实际讲不出东西。

做法：整页渲染成 PNG → 视觉转写。比"逐张剥图"更完整（保留页面版式与图文关系），
     并且能顺手跳过重复的页眉标识（本文件是 472×72）。

约束：
    - **不进 knowledge_base/**（用户要求隔离；与 tmp_ml1 同理）
    - 产物落 `temp_material/nlp6/`，状态文件支持断点续跑
    - 转写失败逐条记录，不静默填空白

用法：
    python scripts/transcribe_pdf_pages.py                # 全部页
    python scripts/transcribe_pdf_pages.py --pages 7 14 16
    python scripts/transcribe_pdf_pages.py --only-image-pages   # 只跑有内容图的页
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))

SRC = Path(
    r"C:\Users\27059\.dsh\attachments\v1\files\32"
    r"\328aa1a8edee30493d8267b14cb3ceb2f6fdb33e4f3e698169cea10c3fb9d0dd\lecture-6-qa.pdf"
)
OUT = ROOT / "temp_material" / "nlp6"
PAGES_DIR = OUT / "_pages"
STATE = OUT / "_transcribe_state.json"

LOGO_SIZES = {(472, 72), (503, 106), (728, 78), (661, 91)}
MIN_CONTENT_PX = 300  # 宽或高小于此值视为装饰

PROMPT = """这是一页教学幻灯片的**整页渲染图**。请把这一页的内容转写成结构化文本，供后续讲解使用。

要求：
1. 先给一行 `标题：` 写下本页标题（若有）。
2. 然后**按页面上的阅读顺序**转写全部实质内容：
   - 正文/要点 → markdown 列表或段落
   - **图片、示意图、表格里的文字与公式也要转写出来**（这些往往是本页的核心定义）
   - 示意图/流程图 → 用一两句中文描述它画了什么（有哪些方框、箭头、标注）
   - 公式 → LaTeX
   - 代码 → markdown 代码块
3. **不要遗漏图片里出现的定义、符号表、例子**——这一页的图片里常常就是正文没写的内容。
4. 忽略页眉页脚里的课程名、"AIAA 4051 Fall 2026 Natural Language Processing" 这类重复标识，
   以及纯装饰图片。
5. 看不清的地方写 `[不清晰]`，**不要猜**。

直接输出转写结果，不要任何额外说明。"""


def content_image_pages(doc: fitz.Document) -> list[int]:
    """哪些页含"非页眉"的实质图片。"""
    out = []
    for i, pg in enumerate(doc, 1):
        for info in pg.get_images(full=True):
            w, h = info[2], info[3]
            if (w, h) in LOGO_SIZES:
                continue
            if w >= MIN_CONTENT_PX and h >= MIN_CONTENT_PX:
                out.append(i)
                break
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", nargs="*", type=int)
    ap.add_argument("--only-image-pages", action="store_true")
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--model", default=os.environ.get("DEEPSEEK_MODEL", "deepseek-chat"))
    args = ap.parse_args()

    from demo_app import load_dotenv

    load_dotenv(ROOT / ".env")
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        print("没有 DEEPSEEK_API_KEY")
        return 2
    from openai import OpenAI

    client = OpenAI(api_key=key, base_url="https://api.deepseek.com", timeout=180)

    doc = fitz.open(SRC)
    OUT.mkdir(parents=True, exist_ok=True)
    PAGES_DIR.mkdir(parents=True, exist_ok=True)

    if args.pages:
        targets = [p for p in args.pages if 1 <= p <= doc.page_count]
    elif args.only_image_pages:
        targets = content_image_pages(doc)
    else:
        targets = list(range(1, doc.page_count + 1))

    state: dict[str, str] = {}
    if STATE.exists() and not args.force:
        state = json.loads(STATE.read_text(encoding="utf-8"))

    print(f"总页数 {doc.page_count}；含实质图片的页 {content_image_pages(doc)}")
    print(f"本次处理 {len(targets)} 页：{targets}")

    ok = skip = fail = 0
    t0 = time.time()
    zoom = args.dpi / 72.0
    for i, pno in enumerate(targets, 1):
        key_ = f"p{pno:02d}"
        if state.get(key_) and not args.force:
            skip += 1
            continue
        pg = doc[pno - 1]
        png_path = PAGES_DIR / f"{key_}.png"
        if not png_path.exists():
            pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
            pix.save(png_path)
        b64 = base64.b64encode(png_path.read_bytes()).decode()

        text = ""
        err = ""
        for attempt in range(1, 4):
            try:
                resp = client.chat.completions.create(
                    model=args.model,
                    messages=[{"role": "user", "content": [
                        {"type": "text", "text": PROMPT},
                        {"type": "image_url",
                         "image_url": {"url": "data:image/png;base64," + b64}},
                    ]}],
                    temperature=0,
                    max_tokens=2500,
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
            print(f"[{i}/{len(targets)}] OK   page {pno:2d}  ({len(text)} 字符)")
        else:
            state[key_] = ""
            fail += 1
            print(f"[{i}/{len(targets)}] FAIL page {pno:2d}  {err[:120]}")
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")

    report = {
        "model": args.model,
        "dpi": args.dpi,
        "pages_total": doc.page_count,
        "transcribed_nonempty": sum(1 for v in state.values() if v),
        "transcribed_empty_or_failed": sum(1 for v in state.values() if not v),
        "this_run": {"ok": ok, "skipped": skip, "failed": fail,
                     "seconds": round(time.time() - t0, 1)},
    }
    (OUT / "_transcribe_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
