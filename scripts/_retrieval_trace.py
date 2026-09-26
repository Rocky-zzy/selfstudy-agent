# -*- coding: utf-8 -*-
"""看检索对某个问题到底选中了哪些页——用于排查"该进的节点为什么没进来"。"""
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
from retrieval import load_chunks, search  # noqa: E402

g = gi.load_graph("rosen-ch1")
chunks = load_chunks(ROOT / "data" / "rosen" / "ch1" / "chunks.jsonl")
present_pages = {c.chunk_id: c for c in chunks}

QS = [
    ("1.7", "怎么用反证法证明？它和逆否证明有什么区别？"),
    ("1.7", "直接证明、空证明、平凡证明分别在什么情况下用？"),
    ("1.3", "什么是可满足性？为什么它重要？"),
    ("1.4", "怎么否定一个带量词的命题？"),
]
for lec, q in QS:
    sel = search(q, chunks, lecture=lec, top_k=4, bridge=True,
                 whole_lecture=False, page_range=None)
    print("==", lec, q)
    for c in sel:
        print(f"   选中 {c.chunk_id} p{c.page} score={getattr(c, 'score', '?')}")
    print("   关键词命中：")
    for n in g["nodes"]:
        hits = gi._hits(q, n)
        if hits:
            ov = bool(set(n.get("sources") or []) & {c.chunk_id for c in sel})
            print(f"     {n['id'].split('__', 1)[1]:34} hits={hits} 页重合={ov} "
                  f"节={'/'.join(sorted({s.split('-')[1] for s in n.get('sources') or []}))}")
    print()
