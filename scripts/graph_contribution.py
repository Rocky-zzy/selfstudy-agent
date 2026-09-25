# -*- coding: utf-8 -*-
r"""知识结构到底"多给了什么"——纯计算，不调模型。

要回答的问题：注入的知识节点里，有多少是**检索本来就会碰到**的（那它没贡献），
有多少是**检索没碰到的**（那才是它真正加进来的信息）。

判据（可核对）：`/api/ask` 会回传 `citations`（本次选中了哪些页）。
把每个被注入节点的 `sources` 与这次选中的页求交集：
  - 完全不相交 → 该节点**完全靠图进来**（前置/对比/关键词命中）
  - 有交集     → 它本来就在这批页里，图只是"提前告诉我们它叫什么"
"""
from __future__ import annotations

import json
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

QUESTIONS = [
    ("1.1", "什么是命题？"),
    ("1.1", "逆否命题和原命题等价吗？"),
    ("1.3", "怎么用真值表判断两个命题是否等价？"),
    ("1.4", "怎么否定一个带量词的命题？"),
    ("1.5", "什么是嵌套量词？"),
    ("1.6", "什么是假言三段论？"),
    ("1.7", "怎么用反证法证明？"),
    ("1.7", "空证明和平凡证明有什么区别？"),
    ("1.8", "怎么用分情形证明？"),
]

# 用检索器现算"这次会选中哪些页"，与 /api/ask 的 citations 同源
from retrieval import load_chunks, search  # noqa: E402

g = gi.load_graph("rosen-ch1")
chunks = load_chunks(ROOT / "data" / "rosen" / "ch1" / "chunks.jsonl")
by_id = {n["id"]: n for n in g["nodes"]}

print(f"{'节':4} {'问题':34} 注入  其中「图独有」")
print("-" * 78)
tot = new = 0
for lec, q in QUESTIONS:
    sel = search(q, chunks, lecture=lec, top_k=4, bridge=True,
                 whole_lecture=False, page_range=None)
    present = [c.chunk_id for c in sel]
    _inj, ids = gi.build_injection(g, present, q)
    fresh = [i for i in ids if not (set(by_id[i].get("sources") or []) & set(present))]
    tot += len(ids)
    new += len(fresh)
    mark = "、".join(i.split("__", 1)[1] for i in fresh) or "—"
    print(f"{lec:4} {q:34} {len(ids):3}   {len(fresh)}  {mark}")
print("-" * 78)
print(f"合计注入 {tot} 个节点次，其中 {new} 个（{new / tot:.0%}）是检索页里没有的"
      f"——这部分才是知识结构**真正加进来**的信息。")
