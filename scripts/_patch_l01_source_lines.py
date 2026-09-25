# -*- coding: utf-8 -*-
"""一次性修补：把 L01 图的 `subgoals[].source_line` 换成**真·原文子串**。

为什么：新加的溯源校验（graph_check.py）发现 L01 里 9 条 source_line 全是
**转述**（`B~ → B : Sv`）而不是原文（`$\\widetilde{B} \\to B : Sv$`）。
转述看起来更"干净"，但它让"可回原文核对"变成空话——校验器抓不到编造。

本脚本直接从 knowledge_base 取子串、逐条断言"改完真的能在原文里找到"，
失败就非零退出（不允许"改了但没查"）。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPH = ROOT / "data" / "graph" / "L01.json"
KB = ROOT / "knowledge_base" / "chunks.jsonl"

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def norm(s: str) -> str:
    return re.sub(r"\s+", "", s or "")


chunks = {}
for line in KB.read_text(encoding="utf-8").splitlines():
    if line.strip():
        r = json.loads(line)
        chunks[r["chunk_id"]] = r.get("text") or ""
hay = "".join(norm(v) for v in chunks.values())

# 每条：节点 id → 步骤号 → 原文子串（必须逐字来自 chunks.jsonl）
PATCH: dict[str, dict[int, str]] = {
    "rank_full_rank_cases": {
        1: r"for $\tilde{W} \in \mathbb{R}^{m \times n}$, $\text{rank}(\tilde{W}) = \min\{m, n\}$, then we say $\tilde{W}$ has full rank.",
        2: r"① $\text{rank}(\tilde{W}) = n = m$, space $V$ and $W$ has the same dimension.",
        3: "handling data in a lower dimension in a higher dimension",
    },
    "matrix_form_derivation": {
        1: r"$$y_1 = W_{11}x_1 + W_{21}x_2 + W_{31}x_3 + b_1$$",
        2: r"\begin{bmatrix} W_{11} & W_{21} & W_{31} \\ W_{12} & W_{22} & W_{32} \\ W_{13} & W_{23} & W_{33} \end{bmatrix}",
        3: r"compact form:",
    },
    "basis_change": {
        1: r"$\widetilde{B} \to B : Sv$",
        2: r"$\widetilde{B} \to B \to C : A_\phi Sv$",
        3: r"$\widetilde{B} \to B \to C \to \widetilde{C} : T^{-1}A_\phi Sv$",
    },
}

g = json.loads(GRAPH.read_text(encoding="utf-8"))
by_id = {n["id"]: n for n in g["nodes"]}
bad = []
changed = 0
for nid, steps in PATCH.items():
    n = by_id.get(nid)
    if n is None:
        bad.append(f"图里没有节点 {nid}")
        continue
    for i, txt in steps.items():
        if i - 1 >= len(n.get("subgoals", [])):
            bad.append(f"{nid} 没有第 {i} 个子目标")
            continue
        # 先证明"这段真的在原文里"，再写进图
        if norm(txt) not in hay:
            bad.append(f"{nid} 第 {i} 步：给的子串在知识库里找不到 → {txt[:50]!r}")
            continue
        old = n["subgoals"][i - 1]["source_line"]
        n["subgoals"][i - 1]["source_line"] = txt
        changed += 1
        print(f"  {nid} 第 {i} 步：{old[:34]!r} → {txt[:44]!r}")

if bad:
    print("\n✗ 拒绝写入：")
    for x in bad:
        print("   " + x)
    raise SystemExit(1)

GRAPH.write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"\n已改写 {changed} 条 source_line → {GRAPH.relative_to(ROOT)}")
