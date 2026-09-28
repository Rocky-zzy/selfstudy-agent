# -*- coding: utf-8 -*-
"""数一数英文汇报的**真实正文**词数，并检查末尾标注是否与之一致。

为什么单独写：PowerShell 会把内联正则里的引号吃掉（`docs/00` M13 同源问题），
所以数词这种事要落到文件里做，不能靠命令行内联。
标注行本身也会被算进词数，所以先剔掉再数 —— 这也是发现"标注写错"的办法
（我就在这上面写错过一次：标注 261、实际 270）。
"""
import re
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

p = Path(__file__).resolve().parent.parent / "docs" / "16_季度汇报_英文300词.md"
raw = p.read_text(encoding="utf-8")
body = "\n".join(l for l in raw.splitlines() if not l.startswith("#"))
tag = re.findall(r"\(\s*(\d+)\s*words", body)
body = re.sub(r"\(\s*\d+\s*words[^)]*\)", "", body)
body = re.sub(r"^\s*-\s+", "", body, flags=re.M)
words = re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-/.]*", body)
print("真实正文词数 =", len(words))
print("文件末尾标注 =", tag)
if tag and int(tag[-1]) != len(words):
    print(f"  [!!] 不一致：标注 {tag[-1]} / 实际 {len(words)}")
    raise SystemExit(1)
print("标注一致")
