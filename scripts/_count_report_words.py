# -*- coding: utf-8 -*-
"""数一数英文汇报的字数（不含标题行、不含末尾的 (N words) 标注）。"""
import re
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

p = Path(__file__).resolve().parent.parent / "docs" / "16_季度汇报_英文300词.md"
lines = [l for l in p.read_text(encoding="utf-8").splitlines()
         if not l.startswith("#")]
body = "\n".join(lines)
body = re.sub(r"\(\d+ words\)", "", body)
body = re.sub(r"^\s*-\s+", "", body, flags=re.M)
words = re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-/.]*", body)
print("word count =", len(words))
