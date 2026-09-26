# -*- coding: utf-8 -*-
r"""跑一遍**整批问题**，看知识结构给每个问题注入了哪些节点——不调模型，几秒出结果。

为什么值得单独跑一遍：上一版的选择规则在"这一节整体在讲什么"上给出过
"位串 / 按位运算"，这种错**只有把整批问题一起看**才发现得了
（单个问题看起来都"有输出"，像是正常工作）。

用法：
    python scripts/graph_targets_probe.py                 # 主数据集 Rosen 第 1 章
    python scripts/graph_targets_probe.py --material kb   # AIAA 2711
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
sys.path.insert(0, str(ROOT / "scripts"))
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import graph_inject as gi  # noqa: E402
from retrieval import load_chunks, search  # noqa: E402

MAT = {
    "rosen-ch1": ("rosen-ch1", ROOT / "data" / "rosen" / "ch1" / "chunks.jsonl"),
    "kb": ("L01", ROOT / "knowledge_base" / "chunks.jsonl"),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--material", default="rosen-ch1")
    args = ap.parse_args()

    import make_mqi_batch as mb  # noqa: E402

    scope, kb = MAT[args.material]
    questions = (mb.QUESTIONS_ROSEN_CH1 if args.material == "rosen-ch1" else mb.QUESTIONS)
    g = gi.load_graph(scope)
    chunks = load_chunks(kb)
    by_id = {n["id"]: n for n in g["nodes"]}

    print(f"素材 {args.material} / 图 {scope}（{len(g['nodes'])} 节点）/ {len(questions)} 问")
    print("=" * 100)
    empty = 0
    for lec, _teach, q in questions:
        sel = search(q, chunks, lecture=lec, top_k=4, bridge=True,
                     whole_lecture=False, page_range=None)
        inj, ids = gi.build_injection(g, [c.chunk_id for c in sel], q)
        names = [i.split("__", 1)[1] for i in ids]
        if not ids:
            empty += 1
        print(f"{lec}  {q}")
        print(f"     展开：{'、'.join(names) if names else '（无：只给目录）'}")
        for line in inj.split("\n"):
            if "清单" in line or "只列名字" in line:
                print(f"     目录：{line.strip()[:130]}…")
    print("=" * 100)
    print(f"{empty}/{len(questions)} 问没有可展开的节点（只注入目录）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
