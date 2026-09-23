# -*- coding: utf-8 -*-
"""临时素材：把 Machine Learning I.pptx 抽成逐页文本，供本次体验使用。

**不进 knowledge_base/**（用户 2026-09-17 明确要求：这份课件只是临时测试样本）。

用法：
    python scripts/extract_pptx_temp.py                 # 打印概览
    python scripts/extract_pptx_temp.py --dump 1 5      # 打印第 1–5 页全文
    python scripts/extract_pptx_temp.py --all           # 打印全部
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import zipfile
from pathlib import Path

PPTX = Path(
    r"C:\Users\27059\.dsh\attachments\v1\files\b7"
    r"\b70d953cfdfb1fcba717cc3e72eecabad247c2a0ca30ae95a962f0d68efb9310\Machine Learning I.pptx"
)
OUT_DIR = Path(__file__).resolve().parent.parent / "temp_material" / "ml1"


def slide_num(name: str) -> int:
    return int(re.search(r"slide(\d+)\.xml", name).group(1))


def para_texts(xml: str) -> list[str]:
    """按段落抽 <a:t> 文本，保留段落换行。"""
    out: list[str] = []
    for para in re.findall(r"<a:p>(.*?)</a:p>", xml, re.S):
        t = "".join(html.unescape(x) for x in re.findall(r"<a:t>(.*?)</a:t>", para, re.S))
        t = t.strip()
        if t:
            out.append(t)
    return out


def notes_texts(xml: str) -> list[str]:
    return para_texts(xml)


def load() -> tuple[list[tuple[int, list[str], list[str], int]], dict]:
    z = zipfile.ZipFile(PPTX)
    names = z.namelist()
    slides = sorted(
        [n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)], key=slide_num
    )
    # slide 的 rels 里找 notesSlide
    pages = []
    for n in slides:
        num = slide_num(n)
        body = para_texts(z.read(n).decode("utf-8"))
        rels_name = f"ppt/slides/_rels/slide{num}.xml.rels"
        notes: list[str] = []
        if rels_name in names:
            rels = z.read(rels_name).decode("utf-8")
            m = re.search(r'Target="\.\./(notesSlides/notesSlide\d+\.xml)"', rels)
            if m:
                np = "ppt/" + m.group(1)
                if np in names:
                    notes = notes_texts(z.read(np).decode("utf-8"))
        n_media = 0
        if rels_name in names:
            n_media = len(re.findall(r'Target="\.\./media/', z.read(rels_name).decode("utf-8")))
        # 该页引用的图片大小合计
        pages.append((num, body, notes, n_media))
    meta = {
        "slides": len(pages),
        "media_files": len([x for x in names if x.startswith("ppt/media/")]),
    }
    return pages, meta


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dump", nargs=2, type=int, metavar=("FROM", "TO"))
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--save", action="store_true", help="写到 temp_material/ml1/")
    args = ap.parse_args()

    pages, meta = load()
    body_chars = sum(len("".join(b)) for _, b, _, _ in pages)
    note_chars = sum(len("".join(n)) for _, _, n, _ in pages)
    empty_body = [num for num, b, _, _ in pages if not b]
    img_only = [num for num, b, _, m in pages if m and len("".join(b)) < 60]

    print(f"文件   : {PPTX.name}")
    print(f"页数   : {meta['slides']}   媒体文件: {meta['media_files']}")
    print(f"正文   : {body_chars} 字符   备注: {note_chars} 字符")
    print(f"无正文页: {len(empty_body)} {empty_body[:20]}")
    print(f"疑似图为主页: {len(img_only)} {img_only[:20]}")

    if args.save:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        for num, body, notes, _ in pages:
            parts = [f"# Slide {num:02d}", ""]
            parts += body
            if notes:
                parts += ["", "## 演讲者备注", ""] + notes
            (OUT_DIR / f"slide{num:02d}.md").write_text("\n".join(parts), encoding="utf-8")
        print(f"已写入 {OUT_DIR}（{len(pages)} 个文件）")

    if args.dump or args.all:
        lo, hi = (1, 10**6) if args.all else (args.dump[0], args.dump[1])
        for num, body, notes, _ in pages:
            if not (lo <= num <= hi):
                continue
            print("=" * 74)
            print(f"SLIDE {num:02d}")
            print("-" * 74)
            for t in body:
                print("  |", t)
            if notes:
                print("  --- 备注 ---")
                for t in notes:
                    print("  ~", t)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
