# -*- coding: utf-8 -*-
r"""把 docx / pdf 的正文抽成文本，供阅读与整理。

为什么写脚本而不是随手抽一次：
    这几份文件是**只读副本**（在 .dsh/attachments 下），而且 docx 是压缩包、
    PDF 有排版噪声，直接用文本工具读会失败或读到乱码。抽一次存到 temp_material/，
    后面（写报告、核对引用）就能反复引用同一份文本，不必重复解析。

用法：
    python scripts/extract_docs.py <文件...>          # 抽到 temp_material/_refs/
"""
from __future__ import annotations

import html
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "temp_material" / "_refs"

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def docx_text(p: Path) -> str:
    z = zipfile.ZipFile(p)
    parts = [n for n in z.namelist()
             if re.fullmatch(r"word/(document|header\d*|footer\d*|footnotes|endnotes)\.xml", n)]
    chunks = []
    for name in ["word/document.xml"] + [x for x in parts if x != "word/document.xml"]:
        x = z.read(name).decode("utf-8", errors="replace")
        # 表格单元格转换行、段落转换行、制表符保留
        x = x.replace("</w:tc>", "\t")
        x = re.sub(r"</w:p>", "\n", x)
        x = re.sub(r"<w:tab[^>]*/>", "\t", x)
        x = re.sub(r"<w:br[^>]*/>", "\n", x)
        t = html.unescape(re.sub(r"<[^>]+>", "", x))
        chunks.append(t)
    return "\n".join(chunks)


def pdf_text(p: Path) -> str:
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return "（没有 PyMuPDF，无法抽 PDF 正文）"
    d = fitz.open(p)
    return "\n\n".join(f"===== 第 {i + 1} 页 =====\n{pg.get_text()}" for i, pg in enumerate(d))


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for a in sys.argv[1:]:
        p = Path(a)
        if not p.exists():
            print(f"  [!!] 不存在：{p}")
            continue
        t = docx_text(p) if p.suffix.lower() == ".docx" else pdf_text(p)
        lines = [l.rstrip() for l in t.splitlines()]
        # 压掉大量空行，方便阅读（不改内容）
        out, blank = [], 0
        for l in lines:
            if l.strip():
                blank = 0
                out.append(l)
            else:
                blank += 1
                if blank <= 1:
                    out.append("")
        dst = OUT / (p.stem + ".txt")
        dst.write_text("\n".join(out).strip() + "\n", encoding="utf-8")
        print(f"  {p.name}  {len(t)} 字符 -> {dst.relative_to(ROOT)}  ({len(out)} 行)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
