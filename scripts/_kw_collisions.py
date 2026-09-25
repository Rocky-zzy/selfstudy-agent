# -*- coding: utf-8 -*-
"""看看图里的 keywords 有多少"撞车"——撞车会让提问匹配到错的节点。"""
import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

g = json.loads((ROOT / "data" / "graph" / "rosen-ch1.json").read_text(encoding="utf-8"))
c: dict[str, set[str]] = collections.defaultdict(set)
for n in g["nodes"]:
    for k in n.get("keywords") or []:
        c[k].add(n["id"].split("__", 1)[1])
dup = {k: sorted(v) for k, v in c.items() if len(v) > 1}
total = sum(len(n.get("keywords") or []) for n in g["nodes"])
print(f"关键词 {total} 条（唯一 {len(c)}），撞车 {len(dup)} 条")
for k, v in sorted(dup.items(), key=lambda x: -len(x[1])):
    print(f"  {k!r} → {len(v)} 个节点：{v}")
