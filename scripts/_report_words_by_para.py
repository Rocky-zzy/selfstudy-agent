# -*- coding: utf-8 -*-
"""把每段的词数打出来，便于按段压缩到目标字数（默认 260）。"""
import re
import sys
from pathlib import Path

TARGET = int(sys.argv[1]) if len(sys.argv) > 1 else 260
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

p = Path(__file__).resolve().parent.parent / "docs" / "16_季度汇报_英文300词.md"
raw = p.read_text(encoding="utf-8")
paras = [l.strip() for l in raw.splitlines()
         if l.strip() and not l.startswith("#") and not re.match(r"^\(\s*\d+\s*words", l.strip())]
total = 0
for i, t in enumerate(paras, 1):
    n = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-/.]*", t))
    total += n
    print(f"  段 {i}: {n:4d} 词   {t[:46]}")
print(f"合计 {total} 词；目标 {TARGET}，需再减 {total - TARGET}")
