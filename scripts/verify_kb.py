# -*- coding: utf-8 -*-
"""知识库结构自检：id 唯一、无空文本、字段完整、与 manifest 一致。"""
import json
import os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB = os.path.join(ROOT, 'knowledge_base')

chunks = [json.loads(l) for l in open(os.path.join(KB, 'chunks.jsonl'), encoding='utf-8') if l.strip()]
man = json.load(open(os.path.join(KB, 'manifest.json'), encoding='utf-8'))

ids = [c['chunk_id'] for c in chunks]
print('chunks=%d  unique_ids=%d  manifest.total_chunks=%d'
      % (len(chunks), len(set(ids)), man['total_chunks']))

FIELDS = {'chunk_id', 'source_file', 'lecture', 'lecture_title', 'page', 'text', 'char_count', 'extraction'}
bad_fields = [c['chunk_id'] for c in chunks if set(c) != FIELDS]
print('field mismatch: %d' % len(bad_fields))

empty = [c['chunk_id'] for c in chunks if not c['text'].strip()]
print('empty text: %d' % len(empty))

bad_len = [c['chunk_id'] for c in chunks if c['char_count'] != len(c['text'])]
print('char_count mismatch: %d' % len(bad_len))

dupe = [k for k, v in Counter(ids).items() if v > 1]
print('duplicate ids: %s' % (dupe or 'none'))

print('by extraction: %s' % dict(Counter(c['extraction'] for c in chunks)))
print('chars by extraction: %s' % man['total_chars_by_extraction'])

print('\nchunks per source:')
def label(c):
    return c['lecture'] if c['lecture'] else os.path.basename(c['source_file'])[:34]

per = Counter(label(c) for c in chunks)
order = sorted(per.items(), key=lambda kv: (kv[0].startswith('L') is False, kv[0]))
for name, n in order:
    title = next((c['lecture_title'] for c in chunks if label(c) == name), '')
    print('  %-36s %3d   %s' % (name, n, ('' if name == title else title[:50])))

print('\nsample chunk (l09-p02):')
s = next((c for c in chunks if c['chunk_id'] == 'l09-p02'), None)
if s:
    print(json.dumps({k: v for k, v in s.items() if k != 'text'}, ensure_ascii=False, indent=2))
    print('text head: %s' % s['text'][:220].replace('\n', ' / '))

print('\nblank_pages=%s' % man.get('blank_pages'))
print('missing_transcripts=%s' % (man.get('missing_transcripts') or 'none'))
