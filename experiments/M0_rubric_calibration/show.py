# -*- coding: utf-8 -*-
"""打印某文件里的回答，便于人工阅读。

用法: python show.py baseline.jsonl [q1,q2] [--width 100]
"""
import json
import os
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(HERE, sys.argv[1])
only = None
width = 110
for a in sys.argv[2:]:
    if a.startswith('--width'):
        width = int(a.split('=')[1])
    else:
        only = set(a.split(','))

for line in open(path, encoding='utf-8'):
    if not line.strip():
        continue
    r = json.loads(line)
    if only and r.get('item_id') not in only and r.get('variant_id') not in only:
        continue
    print('=' * width)
    print('%s | %s' % (r.get('variant_id', r.get('item_id')), r.get('topic', '')))
    print('Q: %s' % r.get('question', ''))
    if r.get('inject_item'):
        print('INJECT: %s  (%s)' % (r['inject_item'], r.get('inject_note', '')))
    print('-' * width)
    print(textwrap.fill(r['answer'], width=width, replace_whitespace=False))
    print()
