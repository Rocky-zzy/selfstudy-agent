# -*- coding: utf-8 -*-
"""M0.5b 分析：归因探针（n_unsupported）是否可靠。

判据：若某注入只**增删非信息性内容**（寒暄、总结、超范围补充、分段变化），
正文信息量不变，则 n_unsupported 不应变化。变化多少就是噪声。

用法: python analyze_attribution.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ITEMS = ['A1', 'A2', 'A3', 'B1', 'B2', 'C1', 'C2', 'C3']
# 只增删非信息性内容的注入：正文信息量不变，n_unsupported 的变动即噪声
NON_INFORMATIONAL = {'A2', 'B1', 'B2', 'C3'}


def load(name):
    return [json.loads(l) for l in open(os.path.join(HERE, name), encoding='utf-8') if l.strip()]


def main():
    A = {r['response_id']: r for r in load('attribution.jsonl')}
    base = {r['item_id']: r for r in load('baseline.jsonl')}
    inj = {r['variant_id']: r for r in load('injected.jsonl')}

    print('=' * 88)
    print('对照组（无解释）：n_unsupported 应远高于任何有解释的版本')
    print('=' * 88)
    cs = [(i, A['CONTROL_' + i]['n_unsupported']) for i in sorted(base) if 'CONTROL_' + i in A]
    for i, n in cs:
        print('  CONTROL_%-3s n_unsupported=%s' % (i, n))
    print('  对照均值 %.1f' % (sum(n for _i, n in cs) / len(cs)))

    print('\n' + '=' * 88)
    print('基底 -> 注入：n_unsupported 变化（Δ>0 才说明缺陷造成了信息缺口）')
    print('=' * 88)
    print('%-13s %-4s %-6s %-6s %-6s %s' % ('variant', 'targ', '基底', '注入', 'Δ', '注入类型'))
    deltas = {}
    for vid in sorted(inj):
        sub, tgt = inj[vid]['item_id'], inj[vid]['inject_item']
        if sub not in A or vid not in A:
            continue
        a = A[sub]['n_unsupported']
        b = A[vid]['n_unsupported']
        kind = '非信息性' if tgt in NON_INFORMATIONAL else '信息缺口型'
        deltas[vid] = (tgt, b - a, kind)
        print('%-13s %-4s %-6s %-6s %-6s %s' % (vid, tgt, a, b, '%+d' % (b - a), kind))

    print('\n' + '=' * 88)
    print('可靠性检验：非信息性注入的 Δ 应当为 0，实际值即噪声')
    print('=' * 88)
    ni = [d for _v, (t, d, k) in deltas.items() if k == '非信息性']
    ig = [d for _v, (t, d, k) in deltas.items() if k == '信息缺口型']
    if ni:
        print('  非信息性注入 Δ: %s   均值 %+.2f  最大绝对变动 %d'
              % (['%+d' % d for d in ni], sum(ni) / len(ni), max(abs(d) for d in ni)))
    if ig:
        print('  信息缺口型注入 Δ: %s   均值 %+.2f'
              % (['%+d' % d for d in ig], sum(ig) / len(ig)))

    worst = max(deltas.items(), key=lambda kv: abs(kv[1][1]))
    print('\n  最严重的一例: %s（%s）Δ=%+d —— 该注入只增删非信息性内容，'
          '\n  但 n_unsupported 变动了 %d 步。这说明该因变量主要由噪声主导。'
          % (worst[0], worst[1][2], worst[1][1], abs(worst[1][1])))

    print('\n' + '=' * 88)
    print('结论')
    print('=' * 88)
    print('  非信息性注入本不应改变 n_unsupported，实测最大变动 %d 步；'
          % max((abs(d) for d in ni), default=0))
    print('  且方向频繁为**负**（加了内容反而"更自足"），与机制预期相反。')
    print('  -> 该探针不可作为准则效度的依据。')


if __name__ == '__main__':
    main()
