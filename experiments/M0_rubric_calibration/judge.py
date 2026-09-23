# -*- coding: utf-8 -*-
"""M0 评判器：对每个回答跑多个独立评判 pass。

评判 pass：
  sat_a / sat_b : satisfaction 框架（同一 prompt 跑两次 -> 测自一致性）
  def           : defect-detection 框架（问法相反、条目乱序 -> 近似跨评分者一致性）
  hol           : 整体质量 1-5 分，不带 rubric（-> 准则效度）

用法: python judge.py baseline.jsonl injected.jsonl
可断点续跑：verdicts.jsonl 中已有的 (response_id, judge) 会跳过。
"""
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from openai import OpenAI

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
KB = os.path.join(ROOT, 'knowledge_base', 'chunks.jsonl')

MODEL = 'deepseek-v4-flash'
BASE_URL = 'https://api.deepseek.com'
VERDICTS = os.path.join(HERE, 'verdicts.jsonl')

JUDGES = [
    ('sat_a', 'prompt_judge_satisfaction.txt', True),
    ('sat_b', 'prompt_judge_satisfaction.txt', True),
    ('def', 'prompt_judge_defect.txt', True),
    ('hol', 'prompt_holistic.txt', False),
]

ITEMS = ['A1', 'A2', 'A3', 'B1', 'B2', 'C1', 'C2', 'C3']


def load_key():
    key = os.environ.get('DEEPSEEK_API_KEY')
    if key:
        return key
    for line in open(os.path.join(ROOT, '.env'), encoding='utf-8'):
        if line.startswith('DEEPSEEK_API_KEY='):
            return line.split('=', 1)[1].strip()
    raise RuntimeError('DEEPSEEK_API_KEY not found')


def load_chunks():
    out = {}
    with open(KB, encoding='utf-8') as f:
        for line in f:
            if line.strip():
                c = json.loads(line)
                out[c['chunk_id']] = c
    return out


def build_material(chunk_ids, chunks):
    parts = []
    for cid in chunk_ids:
        c = chunks[cid]
        parts.append('--- %s (page %d) ---\n%s' % (cid, c['page'], c['text']))
    return '\n\n'.join(parts)


def load_responses(paths):
    out = []
    for p in paths:
        full = os.path.join(HERE, p)
        with open(full, encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    r = json.loads(line)
                    r['_source_file'] = p
                    r['response_id'] = r.get('variant_id') or r['item_id']
                    out.append(r)
    return out


def parse_json(text):
    text = text.strip()
    text = re.sub(r'^```(?:json)?\s*|\s*```$', '', text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r'\{[\s\S]*\}', text)
        if m:
            return json.loads(m.group(0))
        raise


def judge_one(client, judge_id, template, want_json, resp, material):
    # 用 replace 而非 str.format：prompt 里含 JSON 输出示例的字面大括号，
    # .format() 会把它们当成占位符并抛 KeyError。
    prompt = (template
              .replace('<<<MATERIAL>>>', material)
              .replace('<<<QUESTION>>>', resp['question'])
              .replace('<<<ANSWER>>>', resp['answer']))
    # 评判要比生成啰嗦（8 条判定 + 每条原文引用），且 thinking 的推理 token 也算在
    # max_tokens 里。预算给小了会静默返回空内容（finish_reason=length），而且恰好
    # 只在最长最复杂的回答上失败——那会造成系统性缺失，比慢更糟。
    # 因此：预算给足 + 截断就加大预算重试 + 推理档降到 medium（判据明确，不需要最高档）。
    base = dict(
        model=MODEL,
        messages=[{'role': 'user', 'content': prompt}],
        extra_body={'thinking': {'type': 'enabled'}, 'reasoning_effort': 'medium'},
    )
    if want_json:
        base['response_format'] = {'type': 'json_object'}

    max_tokens = 8192
    last = None
    for _ in range(4):
        kwargs = dict(base, max_tokens=max_tokens)
        try:
            r = client.chat.completions.create(**kwargs)
            ch = r.choices[0]
            raw = (ch.message.content or '').strip()
            if not raw or ch.finish_reason == 'length':
                last = 'truncated/empty (finish=%s, len=%d, budget=%d)' % (
                    ch.finish_reason, len(raw), max_tokens)
                max_tokens = int(max_tokens * 1.5)
                continue
            return parse_json(raw), raw, ch.finish_reason
        except json.JSONDecodeError as e:
            last = 'JSONDecodeError: %s' % str(e)[:160]
            time.sleep(1)
        except Exception as e:  # noqa: BLE001
            last = '%s: %s' % (type(e).__name__, str(e)[:200])
            time.sleep(2)
    raise RuntimeError(last)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='*', default=['baseline.jsonl', 'injected.jsonl'])
    ap.add_argument('--judges', default='sat_a,sat_b,def,hol',
                    help='要跑哪些评判 pass（sat_a,sat_b,def,hol）。'
                         '去掉 sat_b 可省 16 次调用（只影响自一致性检查）')
    ap.add_argument('--workers', type=int, default=8)
    args = ap.parse_args()

    want = set(args.judges.split(','))
    judges = [j for j in JUDGES if j[0] in want]

    responses = load_responses(args.files)
    chunks = load_chunks()

    done = set()
    if os.path.exists(VERDICTS):
        for line in open(VERDICTS, encoding='utf-8'):
            if line.strip():
                v = json.loads(line)
                done.add((v['response_id'], v['judge']))
    todo = [(j, r) for j in judges for r in responses if (r['response_id'], j[0]) not in done]
    print('responses=%d  judges=%s  todo=%d  workers=%d'
          % (len(responses), [j[0] for j in judges], len(todo), args.workers), flush=True)

    client = OpenAI(api_key=load_key(), base_url=BASE_URL, timeout=240.0)
    templates = {jid: open(os.path.join(HERE, fn), encoding='utf-8').read() for jid, fn, _ in judges}

    def work(task):
        (jid, fn, want_json), resp = task
        material = build_material(resp['chunk_ids'], chunks)
        t0 = time.time()
        try:
            data, raw, finish = judge_one(client, jid, templates[jid], want_json, resp, material)
        except Exception as e:  # noqa: BLE001
            print('FAIL %s/%s  %s' % (resp['response_id'], jid, str(e)[:160]), flush=True)
            return
        dt = time.time() - t0
        rec = {
            'response_id': resp['response_id'],
            'substrate': resp['item_id'],
            'inject_item': resp.get('inject_item'),
            'judge': jid,
            'finish_reason': finish,
            'elapsed_s': round(dt, 1),
            'data': data,
        }
        with open(VERDICTS, 'a', encoding='utf-8') as f:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        if jid == 'hol':
            print('ok %-12s %-6s %5.0fs overall=%s' % (resp['response_id'], jid, dt, data.get('overall')), flush=True)
        else:
            nf = [k for k in ITEMS if data.get('items', {}).get(k, {}).get('verdict') == 'fail']
            print('ok %-12s %-6s %5.0fs type=%s gate=%s fails=%s'
                  % (resp['response_id'], jid, dt, data.get('response_type'),
                     data.get('gate', {}).get('correctness'), ','.join(nf) or '-'), flush=True)

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        list(ex.map(work, todo))
    print('done ->', VERDICTS, flush=True)


if __name__ == '__main__':
    main()
