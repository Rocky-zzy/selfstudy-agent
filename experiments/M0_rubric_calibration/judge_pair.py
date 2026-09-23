# -*- coding: utf-8 -*-
"""M0 成对偏好评判（替换失效的整体 1-5 分准则）。

背景：首轮的 holistic 绝对评分把 16 个回答**全部**打成 5 分（含 8 个被注入缺陷的版本），
零方差 -> 无法作为准则效度的参照。这正是 docs/04 §4.1 预告的 fluency illusion：
话说得流畅，整体印象就好，缺陷被淹没。

成对比较对这类偏差鲁棒得多：同一份材料的两个版本，问哪个更好、另一个差在哪。
每个"回答对"只看一次，(substrate, injected) 的左右顺序随机。

用法: python judge_pair.py
输出: pair_verdicts.jsonl
"""
import json
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor

from openai import OpenAI

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
KB = os.path.join(ROOT, 'knowledge_base', 'chunks.jsonl')
OUT = os.path.join(HERE, 'pair_verdicts.jsonl')

MODEL = 'deepseek-v4-flash'
BASE_URL = 'https://api.deepseek.com'
random.seed(7)

PROMPT = """You are an experienced university tutor who has taught this graduate course many times. A student asked a question, and two teaching assistants each wrote an answer. Decide which answer is the BETTER explanation for this student.

Do NOT use any checklist. Judge as a teacher would: which answer would actually help this student understand?

IMPORTANT: The two answers are largely the same content. One of them has one specific defect introduced. Look carefully for a concrete difference — a missing step, a missing definition, a repetition, an out-of-scope digression, a missing reason, or missing structure. If you cannot find any difference, say so; that is a valid answer.

Course material excerpt (for reference): inside <material>...</material>
Student's question: inside <question>...</question>

<answer_left>
<<<LEFT>>>
</answer_left>

<answer_right>
<<<RIGHT>>>
</answer_right>

OUTPUT — a single JSON object, no other text:
{
  "better": "left|right|tie",
  "difference": "the concrete difference you found, quoting the offending span; or 'none found'",
  "worse_defect": "one short phrase naming what is wrong with the worse answer, or 'none'",
  "confidence": "high|medium|low"
}

<material>
<<<MATERIAL>>>
</material>

<question>
<<<QUESTION>>>
</question>
"""


def load_key():
    key = os.environ.get('DEEPSEEK_API_KEY')
    if key:
        return key
    for line in open(os.path.join(ROOT, '.env'), encoding='utf-8'):
        if line.startswith('DEEPSEEK_API_KEY='):
            return line.split('=', 1)[1].strip()
    raise RuntimeError('DEEPSEEK_API_KEY not found')


def load_jsonl(name):
    out = {}
    with open(os.path.join(HERE, name), encoding='utf-8') as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                out[r.get('variant_id') or r['item_id']] = r
    return out


def load_chunks():
    out = {}
    with open(KB, encoding='utf-8') as f:
        for line in f:
            if line.strip():
                c = json.loads(line)
                out[c['chunk_id']] = c
    return out


def main():
    base = load_jsonl('baseline.jsonl')
    inj = load_jsonl('injected.jsonl')
    chunks = load_chunks()
    client = OpenAI(api_key=load_key(), base_url=BASE_URL, timeout=240.0)

    done = set()
    if os.path.exists(OUT):
        for line in open(OUT, encoding='utf-8'):
            if line.strip():
                done.add(json.loads(line)['pair_id'])

    pairs = []
    for vid, rec in sorted(inj.items()):
        pid = vid
        if pid in done:
            continue
        sub = base[rec['item_id']]
        if random.random() < 0.5:
            left, right, left_is = sub['answer'], rec['answer'], 'substrate'
        else:
            left, right, left_is = rec['answer'], sub['answer'], 'injected'
        material = '\n\n'.join(
            '--- %s (page %d) ---\n%s' % (c, chunks[c]['page'], chunks[c]['text'])
            for c in rec['chunk_ids'])
        pairs.append((pid, rec, sub, left, right, left_is, material))

    print('pairs todo: %d' % len(pairs), flush=True)

    def work(item):
        pid, rec, sub, left, right, left_is, material = item
        prompt = (PROMPT.replace('<<<LEFT>>>', left).replace('<<<RIGHT>>>', right)
                  .replace('<<<MATERIAL>>>', material).replace('<<<QUESTION>>>', sub['question']))
        t0 = time.time()
        for _ in range(4):
            try:
                r = client.chat.completions.create(
                    model=MODEL, max_tokens=8192,
                    messages=[{'role': 'user', 'content': prompt}],
                    response_format={'type': 'json_object'},
                    extra_body={'thinking': {'type': 'enabled'}, 'reasoning_effort': 'medium'})
                ch = r.choices[0]
                raw = (ch.message.content or '').strip()
                if not raw or ch.finish_reason == 'length':
                    continue
                data = json.loads(raw)
                break
            except Exception as e:  # noqa: BLE001
                data = None
                print('retry %s: %s' % (pid, str(e)[:120]), flush=True)
                time.sleep(2)
        else:
            print('FAIL %s' % pid, flush=True)
            return
        rec_out = {
            'pair_id': pid,
            'substrate': rec['item_id'],
            'inject_item': rec['inject_item'],
            'inject_note': rec['inject_note'],
            'left_is': left_is,
            'elapsed_s': round(time.time() - t0, 1),
            'data': data,
        }
        with open(OUT, 'a', encoding='utf-8') as f:
            f.write(json.dumps(rec_out, ensure_ascii=False) + '\n')
        # 归一化成"能否检出注入版本更差"
        better = data.get('better')
        if better == 'tie':
            verdict = 'tie'
        else:
            better_is = left_is if better == 'left' else ('injected' if left_is == 'substrate' else 'substrate')
            verdict = 'detected' if better_is == 'substrate' else 'MISSED'
        print('ok %-12s %-5s %-9s %5.0fs  %s' % (pid, rec['inject_item'], verdict,
                                                  time.time() - t0, data.get('confidence')), flush=True)

    with ThreadPoolExecutor(max_workers=6) as ex:
        list(ex.map(work, pairs))
    print('done ->', OUT, flush=True)


if __name__ == '__main__':
    main()
