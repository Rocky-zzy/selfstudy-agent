# -*- coding: utf-8 -*-
r"""核对"生成时的上下文长度"和"现在重算的"差在哪。

用途：`make_mqi_blind.py` 会给评判者附上课件原文，附之前必须确认
      附的确实是当时那批页（否则评判者拿到的证据与讲解的来源不一致，
      判出来的编码 12 不可信）。这里把差值拆开：
      ctx（检索页正文）+ 注入块 + 包裹标记 vs. 生成时记录的 ctx_chars。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import graph_inject as gi  # noqa: E402
from retrieval import build_context, load_chunks, search  # noqa: E402

batch = sys.argv[1] if len(sys.argv) > 1 else "r4"
rows = json.loads((ROOT / "data" / "mqi" / "batches" / batch / "samples.json")
                  .read_text(encoding="utf-8"))
chunks = load_chunks(ROOT / "data" / "rosen" / "ch1" / "chunks.jsonl")
g = gi.load_graph("rosen-ch1")

print(f"{'问':5}{'选中页':>6}{'ctx':>8}{'注入':>7}{'合计':>8}{'生成时':>8}{'差':>7}")
for i, s in enumerate(rows):
    lec, q = s["lecture"], s["question"]
    pool = [c for c in chunks if c.lecture == lec]
    pc = sum(len(c.text or "") for c in pool)
    sel = search(q, chunks, lecture=lec, top_k=4, bridge=True,
                 whole_lecture=pc <= 20000, whole_lecture_char_limit=20000,
                 page_range=None)
    ctx = build_context(sel)
    inj, _ids = gi.build_injection(g, [c.chunk_id for c in sel], q)
    total = len(ctx) + len(inj) + 2
    rec = s.get("ctx_chars") or 0
    print(f"q{i:02d}  {len(sel):>6}{len(ctx):>8}{len(inj):>7}{total:>8}{rec:>8}{rec - total:>+7}")
