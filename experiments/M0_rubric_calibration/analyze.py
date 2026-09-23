# -*- coding: utf-8 -*-
"""M0 分析：区分度 / 灵敏度 / 特异度 / 一致性 / 准则效度，并给出逐条裁决建议。

用法: python analyze.py
读取: baseline.jsonl, injected.jsonl, verdicts.jsonl, pair_verdicts.jsonl
"""
import json
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ITEMS = ['A1', 'A2', 'A3', 'B1', 'B2', 'C1', 'C2', 'C3']
HARD = {'A3', 'B1', 'C1'}
RUBRIC_JUDGES = ['sat_a', 'sat_b', 'def']


def load_jsonl(name):
    path = os.path.join(HERE, name)
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            if line.strip():
                out.append(json.loads(line))
    return out


def verdict(data, item):
    if not data:
        return None
    return data.get('items', {}).get(item, {}).get('verdict')


def kappa(pairs):
    pairs = [(a, b) for a, b in pairs if a and b]
    n = len(pairs)
    if n == 0:
        return None, 0.0
    po = sum(1 for a, b in pairs if a == b) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return ((po - pe) / (1 - pe) if pe < 1 else 1.0), po


def main():
    base = {r['item_id']: r for r in load_jsonl('baseline.jsonl')}
    inj = {r['variant_id']: r for r in load_jsonl('injected.jsonl')}
    V = {(r['response_id'], r['judge']): r['data'] for r in load_jsonl('verdicts.jsonl')}
    P = {r['pair_id']: r for r in load_jsonl('pair_verdicts.jsonl')}

    responses = sorted({i for (i, _j) in V})
    print('responses=%d (baseline %d + injected %d)   rubric cells=%d   pair cells=%d'
          % (len(responses), len(base), len(inj),
             sum(1 for i in responses for j in RUBRIC_JUDGES if (i, j) in V), len(P)))
    miss = [(i, j) for i in responses for j in RUBRIC_JUDGES if (i, j) not in V]
    print('missing rubric cells: %s' % (miss or 'none'))

    # ================= 1. 区分度 =================
    print('\n' + '=' * 84)
    print('1. 区分度：8 个基线回答上的条目判定（sat_a）')
    print('=' * 84)
    print('%-5s %-6s %-6s %-6s %-8s %-7s' % ('item', 'pass', 'fail', 'na', 'fail%', '性质'))
    disc = {}
    for it in ITEMS:
        c = Counter(verdict(V.get((b, 'sat_a')), it) for b in base)
        scorable = c['pass'] + c['fail']
        rate = (c['fail'] / scorable) if scorable else 0.0
        disc[it] = rate
        print('%-5s %-6d %-6d %-6d %-7.0f%% %-7s'
              % (it, c['pass'], c['fail'], c['na'], rate * 100, 'Hard' if it in HARD else 'Ctx'))

    # ================= 2. 适用性 =================
    print('\n' + '=' * 84)
    print('2. 适用性判定（响应类型）')
    print('=' * 84)
    bad = 0
    for b in sorted(base):
        got = {j: V.get((b, j), {}).get('response_type') for j in RUBRIC_JUDGES}
        ok = all(g == base[b]['expected_type'] for g in got.values())
        bad += 0 if ok else 1
        if not ok:
            print('  MISMATCH %-3s expected=%s got=%s' % (b, base[b]['expected_type'], got))
    print('  8 题 × 3 评判者全部与预期一致: %s' % ('是' if bad == 0 else '否(%d)' % bad))
    na_only_q8 = all(
        verdict(V.get((b, 'sat_a')), it) == 'na'
        for b in base if base[b]['expected_type'] == 'T1' for it in ['A1', 'A2', 'A3', 'C2', 'C3'])
    print('  T1 上应标 na 的条目确实全部标 na: %s' % ('是' if na_only_q8 else '否'))

    # ================= 3. 灵敏度 / 特异度 =================
    print('\n' + '=' * 84)
    print('3. 缺陷注入：灵敏度（目标条目是否翻成 fail）/ 特异度（其他条目是否被连带改动）')
    print('=' * 84)
    sens = {it: [0, 0] for it in ITEMS}          # [flip, testable]
    spec_bad = Counter()
    for j in RUBRIC_JUDGES:
        print('\n--- judge = %s ---' % j)
        print('%-13s %-4s %-24s %s' % ('variant', 'targ', 'target sub->inj', 'other items changed'))
        for vid in sorted(inj):
            sub, tgt = inj[vid]['item_id'], inj[vid]['inject_item']
            pre = verdict(V.get((sub, j)), tgt)
            post = verdict(V.get((vid, j)), tgt)
            changed = []
            for it in ITEMS:
                if it == tgt:
                    continue
                a, b_ = verdict(V.get((sub, j)), it), verdict(V.get((vid, j)), it)
                if a != b_:
                    changed.append('%s:%s->%s' % (it, a, b_))
                    spec_bad[it] += 1
            if pre == 'fail':
                tag = 'untestable(already fail)'
            elif post == 'fail':
                tag = 'FLIP'
                sens[tgt][0] += 1
                sens[tgt][1] += 1
            else:
                tag = 'NO-FLIP'
                sens[tgt][1] += 1
            print('%-13s %-4s %-24s %s'
                  % (vid, tgt, '%s -> %s  %s' % (pre, post, tag), ', '.join(changed) or '-'))

    print('\n灵敏度汇总（3 个评判者 × 各注入变体）：')
    print('%-5s %-12s %s' % ('item', 'flip/testable', '判定'))
    sens_rate = {}
    for it in ITEMS:
        f, t = sens[it]
        r = (f / t) if t else None
        sens_rate[it] = r
        note = '—' if r is None else (
            '灵敏' if r >= 0.8 else ('部分' if r > 0 else '**完全检不出**'))
        print('%-5s %-12s %s' % (it, '%d/%d' % (f, t) if t else 'n/a', note))

    print('\n特异度：被连带改动的次数（越少越好）')
    for it, n in spec_bad.most_common():
        print('  %-5s 被误伤 %d 次' % (it, n))

    # ================= 4. 一致性 =================
    print('\n' + '=' * 84)
    print('4. 一致性（注意：全 pass 无方差的条目，一致率是虚高的）')
    print('=' * 84)
    ps = [(verdict(V.get((i, 'sat_a')), it), verdict(V.get((i, 'sat_b')), it))
          for i in responses for it in ITEMS]
    pc = [(verdict(V.get((i, 'sat_a')), it), verdict(V.get((i, 'def')), it))
          for i in responses for it in ITEMS]
    for name, pairs in [('sat_a vs sat_b 自一致性', ps), ('sat_a vs def   跨框架', pc)]:
        k, po = kappa(pairs)
        print('%-24s n=%d  一致率=%.1f%%  kappa=%s'
              % (name, len([p for p in pairs if p[0] and p[1]]), po * 100,
                 '%.2f' % k if k is not None else 'n/a'))
    print('\n%-5s %-11s %-11s %-9s %s' % ('item', 'self', 'cross', 'fail数', '备注'))
    for it in ITEMS:
        s_pairs = [(verdict(V.get((i, 'sat_a')), it), verdict(V.get((i, 'sat_b')), it)) for i in responses]
        c_pairs = [(verdict(V.get((i, 'sat_a')), it), verdict(V.get((i, 'def')), it)) for i in responses]
        _, so = kappa(s_pairs)
        _, co = kappa(c_pairs)
        nfail = sum(1 for i in responses if verdict(V.get((i, 'sat_a')), it) == 'fail')
        note = '**无方差，一致率虚高**' if nfail == 0 else ''
        print('%-5s %-11s %-11s %-9d %s'
              % (it, '%.0f%%' % (so * 100), '%.0f%%' % (co * 100), nfail, note))

    # ================= 5. 准则效度 =================
    print('\n' + '=' * 84)
    print('5. 准则效度')
    print('=' * 84)
    hol = {i: V.get((i, 'hol'), {}).get('overall') for i in responses}
    hv = Counter(hol.values())
    print('5a. 整体 1-5 分（holistic 绝对评分）的取值分布: %s' % dict(sorted(hv.items())))
    print('    -> %s' % ('**零方差，无法作为准则**（连被注入缺陷的版本也全部满分）'
                         if len(hv) == 1 else '有方差，可用'))
    print('\n5b. 成对偏好（pairwise，替换准则）: 无 rubric 的评判者能否指出注入版本更差')
    print('%-13s %-5s %-10s %s' % ('variant', 'targ', 'verdict', 'confidence'))
    det = {it: [0, 0] for it in ITEMS}
    for vid in sorted(P):
        r = P[vid]
        better = r['data'].get('better')
        if better == 'tie':
            v = 'tie'
        else:
            better_side = r['left_is'] if better == 'left' else (
                'injected' if r['left_is'] == 'substrate' else 'substrate')
            v = 'detected' if better_side == 'substrate' else 'MISSED'
        if v != 'tie':
            det[r['inject_item']][0 if v == 'detected' else 1] += 1
        print('%-13s %-5s %-10s %s' % (vid, r['inject_item'], v, r['data'].get('confidence')))
    print('\n按条目汇总（成对判定）:')
    print('%-5s %-10s %-8s %s' % ('item', 'detected', 'missed', '判定'))
    for it in ITEMS:
        d, m = det[it]
        if d + m == 0:
            continue
        print('%-5s %-10d %-8d %s' % (it, d, m, '注入的缺陷可被无 rubric 的评判者察觉' if d > m else
                                      '**缺陷不可察觉 -> 该条目可能在挑无关紧要的东西**'))

    # ================= 6. 门槛 =================
    print('\n' + '=' * 84)
    print('6. 门槛（正确性）')
    print('=' * 84)
    gf = [(i, j) for i in responses for j in RUBRIC_JUDGES
          if V.get((i, j), {}).get('gate', {}).get('correctness') == 'fail']
    print('gate=fail 的格数: %d  %s' % (len(gf), gf or ''))

    # ================= 7. 裁决建议 =================
    print('\n' + '=' * 84)
    print('7. 逐条裁决建议（区分度 × 灵敏度 × 稳定性）')
    print('=' * 84)
    print('%-5s %-9s %-12s %-9s %-9s %s' % ('item', '基线fail%', '灵敏度', '自一致', '跨框架', '建议'))
    for it in ITEMS:
        s_pairs = [(verdict(V.get((i, 'sat_a')), it), verdict(V.get((i, 'sat_b')), it)) for i in responses]
        c_pairs = [(verdict(V.get((i, 'sat_a')), it), verdict(V.get((i, 'def')), it)) for i in responses]
        _, so = kappa(s_pairs)
        _, co = kappa(c_pairs)
        r = sens_rate[it]
        if disc[it] == 0 and (r == 0 or r is None):
            adv = '**删除**：基线从不违反且注入检不出'
        elif r is not None and r < 0.5:
            adv = '**删除/重做操作化**：检不出'
        elif disc[it] == 0:
            adv = '**删除**：基线从不违反（无增益空间）'
        elif so < 0.8:
            adv = '保留但需提高稳定性'
        else:
            adv = '保留'
        print('%-5s %-9s %-12s %-9s %-9s %s'
              % (it, '%.0f%%' % (disc[it] * 100),
                 ('%d/%d' % tuple(sens[it])) if sens[it][1] else 'n/a',
                 '%.0f%%' % (so * 100), '%.0f%%' % (co * 100), adv))


if __name__ == '__main__':
    main()
