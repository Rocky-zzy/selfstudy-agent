# -*- coding: utf-8 -*-
r"""构建**裸 LLM vs 最终优化版**的盲判分片。

为什么不复用 r4 那批分片：那批里有 baseline 的 40 段，而这一轮要回答的问题只有一个——
"**最终版比裸 LLM 好多少**"。把 baseline 掺进来会：
  ① 多花一倍判分 token；② 让均值落在三个条件的混合上，反而不清爽。
所以只取 optimized 的 20 段 + 新生成的 raw 20 段，**X/Y 随机重标**（评判者不知道哪边是哪边）。

课件原文按页去重（`docs/00` M17）：20 问共用约 60 页，重复附一次就白烧一倍。

产物：`<batch>/judge_raw_shards.json`
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAT_KB = {
    "kb": ROOT / "knowledge_base" / "chunks.jsonl",
    "rosen-ch1": ROOT / "data" / "rosen" / "ch1" / "chunks.jsonl",
}
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    ap.add_argument("--per-shard", type=int, default=6)
    ap.add_argument("--seed", type=int, default=20260926)
    args = ap.parse_args()

    random.seed(args.seed)
    d = ROOT / "data" / "mqi" / "batches" / args.batch
    samples = json.loads((d / "samples.json").read_text(encoding="utf-8"))
    raw = json.loads((d / "raw.json").read_text(encoding="utf-8"))
    blind = {x["id"]: x for x in json.loads((d / "blind.json").read_text(encoding="utf-8"))}
    key = {x["id"]: x for x in json.loads((d / "_key.json").read_text(encoding="utf-8"))}

    # 每问取它的 optimized 那一段（盲评里的 X 或 Y）
    opt_of: dict[str, str] = {}
    for iid, k in key.items():
        if k["condition"] == "optimized":
            opt_of[k["question"]] = iid
    raw_of = {r["question"]: r for r in raw}
    missing = [q for q in opt_of if q not in raw_of]
    if missing:
        print(f"[!!] 有 {len(missing)} 问缺裸 LLM 答案：{[m[:30] for m in missing]}")
        return 1

    text_of: dict[str, dict[str, str]] = {}
    for mat, kb in MAT_KB.items():
        if kb.exists():
            m = {}
            for line in kb.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    r = json.loads(line)
                    m[r["chunk_id"]] = r.get("text") or ""
            text_of[mat] = m

    qs = sorted(opt_of)
    shards, cur = [], []
    for i, q in enumerate(qs):
        oid = opt_of[q]
        r = raw_of[q]
        # 这一问用到的页（从盲评条目的 sources 里抠标记；与 raw 的 citations 应一致）
        pages = [ln.split()[1] for ln in blind[oid]["sources"].splitlines()
                 if ln.startswith("<<<PAGE ")]
        assert set(pages) == set(r["citations"]), f"{q[:20]} 选页不一致"
        pair = [("optimized", blind[oid]["text"]), ("raw", r["text"])]
        random.shuffle(pair)
        items = [{"id": f"p{i:02d}{'X' if j == 0 else 'Y'}", "text": t}
                 for j, (_c, t) in enumerate(pair)]
        cur.append({"question": q, "teaching": key[oid]["teaching"],
                    "lecture": key[oid]["lecture"], "pages": pages, "items": items,
                    "_map": {items[j]["id"]: pair[j][0] for j in range(2)}})
        if sum(len(x["items"]) for x in cur) >= args.per_shard:
            shards.append(cur)
            cur = []
    if cur:
        shards.append(cur)

    out, mapping = [], {}
    for si, sh in enumerate(shards, 1):
        pages: dict[str, str] = {}
        for q in sh:
            for pid in q["pages"]:
                if pid not in pages:
                    pages[pid] = text_of["rosen-ch1" if pid.startswith("rosen") else "kb"].get(pid, "")
            for it in q["items"]:
                mapping[it["id"]] = q["_map"][it["id"]]
        out.append({
            "shard": si,
            "questions": [{"question": q["question"], "teaching": q["teaching"],
                           "lecture": q["lecture"], "pages": q["pages"]} for q in sh],
            "courseware": pages,
            "items": [{"id": it["id"], "question": q["question"], "text": it["text"]}
                      for q in sh for it in q["items"]],
        })
        for q in sh:
            q.pop("_map", None)

    (d / "judge_raw_shards.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    # 答案键单独存：评判者拿不到，我核对用
    (d / "_raw_map.json").write_text(
        json.dumps(mapping, ensure_ascii=False, indent=1), encoding="utf-8")

    chars = sum(len(it["text"]) for s in out for it in s["items"]) + sum(
        len(v) for s in out for v in s["courseware"].values())
    print(f"{len(out)} 片 / {sum(len(s['items']) for s in out)} 段（裸 {len(raw)} vs 最终版 {len(opt_of)}）")
    for s in out:
        print(f"  片 {s['shard']}: {len(s['items'])} 段 / {len(s['courseware'])} 页原文")
    print(f"总字符 {chars}（原文已按页去重）")
    print(f"答案键 -> {d / '_raw_map.json'}（**不要给评判者**）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
