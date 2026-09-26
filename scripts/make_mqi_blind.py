# -*- coding: utf-8 -*-
r"""导出给盲评判分用的输入，并**附上判分需要的课件原文**。

为什么不能只给讲解文本：
    编码 12（数学内容错误）要求判"是不是与课件不符、有没有把概念等同"。
    不给原文，评判者只能凭自己的数学记忆判——那就不是"对着材料判"，
    而是"对着评判者的先验判"，结论不可复核（`docs/12` §3.2 就是靠原文才查出误伤）。

检索是确定性的（同一问 + 同一节 → 同一批页），所以这里**重算**引用页，
不需要重跑模型；同时也顺手校验"重算的页数"和生成时记录的 ctx 是否自洽。

产物：
    <batch>/blind.json    给评判者：id / question / teaching / text / sources
    <batch>/_key.json     答案键（不要给评判者）
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from retrieval import build_context, load_chunks, search  # noqa: E402

MAT_KB = {
    "kb": ROOT / "knowledge_base" / "chunks.jsonl",
    "rosen-ch1": ROOT / "data" / "rosen" / "ch1" / "chunks.jsonl",
}
WHOLE_LIMIT = 20000


def cited_pages(sample: dict, chunks: list) -> list:
    """重算这一问当时选中的页（与 /api/ask 同一套参数）。"""
    lec, q = sample["lecture"], sample["question"]
    pool = [c for c in chunks if c.lecture == lec]
    pool_chars = sum(len(c.text or "") for c in pool)
    effective_whole = pool_chars <= WHOLE_LIMIT
    return search(q, chunks, lecture=lec, top_k=4, bridge=True,
                  whole_lecture=effective_whole,
                  whole_lecture_char_limit=WHOLE_LIMIT, page_range=None)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    ap.add_argument("--no-sources", action="store_true",
                    help="不附课件原文（只做格式检查时用）")
    args = ap.parse_args()

    d = ROOT / "data" / "mqi" / "batches" / args.batch
    rows = json.loads((d / "samples.json").read_text(encoding="utf-8"))
    usable = [r for r in rows
              if all((r["answers"][s]["text"] or "").strip() for s in r["answers"])]
    dropped = len(rows) - len(usable)
    if dropped:
        print(f"⚠️ 跳过 {dropped} 个空答案样本（生成失败）：")
        for r in rows:
            if not all((r["answers"][s]["text"] or "").strip() for s in r["answers"]):
                print(f"     {r.get('lecture')} {r['question'][:44]}")

    cache: dict[str, list] = {}
    items, key = [], []
    for i, r in enumerate(usable):
        mat = r.get("material", "kb")
        if mat not in cache:
            cache[mat] = load_chunks(MAT_KB[mat])
        sel = cited_pages(r, cache[mat])
        ctx = build_context(sel)
        src_block = ("" if args.no_sources else
                     "\n\n".join(f"<<<PAGE {c.chunk_id} | page {c.page}>>>\n{c.text}"
                                 for c in sel))
        cond_of = r["conditions"]
        slots = list(cond_of)
        random.shuffle(slots)
        for j, slot in enumerate(slots):
            new_slot = "X" if j == 0 else "Y"
            iid = f"q{i:02d}{new_slot}"
            text = r["answers"][slot]["text"]
            items.append({
                "id": iid,
                "question": r["question"],
                "teaching": r["teaching"],
                "text": text,
                "sources": src_block,
                # 哈希：跨轮复用时用它证明"是同一段文本"（docs/00 M12）
                "sha": hashlib.sha256((text or "").encode("utf-8")).hexdigest()[:16],
            })
            key.append({"id": iid, "condition": cond_of[slot], "sha": items[-1]["sha"],
                        "question": r["question"], "teaching": r["teaching"],
                        "lecture": r.get("lecture"), "material": mat,
                        "ctx_chars": r.get("ctx_chars"), "recomputed_ctx": len(ctx)})
        print(f"  q{i:02d} {r.get('lecture')} {r['teaching']:<8} "
              f"{len(sel)} 页原文 / {len(ctx)} 字符（生成时 {r.get('ctx_chars')}）")

    (d / "blind.json").write_text(json.dumps(items, ensure_ascii=False, indent=1),
                                  encoding="utf-8")
    (d / "_key.json").write_text(json.dumps(key, ensure_ascii=False, indent=1),
                                 encoding="utf-8")
    print(f"\n导出 {len(items)} 条盲评输入（{len(usable)} 问 × 2）-> {d / 'blind.json'}")
    print("字段：id / question / teaching / text / sources / sha"
          "——**无 condition、无 user_score**")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
