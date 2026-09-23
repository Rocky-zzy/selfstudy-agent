# -*- coding: utf-8 -*-
"""生成 M0 人工盲评表（成对比较 + 单独评分）与对应答案钥匙。

Part A 成对比较：每对 = 一个基线回答 + 它的一处定向缺陷版本，左右顺序随机。
                 直接检验「人能否检出这个缺陷、并把它归到正确条目」= 人工灵敏度。
Part B 单独评分：只看基线回答，给 1-5 与违反条目 = 人工区分度。

用法: python make_human_sheet.py
输出: human_rating_sheet.md, human_rating_key.json
"""
import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
random.seed(20260501)

ITEM_LEGEND = """A1 定位与意图｜A2 分阶段步进｜A3 推理链完整、关系显式｜B1 无冗余与填充
B2 范围相称｜C1 符号与术语卫生｜C2 前置桥接｜C3 给出理由，而非仅步骤"""

PAIRS = ['inj_A1_q6', 'inj_A2_q3', 'inj_A3_q4', 'inj_B1_q7', 'inj_B2_q8', 'inj_C1_q8',
         'inj_C2_q7', 'inj_C3_q3']
SOLO = ['q1', 'q2', 'q5']


def load(name):
    out = {}
    with open(os.path.join(HERE, name), encoding='utf-8') as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                out[r.get('variant_id') or r['item_id']] = r
    return out


def main():
    base = load('baseline.jsonl')
    inj = load('injected.jsonl')

    lines = []
    key = {'pairs': [], 'solo': []}

    lines.append('# M0 人工盲评表')
    lines.append('')
    lines.append('**怎么用**：这份表不用全做完。Part A 的前 4 对（A1/A2/A3/B1）最关键，'
                 '做完就能和 LLM 评判者算出一致性；有余力再往后做。')
    lines.append('')
    lines.append('**唯一要求**：不要猜"哪个是被改坏的"。如果两个回答你看不出差别，'
                 '就写"差不多"——那本身就是重要的结果（说明这个条目人判不出来）。')
    lines.append('')
    lines.append('条目速查：')
    lines.append('')
    lines.append('```')
    lines.append(ITEM_LEGEND)
    lines.append('```')
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## Part A｜成对比较')
    lines.append('')
    lines.append('每对里，两个回答**内容基本相同**，但其中一个被定向注入了一处缺陷。'
                 '顺序已随机。请回答三个问题。')
    lines.append('')

    for i, vid in enumerate(PAIRS, 1):
        substrate = inj[vid]['item_id']
        a = base[substrate]['answer']
        b = inj[vid]['answer']
        if random.random() < 0.5:
            left, right = a, b
            left_is = 'substrate'
        else:
            left, right = b, a
            left_is = 'injected'
        key['pairs'].append({
            'pair': 'A-%d' % i,
            'injected_variant': vid,
            'substrate': substrate,
            'inject_item': inj[vid]['inject_item'],
            'inject_note': inj[vid]['inject_note'],
            'left': left_is,
        })
        lines.append('### A-%d' % i)
        lines.append('')
        lines.append('**问题**：%s' % base[substrate]['question'])
        lines.append('')
        lines.append('**左**：')
        lines.append('')
        lines.append(left)
        lines.append('')
        lines.append('**右**：')
        lines.append('')
        lines.append(right)
        lines.append('')
        lines.append('> **你的判断**')
        lines.append('> - 更好的是：左 / 右 / 差不多')
        lines.append('> - 较差的那个具体问题在哪（尽量指出原句）：')
        lines.append('> - 违反条目（可多选，也可写"无"）：')
        lines.append('')

    lines.append('---')
    lines.append('')
    lines.append('## Part B｜单独评分')
    lines.append('')
    lines.append('这一部分**没有**被改坏的回答，都是原样。请给整体质量分并勾出你看到的缺陷。')
    lines.append('')

    for i, rid in enumerate(SOLO, 1):
        key['solo'].append({'id': 'B-%d' % i, 'response': rid})
        lines.append('### B-%d' % i)
        lines.append('')
        lines.append('**问题**：%s' % base[rid]['question'])
        lines.append('')
        lines.append(base[rid]['answer'])
        lines.append('')
        lines.append('> **你的判断**')
        lines.append('> - 整体质量（1=读了更糊涂 2=能懂但没帮助 3=正确可用 4=清楚有帮助 5=读完基本就懂了）：')
        lines.append('> - 存在的缺陷（可多选，也可写"无"）：')
        lines.append('')

    with open(os.path.join(HERE, 'human_rating_sheet.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    with open(os.path.join(HERE, 'human_rating_key.json'), 'w', encoding='utf-8') as f:
        json.dump(key, f, ensure_ascii=False, indent=2)
    print('wrote human_rating_sheet.md (%d pairs, %d solo)' % (len(PAIRS), len(SOLO)))
    for p in key['pairs']:
        print('  %s  %-12s inject=%s  left=%s' % (p['pair'], p['injected_variant'],
                                                  p['inject_item'], p['left']))


if __name__ == '__main__':
    main()
