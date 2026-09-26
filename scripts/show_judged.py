# -*- coding: utf-8 -*-
r"""把某条判定的**原文片段**打出来，用于人工核对判分是否成立。

用法：
    python scripts/show_judged.py --batch r4 --id q07Y --grep 唯一
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    ap.add_argument("--id", required=True)
    ap.add_argument("--grep", default="")
    ap.add_argument("--width", type=int, default=700)
    args = ap.parse_args()

    d = ROOT / "data" / "mqi" / "batches" / args.batch
    blind = {x["id"]: x for x in json.loads((d / "blind.json").read_text(encoding="utf-8"))}
    key = {x["id"]: x for x in json.loads((d / "_key.json").read_text(encoding="utf-8"))}
    judge = {x["id"]: x for x in json.loads((d / "judge_result.json").read_text(encoding="utf-8"))}
    it, k, j = blind[args.id], key[args.id], judge[args.id]
    print(f"=== {args.id}  真实条件={k['condition']}  {k['lecture']}  {k['teaching']}")
    print(f"问题：{k['question']}")
    print(f"判定：3={j.get('3')} 4={j.get('4')} 12={j.get('12')} 13={j.get('13')} 14={j.get('14')}")
    print(f"理由：{j.get('note')}")
    print(f"文本 {len(it['text'])} 字符；来源页 {len(it['sources'])} 字符")
    print("-" * 78)
    if args.grep:
        pos = 0
        hit = 0
        while True:
            i = it["text"].find(args.grep, pos)
            if i < 0:
                break
            hit += 1
            print(f"[命中 {hit}] …{it['text'][max(0, i - args.width // 2):i + args.width]}…")
            print()
            pos = i + len(args.grep)
        if not hit:
            print(f"（文本里找不到 {args.grep!r}）")
    else:
        print(it["text"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
