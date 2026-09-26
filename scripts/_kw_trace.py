# -*- coding: utf-8 -*-
"""看清"哪个关键词把节点拉进了注入列表"——用于调匹配门槛。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import graph_inject as gi  # noqa: E402

g = gi.load_graph("rosen-ch1")
QS = [
    "怎么用反证法证明？",
    "全称量词和存在量词分别是什么？为什么需要论域？",
    "什么是命题？为什么需要「真值」这个概念？",
    "分情形证明怎么做？什么时候该想到用它？",
]
for q in QS:
    print("==", q)
    for n in g["nodes"]:
        w, longest, _ = gi._score(q, n)
        if w >= 1:
            cands = [n.get("title", "")] + list(n.get("keywords") or [])
            hits = [c for c in cands if c and c in q]
            print(f"   w={w} longest={longest}  {n['id'].split('__', 1)[1]:34} hits={hits}")
    print()
