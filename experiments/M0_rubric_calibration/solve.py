# -*- coding: utf-8 -*-
"""M0.5 信息充分性测试（information sufficiency test）。

为什么需要它：
- 整体 1-5 分把 19 个回答全打成 5 分，零方差，无法作为准则；
- 成对偏好可用，但**方向偏向冗长**（它认为加了寒暄和总结的那版更好）。
所以需要一个不奖励流畅、不奖励篇幅的准则：

    把解释单独给一个干净上下文（不给课件、不给原题），只让它做一道**最小变式题**；
    并要求「只能用这份解释，不够就答 INSUFFICIENT」。
    测的是：这份解释本身能不能支撑学生往下走一步。

**无解释对照组**（每个知识点一次）：如果模型不看解释也能做对，这道题就没有区分度，
该题的结论不可用——这是本测试的自我校验。

两个阶段：
  1) solve  —— 生成解答（JSON: reasoning / final_answer / coverage）
  2) grade  —— 拿 gold 判 correct / partially_correct / incorrect / insufficient

用法: python solve.py
输出: sufficiency.jsonl（可断点续跑）
"""
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

from openai import OpenAI

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(HERE, 'sufficiency.jsonl')

MODEL = 'deepseek-v4-flash'
BASE_URL = 'https://api.deepseek.com'

SOLVE_PROMPT = """Below is an explanation written for a student. Using ONLY this explanation as your source, solve the problem at the end.

Rules:
- Rely only on what the explanation states. Do NOT import facts or formulas that the explanation does not contain.
- If the explanation does not contain enough to determine the answer, set "final_answer" to "INSUFFICIENT" and "coverage" to "insufficient".
- Keep the reasoning brief.

<explanation>
<<<EXPLANATION>>>
</explanation>

<problem>
<<<PROBLEM>>>
</problem>

OUTPUT a single JSON object, no other text:
{
  "reasoning": "brief, at most a few lines",
  "final_answer": "the answer, or INSUFFICIENT",
  "coverage": "sufficient|partial|insufficient"
}
"""

GRADE_PROMPT = """Grade a student's answer against the gold answer.

<problem>
<<<PROBLEM>>>
</problem>

<gold_answer>
<<<GOLD>>>
</gold_answer>

<grading_notes>
<<<NOTES>>>
</grading_notes>

<student_final_answer>
<<<STUDENT>>>
</student_final_answer>

Decide one of:
- "correct": the final answer matches the gold answer (numerically and in the required form)
- "partially_correct": the answer is on the right track but incomplete or missing a required part (per the grading notes)
- "incorrect": the answer is wrong
- "insufficient": the student declared the explanation did not contain enough information

Be strict about the final numerical answer; ignore differences in wording or notation style.

OUTPUT a single JSON object, no other text:
{"verdict": "correct|partially_correct|incorrect|insufficient", "reason": "one sentence"}
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
    path = os.path.join(HERE, name)
    with open(path, encoding='utf-8') as f:
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
                last = 'truncated (budget=%d)' % max_tokens
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
                r = json.loads(line)
                done.add((r['response_id'], r['stage']))
    print('already done cells: %d' % len(done), flush=True)

    # 组装任务：(response_id, item_id, explanation) ；explanation 为 None 表示无解释对照
    jobs = []
    for rid, rec in sorted(base.items()):
        jobs.append((rid, rec['item_id'], rec['answer'], 'baseline'))
    for vid, rec in sorted(inj.items()):
        jobs.append((vid, rec['item_id'], rec['answer'], 'injected:' + rec['inject_item']))
    for iid in sorted(variants):
        jobs.append(('CONTROL_' + iid, iid, None, 'control_no_explanation'))

    client = OpenAI(api_key=load_key(), base_url=BASE_URL, timeout=240.0)
    lock_out = []

    def work(job):
        rid, iid, expl, kind = job
        v = variants[iid]
        # --- stage 1: solve ---
        if (rid, 'solve') not in done:
            prompt = (SOLVE_PROMPT
                      .replace('<<<EXPLANATION>>>', expl if expl else '(no explanation was provided)')
                      .replace('<<<PROBLEM>>>', v['problem']))
            t0 = time.time()
            try:
                sol = call_json(client, prompt)
            except Exception as e:  # noqa: BLE001
                print('SOLVE FAIL %s: %s' % (rid, str(e)[:120]), flush=True)
                return
            rec = {'response_id': rid, 'item_id': iid, 'kind': kind, 'stage': 'solve',
                   'elapsed_s': round(time.time() - t0, 1),
                   'final_answer': sol.get('final_answer'), 'coverage': sol.get('coverage'),
                   'reasoning': sol.get('reasoning')}
            with open(OUT, 'a', encoding='utf-8') as f:
                f.write(json.dumps(rec, ensure_ascii=False) + '\n')
            fin = str(sol.get('final_answer'))
        else:
            fin = None
            for line in open(OUT, encoding='utf-8'):
                if line.strip():
                    r = json.loads(line)
                    if r['response_id'] == rid and r['stage'] == 'solve':
                        fin = str(r.get('final_answer'))
        if fin is None:
            return

        # --- stage 2: grade ---
        if (rid, 'grade') not in done:
            prompt = (GRADE_PROMPT.replace('<<<PROBLEM>>>', v['problem'])
                      .replace('<<<GOLD>>>', v['gold'])
                      .replace('<<<NOTES>>>', v['grading'])
                      .replace('<<<STUDENT>>>', fin))
            try:
                g = call_json(client, prompt)
            except Exception as e:  # noqa: BLE001
                print('GRADE FAIL %s: %s' % (rid, str(e)[:120]), flush=True)
                return
            rec = {'response_id': rid, 'item_id': iid, 'kind': kind, 'stage': 'grade',
                   'verdict': g.get('verdict'), 'reason': g.get('reason')}
            with open(OUT, 'a', encoding='utf-8') as f:
                f.write(json.dumps(rec, ensure_ascii=False) + '\n')
            print('ok %-13s %-8s %-17s %s' % (rid, iid, kind[:17], g.get('verdict')), flush=True)
        else:
            lock_out.append(rid)

    with ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(work, jobs))
    print('done ->', OUT, flush=True)


if __name__ == '__main__':
    main()
