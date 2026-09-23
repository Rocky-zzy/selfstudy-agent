# -*- coding: utf-8 -*-
"""M0.5b 归因探针：解变式题时，逐步标注这一步是「解释支持的」还是「自己补的」。

动机：M0.5 的信息充分性测试出现天花板——19 个回答全部 correct，无法区分。
可能是变式题太简单，也可能是充分性根本不是这套 rubric 的正确准则。

本探针换一个因变量：
  - 若某缺陷造成**信息缺口**（推理链断裂 A3、符号未定义 C1、前置未点名 C2），
    求解器就必须自己补步 -> n_unsupported > 0；
  - 若某缺陷只是**加工成本**问题（冗余 B1、范围 B2、分段 A2），信息并未缺失，
    求解器不需要补步 -> n_unsupported = 0。

这样能把 rubric 的条目分成「信息缺口型」与「加工成本型」两类，
并说明：任何基于信息充分性的准则**只能验证前一类**。

沿用 M0.5 的最小变式题与无解释对照组。
用法: python solve2.py
输出: attribution.jsonl
"""
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

from openai import OpenAI

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(HERE, 'attribution.jsonl')

MODEL = 'deepseek-v4-flash'
BASE_URL = 'https://api.deepseek.com'

PROMPT = """Below is an explanation written for a student. Solve the problem at the end, and for EACH step of your solution state whether that step is supported by the explanation or whether you had to supply it from your own knowledge.

Be strict. A step counts as supported ("E") only if the explanation actually contains the fact, formula, definition or justification that the step relies on. If your step needs something the explanation does not state, that step is "S".

<explanation>
<<<EXPLANATION>>>
</explanation>

<problem>
<<<PROBLEM>>>
</problem>

OUTPUT a single JSON object, no other text:
{
  "steps": [{"step": "short description", "source": "E or S", "why": "brief"}],
  "n_unsupported": 0,
  "self_sufficient": true,
  "missing": "what the explanation would have to add for every step to be E, or 'none'"
}
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


def call_json(client, prompt, max_tokens=4096):
    last = None
    for _ in range(4):
        try:
            r = client.chat.completions.create(
                model=MODEL, max_tokens=max_tokens,
                messages=[{'role': 'user', 'content': prompt}],
                response_format={'type': 'json_object'},
                extra_body={'thinking': {'type': 'enabled'}, 'reasoning_effort': 'medium'})
            ch = r.choices[0]
            raw = (ch.message.content or '').strip()
            if not raw or ch.finish_reason == 'length':
                last = 'truncated'
                max_tokens = int(max_tokens * 1.5)
                continue
            return json.loads(raw)
        except Exception as e:  # noqa: BLE001
            last = '%s: %s' % (type(e).__name__, str(e)[:160])
            time.sleep(2)
    raise RuntimeError(last)


def main():
    base = load_jsonl('baseline.jsonl')
    inj = load_jsonl('injected.jsonl')
    variants = {v['item_id']: v for v in
                json.load(open(os.path.join(HERE, 'variants.json'), encoding='utf-8'))['variants']}

    done = set()
    if os.path.exists(OUT):
        for line in open(OUT, encoding='utf-8'):
            if line.strip():
                done.add(json.loads(line)['response_id'])

    jobs = [(rid, rec['item_id'], rec['answer'], 'baseline') for rid, rec in sorted(base.items())]
    jobs += [(vid, rec['item_id'], rec['answer'], 'injected:' + rec['inject_item'])
             for vid, rec in sorted(inj.items())]
    jobs += [('CONTROL_' + iid, iid, None, 'control_no_explanation') for iid in sorted(variants)]
    jobs = [j for j in jobs if j[0] not in done]
    print('todo: %d' % len(jobs), flush=True)

    client = OpenAI(api_key=load_key(), base_url=BASE_URL, timeout=240.0)

    def work(job):
        rid, iid, expl, kind = job
        prompt = (PROMPT
                  .replace('<<<EXPLANATION>>>', expl if expl else '(no explanation was provided)')
                  .replace('<<<PROBLEM>>>', variants[iid]['problem']))
        try:
            d = call_json(client, prompt)
        except Exception as e:  # noqa: BLE001
            print('FAIL %s: %s' % (rid, str(e)[:120]), flush=True)
            return
        rec = {'response_id': rid, 'item_id': iid, 'kind': kind,
               'n_unsupported': d.get('n_unsupported'),
               'self_sufficient': d.get('self_sufficient'),
               'missing': d.get('missing'),
               'steps': d.get('steps')}
        with open(OUT, 'a', encoding='utf-8') as f:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        print('ok %-13s %-6s %-17s n_unsup=%s self_suff=%s'
              % (rid, iid, kind[:17], d.get('n_unsupported'), d.get('self_sufficient')), flush=True)

    with ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(work, jobs))
    print('done ->', OUT, flush=True)


if __name__ == '__main__':
    main()
