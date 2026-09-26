# -*- coding: utf-8 -*-
r"""合并「裸 LLM vs 最终版」的盲判结果，并出对照报告。

与 r4 那轮的区别：
  · 答案键是 `_raw_map.json`（id → raw / optimized），不是 _key.json；
  · 只报两组（raw / optimized），不含 baseline —— 这一轮要回答的问题只有一个：
    "**最终优化版比裸 LLM 好多少**"。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODES = [("3", "Explanations", True), ("4", "Sense-Making", True),
         ("12", "Content Errors", False), ("13", "Imprecision", False),
         ("14", "Lack of Clarity", False)]
LEVELS = ["NotPresent", "Low", "Mid", "High"]
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    ap.add_argument("--write", action="store_true", help="把合并结果写盘")
    args = ap.parse_args()

    d = ROOT / "data" / "mqi" / "batches" / args.batch
    mapping = json.loads((d / "_raw_map.json").read_text(encoding="utf-8"))

    merged: dict[str, dict] = {}
    for p in sorted(d.glob("judge_raw[0-9]*.json")):
        for r in json.loads(p.read_text(encoding="utf-8")):
            iid = r.get("id")
            if iid in merged:
                print(f"  [!!] 重复判定 {iid}")
                return 1
            for c, _n, _h in CODES:
                v = r.get(c)
                if not isinstance(v, int) or not 0 <= v <= 3:
                    print(f"  [!!] {p.name} {iid} 编码 {c} 非法：{v!r}")
                    return 1
            merged[iid] = r
    missing = sorted(set(mapping) - set(merged))
    if missing:
        print(f"  [!!] 缺判定：{missing}")
        return 1
    print(f"合并 {len(merged)} 段，id 齐全、取值合法")

    if args.write:
        out = [merged[i] for i in sorted(merged)]
        (d / "judge_result_raw.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"已写 {d / 'judge_result_raw.json'}")

    def mean(xs):
        return sum(xs) / len(xs) if xs else float("nan")

    print()
    print("=" * 88)
    print(f"MQI 对照：裸 LLM vs 最终优化版（批次 {args.batch}，20 问 × 2）")
    print("=" * 88)
    print(f"{'编码':<5}{'名称':<20}{'极性':<9}{'裸LLM':>8}{'最终版':>8}{'差':>8}")
    agg = {c: {"raw": [], "optimized": []} for c, _n, _h in CODES}
    per_q: dict[str, dict[str, dict[str, int]]] = {}
    for iid, j in merged.items():
        cond = mapping[iid]
        q = j.get("_question") or iid
        for c, _n, _h in CODES:
            agg[c][cond].append(j[c])
    for c, name, hib in CODES:
        r, o = agg[c]["raw"], agg[c]["optimized"]
        print(f"{c:<5}{name:<20}{'高分好' if hib else '高分差':<9}"
              f"{mean(r):>8.2f}{mean(o):>8.2f}{mean(o) - mean(r):>+8.2f}")

    print()
    print("分级分布（关键是 High 那一列）：")
    for c, name, _h in CODES:
        for cond in ("raw", "optimized"):
            xs = agg[c][cond]
            dist = [xs.count(i) for i in range(4)]
            print(f"  编码 {c:<3}{cond:<10} " +
                  "  ".join(f"{LEVELS[i]}={dist[i]}" for i in range(4)))

    # 逐问胜负：按答案键把每问的两段配起来
    pairs: dict[str, dict[str, dict]] = {}
    for iid, cond in mapping.items():
        pairs.setdefault(iid[:3], {})[cond] = merged[iid]
    print()
    win = lose = tie = 0
    rows = []
    for qid in sorted(pairs):
        pr = pairs[qid]
        if "raw" not in pr or "optimized" not in pr:
            continue
        a, b = pr["raw"]["3"], pr["optimized"]["3"]
        mark = "赢" if b > a else ("输" if b < a else "平")
        win += b > a
        lose += b < a
        tie += b == a
        rows.append((qid, a, b, mark))
    print("编码 3 逐问（裸 → 最终版）：")
    for qid, a, b, mark in rows:
        print(f"  {qid}  {a} → {b}   {mark}")
    print()
    print(f"编码 3 逐问胜负：最终版**赢 {win} / 输 {lose} / 平 {tie}**（共 {win + lose + tie} 问）")
    hr = agg["3"]["raw"].count(3)
    ho = agg["3"]["optimized"].count(3)
    print(f"编码 3 的 High 比例：裸 LLM {hr}/20 = {hr / 20:.0%} → "
          f"最终版 {ho}/20 = {ho / 20:.0%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
