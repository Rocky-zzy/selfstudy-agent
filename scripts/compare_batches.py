# -*- coding: utf-8 -*-
r"""把两个 MQI 批次按**同题同条件**配对对比（如 r4 vs r5：同一批 20 问、机制改了）。

为什么需要这个脚本：docs/12 每轮都强调"素材/题目不同就不能比均值"；
r5 与 r4 用的是**同一批 20 问**（make_mqi_batch 的问题清单是硬编码的），
所以可以配对到**每一问**上比较——这比均值差有信息量得多。
对应 docs/15 §四 的验收口径：主指标 = 编码 3 High 比例是否上升（配对地看）。

用法：
    python scripts/compare_batches.py --old r4 --new r5
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def load(batch: str) -> dict[tuple[str, str], dict]:
    """返回 {(question, condition): judge_row}。condition 以 baseline/optimized 归一。"""
    d = ROOT / "data" / "mqi" / "batches" / batch
    key = {x["id"]: x for x in json.loads((d / "_key.json").read_text(encoding="utf-8"))}
    rows = json.loads((d / "judge_result.json").read_text(encoding="utf-8"))
    out: dict[tuple[str, str], dict] = {}
    for r in rows:
        k = key.get(r["id"])
        if not k:
            continue
        out[(k["question"], k["condition"])] = r
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--old", required=True, help="基线批次名，如 r4")
    ap.add_argument("--new", required=True, help="新批次名，如 r5")
    ap.add_argument("--code", default="3", help="要看哪个编码（默认 3）")
    args = ap.parse_args()

    old, new = load(args.old), load(args.new)
    questions = sorted({q for q, _ in old.keys()} & {q for q, _ in new.keys()})
    dropped = ({q for q, _ in old.keys()} | {q for q, _ in new.keys()}) - set(questions)
    if dropped:
        print(f"⚠️ {len(dropped)} 问只在一边有（不进配对）：")
        for q in sorted(dropped):
            print(f"   {q[:50]}")

    code = args.code
    print(f"编码 {code} 配对（{args.old} -> {args.new}），共 {len(questions)} 问")
    print("=" * 88)

    stats = {"base": [], "opt": []}
    moves = {"opt_up": 0, "opt_down": 0, "opt_same": 0,
             "base_up": 0, "base_down": 0, "base_same": 0}
    unfavorable: list[str] = []
    for q in questions:
        ob = old.get((q, "baseline"))
        oo = old.get((q, "optimized"))
        nb = new.get((q, "baseline"))
        no = new.get((q, "optimized"))
        if not all([ob, oo, nb, no]):
            print(f"缺行，跳过：{q[:50]}")
            continue
        obv, oov, nbv, nov = ob[code], oo[code], nb[code], no[code]
        stats["base"].append(nbv)
        stats["opt"].append(nov)
        if nov > oov:
            moves["opt_up"] += 1
        elif nov < oov:
            moves["opt_down"] += 1
        else:
            moves["opt_same"] += 1
        if nbv > obv:
            moves["base_up"] += 1
        elif nbv < obv:
            moves["base_down"] += 1
        else:
            moves["base_same"] += 1
        # 方向对我方不利的移动 = 优化侧下降（或基线上升更多）——M18 要回原文核
        if nov < oov:
            unfavorable.append(q)
        print(f"{q[:40]:<42} base {obv}->{nbv}   opt {oov}->{nov}")

    n = len(stats["opt"])
    if n == 0:
        print("没有可配对的题。")
        return 1

    print("-" * 88)
    print(f"均值：base {sum(stats['base'])/n:.2f}  opt {sum(stats['opt'])/n:.2f}  "
          f"差 {sum(stats['opt'])/n - sum(stats['base'])/n:+.2f}")
    print(f"High（=3）比例：base {sum(1 for v in stats['base'] if v == 3)}/{n}"
          f"  opt {sum(1 for v in stats['opt'] if v == 3)}/{n}")
    print(f"优化侧逐问：升 {moves['opt_up']} / 降 {moves['opt_down']} / 平 {moves['opt_same']}"
          f"   基线侧：升 {moves['base_up']} / 降 {moves['base_down']} / 平 {moves['base_same']}")
    if unfavorable:
        print(f"\n★ 优化侧下降的 {len(unfavorable)} 问（M18：**必须回原文核对判定**）：")
        for q in unfavorable:
            print(f"   {q}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
