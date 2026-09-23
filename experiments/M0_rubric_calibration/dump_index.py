# -*- coding: utf-8 -*-
"""打印知识库 chunk 索引（id + 首行摘要），用于挑选 M0 知识点。"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KB = os.path.join(ROOT, 'knowledge_base', 'chunks.jsonl')

want = [w.upper() for w in sys.argv[1:]] or None
rows = [json.loads(l) for l in open(KB, encoding='utf-8') if l.strip()]

for c in rows:
    if want and c['lecture'] not in want:
        continue
    head = ' / '.join(x.strip() for x in c['text'].split('\n') if x.strip())[:150]
    print('%-9s %-4d %s' % (c['chunk_id'], c['char_count'], head))
