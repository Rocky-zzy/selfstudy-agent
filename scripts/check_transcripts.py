# -*- coding: utf-8 -*-
"""视觉转写质量自检：找漏页、异常短页、拒答/免责话术。"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TR = os.path.join(ROOT, 'knowledge_base', 'transcripts')

REFUSAL = re.compile(
    r"(as an ai|i'?m sorry|i cannot|i can'?t (assist|help|transcribe)|unable to (read|transcribe)"
    r"|sorry,? (but )?i)", re.I)

rows = []
for fn in sorted(os.listdir(TR)):
    if not fn.endswith('.md'):
        continue
    body = open(os.path.join(TR, fn), encoding='utf-8').read()
    body = re.sub(r'^<!--.*?-->\s*', '', body, flags=re.S).strip()
    rows.append((fn, len(body), body))

print('transcripts: %d' % len(rows))
if not rows:
    raise SystemExit(0)

lens = sorted(r[1] for r in rows)
print('chars  min=%d  p25=%d  median=%d  max=%d  total=%d'
      % (lens[0], lens[len(lens) // 4], lens[len(lens) // 2], lens[-1], sum(lens)))

short = [r for r in rows if r[1] < 200]
if short:
    print('\nSHORT PAGES (<200 chars) — 逐个人工确认是否真的是空白/标题页:')
    for fn, n, body in short:
        print('  %s  (%d chars)  %s' % (fn, n, body[:90].replace('\n', ' / ')))

hits = [(fn, REFUSAL.search(body).group(0)) for fn, _n, body in rows if REFUSAL.search(body)]
if hits:
    print('\nREFUSAL-LIKE TEXT — 需重跑:')
    for fn, m in hits:
        print('  %s  -> %r' % (fn, m))
else:
    print('\nno refusal-like text found.')
