# -*- coding: utf-8 -*-
"""临时素材：从 PDF 里剥出图片，供人工查看（判断是否需要视觉转写）。

与 PPTX 那条路（scripts/_dump_slide_media.py）同理，只是换成 PyMuPDF。
"""

from __future__ import annotations

import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(
    r"C:\Users\27059\.dsh\attachments\v1\files\32"
    r"\328aa1a8edee30493d8267b14cb3ceb2f6fdb33e4f3e698169cea10c3fb9d0dd\lecture-6-qa.pdf"
)
OUT = ROOT / "temp_material" / "_nlp6_imgs"

# 重复出现的尺寸多为页眉标识，不是内容
LOGO_SIZES = {(472, 72), (503, 106)}


def main() -> int:
    pages = [int(x) for x in sys.argv[1:]] or [14, 16, 18, 7]
    doc = fitz.open(SRC)
    OUT.mkdir(parents=True, exist_ok=True)
    seen_total = 0
    for pno in pages:
        pg = doc[pno - 1]
        imgs = pg.get_images(full=True)
        print(f"--- page {pno}: {len(imgs)} 张图 ---")
        for j, info in enumerate(imgs):
            xref, w, h = info[0], info[2], info[3]
            if (w, h) in LOGO_SIZES:
                print(f"    [跳过] {w}x{h}（疑似页眉标识）")
                continue
            pix = fitz.Pixmap(doc, xref)
            if pix.n - pix.alpha >= 4:  # CMYK -> RGB
                pix = fitz.Pixmap(fitz.csRGB, pix)
            dst = OUT / f"p{pno:02d}_{j}_{w}x{h}.png"
            pix.save(dst)
            print(f"    saved {dst.name}  ({w}x{h})")
            seen_total += 1
    print(f"\n共导出 {seen_total} 张 -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
