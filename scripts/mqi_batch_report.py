# -*- coding: utf-8 -*-
r"""出一批 MQI 样本的对照报告（按批次目录）。

与 `mqi_backfill.py --report` 的区别：那个面向旧的"单文件输入"，
这个面向 `data/mqi/batches/<batch>/` 的批次结构（含复用合判结果）。

用法：
    python scripts/mqi_batch_report.py --batch r3
    python scripts/mqi_batch_report.py --batch r3 --judge judge_result_merged.json
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEVELS = ["NotPresent", "Low", "Mid", "High"]
# (编码, 名称, higher_is_better)
CODES = [
    ("3", "Explanations", True),
    ("4", "Sense-Making", True),
    ("12", "Content Errors", False),
    ("13", "Imprecision", False),
    ("14", "Lack of Clarity", False),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    ap.add_argument("--judge", default="judge_result.json")
    args = ap.parse_args()

    d = ROOT / "data" / "mqi" / "batches" / args.batch
    key = {x["id"]: x for x in json.loads((d / "_key.json").read_text(encoding="utf-8"))}
    judge = {x["id"]: x for x in json.loads((d / args.judge).read_text(encoding="utf-8"))}

    agg: dict[str, dict[str, list[int]]] = {c: {"baseline": [], "optimized": []} for c, _, _ in CODES}
    per_q: dict[str, dict[str, dict[str, int]]] = defaultdict(lambda: defaultdict(dict))
    reused = 0
    for iid, j in judge.items():
        k = key.get(iid)
        if not k:
            continue
        if j.get("_reused"):
            reused += 1
        for c, _, _ in CODES:
            v = j.get(c)
            if isinstance(v, int):
                agg[c][k["condition"]].append(v)
                per_q[k["question"]][k["condition"]][c] = v

    def mean(xs):
        return sum(xs) / len(xs) if xs else float("nan")

    print("=" * 84)
    print(f"MQI 批次 {args.batch} 对照（0=Not Present … 3=High）  判定来源：{args.judge}")
    print(f"（其中 {reused} 条为复用上一轮判定）")
    print("=" * 84)
    print(f"{'编码':<5}{'名称':<20}{'极性':<9}{'base':>7}{'opt':>7}{'差':>8}{'两轮方向':>10}")
    for c, name, hib in CODES:
        b, o = agg[c]["baseline"], agg[c]["optimized"]
        pol = "高分好" if hib else "高分差"
        print(f"{c:<5}{name:<20}{pol:<9}{mean(b):>7.2f}{mean(o):>7.2f}"
              f"{mean(o) - mean(b):>+8.2f}")
    print()
    print("分级分布：")
    for c, name, _ in CODES:
        for cond in ("baseline", "optimized"):
            xs = agg[c][cond]
            dist = [xs.count(i) for i in range(4)]
            print(f"  编码 {c:<3}{cond:<10} " +
                  "  ".join(f"{LEVELS[i]}={dist[i]}" for i in range(4)))
    print()
    print("逐问明细（看方向一致性，不要只看均值）：")
    for q, dd in per_q.items():
        b, o = dd.get("baseline", {}), dd.get("optimized", {})
        seg = " ".join(f"c{c}:{b.get(c,'-')}→{o.get(c,'-')}" for c, _, _ in CODES)
        print(f"  {q[:40]:<42} {seg}")

    # 方向一致性：编码 3 逐问比较
    print()
    win = lose = tie = 0
    for q, dd in per_q.items():
        b, o = dd.get("baseline", {}).get("3"), dd.get("optimized", {}).get("3")
        if b is None or o is None:
            continue
        if o > b:
            win += 1
        elif o < b:
            lose += 1
        else:
            tie += 1
    print(f"编码 3 逐问胜负：优化赢 {win} / 输 {lose} / 平 {tie}（共 {win+lose+tie} 问）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
