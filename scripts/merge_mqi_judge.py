# -*- coding: utf-8 -*-
r"""把各分片的盲判结果合并成一份，并**先校验完整性**再写盘。

为什么要校验：分片判分容易出现"某片少判了几条"或"两个片都判了同一条"，
不校验就会让报告里的均值悄悄建立在缺样本的基础上（`docs/00` M11/M12 的同类问题）。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODES = ("3", "4", "12", "13", "14")
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    args = ap.parse_args()

    d = ROOT / "data" / "mqi" / "batches" / args.batch
    blind = {x["id"]: x for x in json.loads((d / "blind.json").read_text(encoding="utf-8"))}
    merged: dict[str, dict] = {}
    dup: list[str] = []
    bad: list[str] = []
    for p in sorted(d.glob("judge_shard[0-9]*.json")):
        # ⚠️ 别用 glob("judge_shard*.json")：它会把**判分输入** judge_shards.json
        # 也当成判定结果读进来（实测就发生了：多出 1 条 id=None、还报 5 个编码非法）。
        # 完整性校验拦住了它——这就是"先校验再写盘"的用处。
        rows = json.loads(p.read_text(encoding="utf-8"))
        for r in rows:
            iid = r.get("id")
            if iid in merged:
                dup.append(iid)
                continue
            for c in CODES:
                v = r.get(c)
                if not isinstance(v, int) or not 0 <= v <= 3:
                    bad.append(f"{p.name} {iid} 编码 {c} 非法：{v!r}")
            merged[iid] = r
        print(f"  {p.name}: {len(rows)} 条")

    missing = sorted(set(blind) - set(merged))
    extra = sorted(set(merged) - set(blind))
    print()
    print(f"盲评应有 {len(blind)} 条，合并到 {len(merged)} 条")
    if dup:
        print(f"  [!!] 重复判定：{dup}")
    if missing:
        print(f"  [!!] 缺判定：{missing}")
    if extra:
        print(f"  [!!] 多出来的 id：{extra}")
    if bad:
        for x in bad:
            print(f"  [!!] {x}")
    if dup or missing or extra or bad:
        print("\n✗ 拒绝写盘（先补齐/去重）")
        return 1

    out = [merged[i] for i in sorted(merged)]
    (d / "judge_result.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n已写 {d / 'judge_result.json'}（{len(out)} 条，完整性校验通过）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
