# -*- coding: utf-8 -*-
"""M0.5 分析：信息充分性测试。

三件事：
  A. 自我校验——无解释对照组。若某题不看解释也能做对，该题无区分度，结论不可用。
  B. 准则效度——把某条目的缺陷注入进去，回答的**可用性**是否真的下降？
     这补上了 M0 缺失的准则：它不奖励流畅、不奖励篇幅。
  C. 与 M0 的灵敏度结论对照，看 v0.3 的取舍是否成立。

用法: python analyze_sufficiency.py
"""
import json
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ITEMS = ['A1', 'A2', 'A3', 'B1', 'B2', 'C1', 'C2', 'C3']
SCORE = {'correct': 2, 'partially_correct': 1, 'incorrect': 0, 'insufficient': 0}
SUFFICIENT = {'correct', 'partially_correct'}


def load(name):
    path = os.path.join(HERE, name)
    out = []
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    out.append(json.loads(line))
    return out


def main():
    rows = load('sufficiency.jsonl')
    grade = {r['response_id']: r for r in rows if r['stage'] == 'grade'}
    solve = {r['response_id']: r for r in rows if r['stage'] == 'solve'}
    base = {r['item_id']: r for r in load('baseline.jsonl')}
    inj = {r['variant_id']: r for r in load('injected.jsonl')}

    print('solve 记录 %d，grade 记录 %d' % (len(solve), len(grade)))
    missing = [r for r in rows if r['stage'] == 'solve' and rows and r['response_id'] not in grade]
    if missing:
        print('缺 grade 的: %s' % [m['response_id'] for m in missing])

    # ---------- A. 对照组自我校验 ----------
    print('\n' + '=' * 84)
    print('A. 无解释对照组（自我校验）：不看解释能否做对')
    print('=' * 84)
    print('%-6s %-12s %-19s %s' % ('item', '对照判定', '对照最终答案', '该题是否可用'))
    usable = {}
    for iid in sorted(base):
        rid = 'CONTROL_' + iid
        g = grade.get(rid, {})
        v = g.get('verdict')
        ans = str(solve.get(rid, {}).get('final_answer'))[:40]
        usable[iid] = (v == 'insufficient') or (v == 'incorrect')
        note = '可用' if usable[iid] else '**无区分度：不看解释也能做对**'
        print('%-6s %-12s %-19s %s' % (iid, v, ans, note))
    n_usable = sum(usable.values())
    print('\n可用题数: %d / %d' % (n_usable, len(usable)))

    # ---------- B. 基线可用性 ----------
    print('\n' + '=' * 84)
    print('B. 基线回答的可用性')
    print('=' * 84)
    print('%-4s %-11s %-13s %s' % ('resp', 'verdict', 'coverage', '解释长度'))
    for rid in sorted(base):
        g = grade.get(rid, {})
        s = solve.get(rid, {})
        print('%-4s %-11s %-13s %d' % (rid, g.get('verdict'), s.get('coverage'),
                                       base[rid]['answer_chars']))
    bc = defaultdict(int)
    for rid in base:
        bc[grade.get(rid, {}).get('verdict')] += 1
    print('基线分布: %s   充分率 %.0f%%'
          % (dict(bc), 100 * sum(bc[k] for k in SUFFICIENT) / max(1, len(base))))

    # ---------- C. 准则效度：注入缺陷是否降低可用性 ----------
    print('\n' + '=' * 84)
    print('C. 准则效度：把某条目的缺陷注入后，回答的可用性是否下降')
    print('=' * 84)
    print('%-13s %-4s %-26s %-9s %s' % ('variant', 'targ', 'verdict 基底 -> 注入', 'Δscore', '该题可用?'))
    per_item = defaultdict(list)
    for vid in sorted(inj):
        sub, tgt = inj[vid]['item_id'], inj[vid]['inject_item']
        gv, gi = grade.get(sub, {}).get('verdict'), grade.get(vid, {}).get('verdict')
        ds = (SCORE.get(gi, 0) - SCORE.get(gv, 0)) if (gv and gi) else None
        usable_note = '' if usable.get(sub) else '(题无区分度)'
        print('%-13s %-4s %-26s %-9s %s'
              % (vid, tgt, '%s -> %s' % (gv, gi), ds if ds is not None else 'n/a', usable_note))
        if ds is not None and usable.get(sub):
            per_item[tgt].append(ds)

    print('\n按条目汇总（只用有区分度的题；Δscore 为负 = 可用性下降 = 该缺陷有实际后果）:')
    print('%-5s %-10s %-9s %s' % ('item', 'n', 'mean Δ', '判定'))
    for it in ITEMS:
        ds = per_item.get(it)
        if not ds:
            print('%-5s %-10s %-9s %s' % (it, 0, '-', '无可用的注入样本'))
            continue
        m = sum(ds) / len(ds)
        if m <= -1.0:
            verdict = '**缺陷严重损害可用性**'
        elif m < 0:
            verdict = '缺陷有轻微影响'
        else:
            verdict = '**缺陷不影响可用性（人眼能看出但学生照样能做对）**'
        print('%-5s %-10d %-9.2f %s' % (it, len(ds), m, verdict))

    # ---------- D. 与 M0 灵敏度对照 ----------
    print('\n' + '=' * 84)
    print('D. 与 M0 的对照')
    print('=' * 84)
    M0_SENS = {'A1': '3/3', 'A2': '0/6', 'A3': '3/3', 'B1': '1/1',
               'B2': '6/6', 'C1': 'n/a', 'C2': '0/3', 'C3': '0/6'}
    print('%-5s %-10s %-14s %s' % ('item', 'M0 灵敏度', 'M0.5 mean Δ', '结论'))
    for it in ITEMS:
        ds = per_item.get(it)
        m = (sum(ds) / len(ds)) if ds else None
        ms = M0_SENS.get(it, '?')
        if ms in ('0/6', '0/3') and (m is None or m >= 0):
            concl = 'rubric 检不出 且 缺陷无实际后果 -> 支持移出计分'
        elif ms in ('0/6', '0/3') and m < 0:
            concl = '**rubric 检不出，但缺陷确实损害可用性 -> 应重做操作化，不该删**'
        elif m is not None and m < 0:
            concl = 'rubric 检得出 且 后果真实 -> 保留'
        else:
            concl = '保留（后果不明确，样本少）'
        print('%-5s %-10s %-14s %s' % (it, ms, ('%.2f' % m) if m is not None else '-', concl))


if __name__ == '__main__':
    main()
