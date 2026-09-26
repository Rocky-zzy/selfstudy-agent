# -*- coding: utf-8 -*-
r"""跑**裸 LLM 条件（raw）**：只给课件原文 + 问题，零约束。

为什么要有这一条（用户 2026-09-26）：
    "优于同款 LLM 冷启动"这句话要成立，对照必须是**真正的裸 LLM**。
    之前的 `baseline` 其实也带着我们的优化（范围约束、输出格式、术语加注、
    教学骨架、知识结构图），拿它当"冷启动"是拿错了对照。

**唯一变量**：系统指令。
    · 检索器、课件原文的范围与拼接、模型、temperature(0.3)、max_tokens(4000) 全部与 r4 相同；
    · 课件原文的选页**直接复用 r4 那一批**（按 topic/节 + 同一 top_k、同一整节降级规则重算），
      所以两边的"看到的东西"逐字一致——差异只可能来自 prompt。

产物：`data/mqi/batches/<batch>/raw.json`
    [{question, teaching, lecture, system_prompt, text, chars, finish, truncated}]

用法：
    python scripts/make_mqi_raw.py --batch r4 --material rosen-ch1            # 全量
    python scripts/make_mqi_raw.py --batch r4 --material rosen-ch1 --limit 1  # 先跑 1 条走通
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from demo_app import load_dotenv  # noqa: E402
from generator import GenConfig, generate, system_prompt_for  # noqa: E402
from retrieval import build_context, load_chunks, search  # noqa: E402

MAT_KB = {
    "kb": ROOT / "knowledge_base" / "chunks.jsonl",
    "rosen-ch1": ROOT / "data" / "rosen" / "ch1" / "chunks.jsonl",
}
WHOLE_LIMIT = 20000
TOP_K = 4


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    ap.add_argument("--material", default="rosen-ch1")
    ap.add_argument("--source-batch", default=None,
                    help="从哪个批次取问题集与选页（默认同 --batch）")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    load_dotenv(ROOT / ".env")
    cfg = GenConfig.from_env()
    if not cfg.api_key:
        print("没有 DEEPSEEK_API_KEY")
        return 2

    src = ROOT / "data" / "mqi" / "batches" / (args.source_batch or args.batch)
    rows = json.loads((src / "samples.json").read_text(encoding="utf-8"))
    rows = [r for r in rows if r.get("material", "kb") == args.material]
    if args.limit:
        rows = rows[:args.limit]

    chunks = load_chunks(MAT_KB[args.material])
    print(f"裸 LLM 条件：{len(rows)} 问 / 素材 {args.material} / 模型 {cfg.model} "
          f"/ temperature {cfg.temperature} / max_tokens {cfg.max_tokens}")
    print(f"system prompt（**就这一句**）：{system_prompt_for('raw')!r}")
    print("=" * 88)

    out = []
    t0 = time.time()
    for i, r in enumerate(rows, 1):
        lec, q = r["lecture"], r["question"]
        pool = [c for c in chunks if c.lecture == lec]
        pool_chars = sum(len(c.text or "") for c in pool)
        sel = search(q, chunks, lecture=lec, top_k=TOP_K, bridge=True,
                     whole_lecture=pool_chars <= WHOLE_LIMIT,
                     whole_lecture_char_limit=WHOLE_LIMIT, page_range=None)
        ctx = build_context(sel)
        res = generate("raw", ctx, q, cfg=cfg)
        if res.error or not (res.text or "").strip():
            print(f"[{i}/{len(rows)}] FAIL {lec} {q[:30]} -> {res.error}")
            continue
        out.append({
            "question": q, "teaching": r["teaching"], "lecture": lec,
            "material": args.material,
            "citations": [c.chunk_id for c in sel],
            "ctx_chars": len(ctx),
            "system_prompt": res.system_prompt,
            "text": res.text, "chars": len(res.text),
            "finish": res.finish_reason, "truncated": res.truncated,
        })
        print(f"[{i}/{len(rows)}] {lec} {r['teaching']:<8} {q[:26]:<28} "
              f"{len(res.text):>5}字 finish={res.finish_reason} "
              f"ctx={len(ctx)}（与最终版同一批 {len(sel)} 页）")

    p = src / "raw.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print()
    print(f"写入 {p}（{len(out)} 条，耗时 {time.time() - t0:.0f}s）")
    tr = [x for x in out if x["truncated"]]
    if tr:
        print(f"⚠️ {len(tr)} 条被截断")
    ln = [x["chars"] for x in out]
    print(f"长度：最短 {min(ln)} / 中位 {sorted(ln)[len(ln) // 2]} / 最长 {max(ln)} 字符")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
