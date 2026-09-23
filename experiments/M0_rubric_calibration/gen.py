# -*- coding: utf-8 -*-
"""M0 回答生成器：按指定 prompt 模板 + 知识库材料生成回答。

用法：
    python gen.py --prompt prompt_baseline.txt --out baseline.jsonl
    python gen.py --prompt prompt_baseline.txt --out baseline.jsonl --only q3

可断点续跑：已存在于 --out 中的 item_id 会跳过。

与 src/llm_client.py 的差别（刻意）：本脚本自带 API 调用，因为
- src 的 MAX_TOKENS=4096 把 thinking 的推理 token 也算在内，推理长时输出会被静默截断；
- 这里提高预算并**检测 finish_reason == "length"**，截断就自动加大预算重试，绝不把半截文本当样本。
"""
import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from openai import OpenAI

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

MODEL = 'deepseek-v4-flash'
BASE_URL = 'https://api.deepseek.com'
KB = os.path.join(ROOT, 'knowledge_base', 'chunks.jsonl')


def load_key():
    key = os.environ.get('DEEPSEEK_API_KEY')
    if key:
        return key
    for line in open(os.path.join(ROOT, '.env'), encoding='utf-8'):
        if line.startswith('DEEPSEEK_API_KEY='):
            return line.split('=', 1)[1].strip()
    raise RuntimeError('DEEPSEEK_API_KEY not found')


def load_items():
    with open(os.path.join(HERE, 'items.json'), encoding='utf-8') as f:
        return json.load(f)['items']


def load_chunks():
    out = {}
    with open(KB, encoding='utf-8') as f:
        for line in f:
            if line.strip():
                c = json.loads(line)
                out[c['chunk_id']] = c
    return out


def build_material(item, chunks):
    parts = []
    for cid in item['chunk_ids']:
        c = chunks[cid]
        parts.append('--- %s (page %d) ---\n%s' % (cid, c['page'], c['text']))
    return '\n\n'.join(parts)


def call(client, prompt, max_tokens=8192):
    """返回 (text, finish_reason)；截断则加大预算重试。"""
    last = None
    for _ in range(4):
        r = client.chat.completions.create(
            model=MODEL,
            max_tokens=max_tokens,
            messages=[{'role': 'user', 'content': prompt}],
            extra_body={'thinking': {'type': 'enabled'}, 'reasoning_effort': 'high'},
        )
        ch = r.choices[0]
        txt = (ch.message.content or '').strip()
        if txt and ch.finish_reason != 'length':
            return txt, ch.finish_reason
        last = 'finish_reason=%s len=%d' % (ch.finish_reason, len(txt))
        max_tokens = int(max_tokens * 1.6)
    raise RuntimeError('generation failed (truncated or empty): %s' % last)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prompt', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--only', default=None)
    ap.add_argument('--workers', type=int, default=4)
    args = ap.parse_args()

    template = open(os.path.join(HERE, args.prompt), encoding='utf-8').read()
    items = load_items()
    if args.only:
        keep = set(args.only.split(','))
        items = [i for i in items if i['id'] in keep]
    chunks = load_chunks()

    out_path = os.path.join(HERE, args.out)
    done = set()
    if os.path.exists(out_path):
        for line in open(out_path, encoding='utf-8'):
            if line.strip():
                done.add(json.loads(line)['item_id'])
    todo = [i for i in items if i['id'] not in done]
    print('items=%d  already=%d  todo=%d' % (len(items), len(done), len(todo)), flush=True)

    client = OpenAI(api_key=load_key(), base_url=BASE_URL, timeout=240.0)

    def work(item):
        material = build_material(item, chunks)
        prompt = template.format(material=material, question=item['question'])
        answer, finish = call(client, prompt)
        rec = {
            'item_id': item['id'],
            'topic': item['topic'],
            'expected_type': item['expected_type'],
            'chunk_ids': item['chunk_ids'],
            'question': item['question'],
            'prompt_file': args.prompt,
            'model': MODEL,
            'thinking': 'enabled', 'reasoning_effort': 'high',
            'finish_reason': finish,
            'material_chars': len(material),
            'answer_chars': len(answer),
            'answer': answer,
            'ts': time.strftime('%Y-%m-%dT%H:%M:%S'),
        }
        with open(out_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        print('ok %s  %d chars  finish=%s' % (item['id'], len(answer), finish), flush=True)

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        list(ex.map(work, todo))
    print('done ->', out_path, flush=True)


if __name__ == '__main__':
    main()
