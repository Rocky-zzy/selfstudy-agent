# -*- coding: utf-8 -*-
r"""把盲评输入切成**判分分片**，并把课件原文按页去重。

为什么必须去重：第一版给每条样本都附上它依据的课件原文，
40 段共 **79 万字符**，而同一问的两段（X/Y）用的是**同一批页**——
等于同样一页原文被附了 2 次，跨问还有更多重复。白烧一大截 token。

分片规则：每个评判者拿 5 段（2–3 问），**原文按块去重后只出现一次**，
评判者按块 id 去查。这样每片约 4 万字符，8 片并行。

产物：`<batch>/judge_shards.json`（**仍然没有 condition**，盲测不破）
"""
from __future__ import annotations

import argparse
import json
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
    ap.add_argument("--per-shard", type=int, default=5)
    args = ap.parse_args()

    d = ROOT / "data" / "mqi" / "batches" / args.batch
    blind = json.loads((d / "blind.json").read_text(encoding="utf-8"))
    key = {x["id"]: x for x in json.loads((d / "_key.json").read_text(encoding="utf-8"))}

    # 页正文缓存（按 material 分别读，避免把两套知识库的 chunk_id 混在一起）
    text_of: dict[str, dict[str, str]] = {}
    for mat, kb in MAT_KB.items():
        if not kb.exists():
            continue
        m: dict[str, str] = {}
        for line in kb.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                m[r["chunk_id"]] = r.get("text") or ""
        text_of[mat] = m

    # 按问题分组（同一问的 X/Y 共用原文）
    by_q: dict[str, list[dict]] = {}
    for it in blind:
        by_q.setdefault(it["id"][:3], []).append(it)

    shards, cur, cur_chars = [], [], 0
    for qid in sorted(by_q):
        grp = by_q[qid]
        # 这一问用到的页 = 从 sources 里抠出 <<<PAGE id | ...>>> 标记
        pages = []
        for it in grp[:1]:
            for line in it["sources"].splitlines():
                if line.startswith("<<<PAGE "):
                    pages.append(line.split()[1])
        mat = key[grp[0]["id"]]["material"]
        cur.append({
            "qid": qid,
            "question": grp[0]["question"],
            "teaching": grp[0]["teaching"],
            "pages": pages,
            "items": [{"id": it["id"], "text": it["text"]} for it in grp],
        })
        n = sum(len(it["text"]) for it in grp)
        cur_chars += n
        if sum(len(x["items"]) for x in cur) >= args.per_shard:
            shards.append(cur)
            cur, cur_chars = [], 0
    if cur:
        shards.append(cur)

    out = []
    for si, sh in enumerate(shards, 1):
        pages: dict[str, str] = {}
        for q in sh:
            for pid in q["pages"]:
                if pid not in pages:
                    pages[pid] = text_of.get(
                        key[q["items"][0]["id"]]["material"], {}).get(pid, "")
        out.append({
            "shard": si,
            "questions": [{"qid": q["qid"], "question": q["question"],
                           "teaching": q["teaching"], "pages": q["pages"]} for q in sh],
            "courseware": pages,
            "items": [it for q in sh for it in q["items"]],
        })

    p = d / "judge_shards.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    tot = sum(len(json.dumps(s, ensure_ascii=False)) for s in out)
    raw = sum(len(it["text"]) + len(it["sources"]) for it in blind)
    print(f"{len(shards)} 片 → {p}")
    for s in out:
        chars = sum(len(it["text"]) for it in s["items"]) + sum(
            len(v) for v in s["courseware"].values())
        print(f"  片 {s['shard']}: {len(s['items'])} 段 / {len(s['courseware'])} 页原文 / "
              f"{chars} 字符（{len(s['questions'])} 问）")
    print(f"总计 {tot} 字符；若不去重是 {raw} 字符 → 省 {1 - tot / raw:.0%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
