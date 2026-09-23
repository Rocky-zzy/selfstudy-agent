# -*- coding: utf-8 -*-
"""M0 缺陷注入（defect injection）。

对每条 rubric 条目，把一个基线回答**定向改坏一处**，只注入该条目对应的那一种缺陷。
用途：检验该条目能否**专门**测到它该测的东西——注入后该条目应翻成 fail，而其他条目应保持原判。

锚点使用 text.index 定位（不做正则转义），找不到锚点就直接报错，绝不静默跳过。

用法: python inject.py
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
BASELINE = os.path.join(HERE, 'baseline.jsonl')
OUT = os.path.join(HERE, 'injected.jsonl')


def load_baseline():
    out = {}
    with open(BASELINE, encoding='utf-8') as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                out[r['item_id']] = r
    return out


def cut_between(text, start_marker, end_marker, keep_end=False):
    """删除 [start_marker .. end_marker] 这段（含标记本身）。"""
    i = text.index(start_marker)
    j = text.index(end_marker, i) + (0 if keep_end else len(end_marker))
    return text[:i] + text[j:]


def drop_first_paragraph(text):
    parts = text.split('\n\n', 1)
    assert len(parts) == 2, 'expected at least two paragraphs'
    return parts[1].lstrip('\n')


def strip_headings(text):
    lines = [ln for ln in text.split('\n') if not re.match(r'^\s*#{1,6}\s', ln)]
    out = '\n'.join(lines)
    return re.sub(r'\n{3,}', '\n\n', out).strip()


def wall_of_text(text):
    """更强的 A2 缺陷：去掉阶段标题后，再把段落分隔也抹掉，成为一整块文字。"""
    t = strip_headings(text)
    t = re.sub(r'^\s*-{3,}\s*$', '', t, flags=re.M)
    t = re.sub(r'\n\s*\n+', '\n', t)
    return t.strip()


def strip_all_why(text):
    """更强的 C3 缺陷：删掉全部「为什么」——开头的心法、含义说明、正交性证明、归一化理由。"""
    t = text
    t = cut_between(t, 'Gram–Schmidt 的本质可以理解成一句话：', '只留下与前面所有方向都垂直的新成分。')
    t = cut_between(t, '也就是说，每一步做的事是：', '就垂直于所有这些旧方向。')
    t = cut_between(t, '## 3.', '## 4.')
    before = t
    t = t.replace('最后为什么要归一化？', '归一化')
    assert t != before, 'C3b: 归一化小标题未替换'
    return t


PLEASANTRY = '这是一个很好的问题！下面我来为你详细解答。\n\n'
REDUNDANT_RESTATEMENT = (
    '\n\n换句话说，条件熵所刻画的就是：在已经掌握了 $X$ 的信息之后，'
    '$Y$ 身上依然残留的那一部分不确定性。'
)
INFO_FREE_SUMMARY = (
    '\n\n总结一下：上面我们先写出了联合熵和条件熵的定义式，然后借助概率的链式法则，'
    '最终推导出了 $H(X,Y)=H(X)+H(Y\\mid X)$ 这个关系。希望这个解答对你有帮助！'
)
OUT_OF_SCOPE = (
    '\n\n补充一些相关的背景，方便你之后查阅：\n\n'
    '在矩阵微积分中，layout 约定有两套主流体系。numerator layout 把标量对列向量的导数写成行向量；'
    'denominator layout 则写成列向量。两者互为转置，因此同一个公式在两套体系下会相差一个转置符号。\n\n'
    '常用的几个梯度恒等式还包括：\n\n'
    '$$\\frac{\\partial \\vec{a}^T \\vec{x}}{\\partial \\vec{x}}=\\vec{a}^T,\\qquad '
    '\\frac{\\partial \\vec{x}^T \\vec{x}}{\\partial \\vec{x}}=2\\vec{x}^T,\\qquad '
    '\\frac{\\partial \\vec{x}^T A \\vec{x}}{\\partial \\vec{x}}=\\vec{x}^T(A+A^T).$$\n\n'
    '其中 $A$ 是方阵。这些恒等式在推导最小二乘、PCA 和神经网络反向传播时都会用到。'
    '如果你之后要处理矩阵对矩阵的导数，还会遇到四维张量的情形，那时最好固定一套 layout 约定并全程保持一致，'
    '否则很容易在转置上出错。'
)
OUT_OF_SCOPE_2 = (
    '\n\n顺带补充一些背景，方便你以后查阅：\n\n'
    '特征值在实际计算中通常不会真的去展开特征多项式。对 $n\\ge 5$ 的多项式没有通用的根式解，'
    '而且直接求根在数值上很不稳定，所以实际用的是 QR 算法、幂法、Arnoldi 迭代等方法。\n\n'
    '在应用上，特征分解是 PCA 的基础：对协方差矩阵做特征分解，最大特征值对应的特征向量就是第一主成分。'
    '在图论里，邻接矩阵的谱能刻画图的连通性和社区结构；在动力系统里，特征值决定平衡点的稳定性。\n\n'
    '另外，特征多项式还有一些一般性质：相似矩阵有相同的特征多项式；'
    '$\\det(A)=\\prod_i\\lambda_i$，$\\operatorname{tr}(A)=\\sum_i\\lambda_i$；'
    'Cayley–Hamilton 定理说 $p_A(A)=0$。'
)


def build(texts):
    specs = []

    # --- A1 定位与意图：删掉 q6 开头的定位段，让回答直接从 case 1 开始 ---
    specs.append(dict(
        variant_id='inj_A1_q6', substrate='q6', inject_item='A1',
        note='删除开头的定位段（说明这段要settle什么），直接从 case 1 切入',
        fn=lambda t: drop_first_paragraph(t),
    ))

    # --- A2 分阶段步进：删掉 q3 的所有阶段标题 ---
    specs.append(dict(
        variant_id='inj_A2_q3', substrate='q3', inject_item='A2',
        note='删除全部阶段标题（## 1. ... ## 5.），阶段边界不再显式',
        fn=lambda t: strip_headings(t),
    ))

    # --- A3 推理链完整：删掉 q4 中「齐次方程组有非零解 <=> singular <=> det=0」的桥 ---
    specs.append(dict(
        variant_id='inj_A3_q4', substrate='q4', inject_item='A3',
        note='删除从 (A-λI)x=0 到 det(A-λI)=0 之间的推理桥（singular 等价条件）',
        fn=lambda t: cut_between(t, '这是一个齐次线性方程组。', 'determinant 为 \\(0\\)：'),
    ))

    # --- B1 无冗余与填充：q7 加寒暄 + 同义复述 + 无信息总结 ---
    def b1(t):
        t = PLEASANTRY + t
        t = t.replace(
            '表示在已知 \\(X\\) 后，\\(Y\\) 还剩下的平均不确定性。',
            '表示在已知 \\(X\\) 后，\\(Y\\) 还剩下的平均不确定性。' + REDUNDANT_RESTATEMENT,
            1,
        )
        assert REDUNDANT_RESTATEMENT in t, 'B1 redundancy anchor not applied'
        return t + INFO_FREE_SUMMARY
    specs.append(dict(
        variant_id='inj_B1_q7', substrate='q7', inject_item='B1',
        note='前置寒暄 + 同义复述条件熵 + 无信息量总结（覆盖 B1 的三个锚点）',
        fn=b1,
    ))

    # --- B2 范围相称：q8（T1 事实题）追加大量超范围的矩阵微积分内容 ---
    specs.append(dict(
        variant_id='inj_B2_q8', substrate='q8', inject_item='B2',
        note='事实型问题上追加 layout 体系、其他梯度恒等式、张量等超范围内容',
        fn=lambda t: t + OUT_OF_SCOPE,
    ))

    # --- C1 符号与术语卫生：q8 删掉「x 和 a 都是列向量」的定义 ---
    specs.append(dict(
        variant_id='inj_C1_q8', substrate='q8', inject_item='C1',
        note='删除对 \\(\\vec{x}\\)、\\(\\vec{a}\\) 的定义从句，符号首次出现即未定义',
        fn=lambda t: cut_between(t, '其中 ', '无关。'),
    ))

    # --- C2 前置桥接：q7 把「概率的链式法则」这个前置的点名换成无归属的「注意到」 ---
    specs.append(dict(
        variant_id='inj_C2_q7', substrate='q7', inject_item='C2',
        note='把「关键关系来自概率的链式法则」换成「注意到」，前置结论被静默使用（难例）',
        fn=lambda t: t.replace('关键关系来自概率的链式法则：', '注意到', 1),
    ))

    # --- C3 给出理由：q3 删掉「为什么减完就正交」整节 ---
    specs.append(dict(
        variant_id='inj_C3_q3', substrate='q3', inject_item='C3',
        note='删除「## 3. 为什么减完就正交？」整节，只留做法与验证',
        fn=lambda t: cut_between(t, '## 3.', '## 4.'),
    ))

    # --- 第二轮：首轮未翻或测试作废的条目，用更强的缺陷重做 ---
    specs.append(dict(
        variant_id='inj_A2b_q3', substrate='q3', inject_item='A2',
        note='[更强] 去标题后连段落分隔一并抹掉，整篇成为一块没有阶段边界的文字',
        fn=lambda t: wall_of_text(t),
    ))
    specs.append(dict(
        variant_id='inj_B2b_q4', substrate='q4', inject_item='B2',
        note='[更强/T2 靶子] 在 T2 回答后追加数值算法、PCA、谱图论、Cayley–Hamilton 等超范围内容',
        fn=lambda t: t + OUT_OF_SCOPE_2,
    ))
    specs.append(dict(
        variant_id='inj_C3b_q3', substrate='q3', inject_item='C3',
        note='[更强] 删掉全部「为什么」：开头心法、含义说明、正交性证明、归一化理由',
        fn=lambda t: strip_all_why(t),
    ))

    records = []
    for s in specs:
        src = texts[s['substrate']]['answer']
        new = s['fn'](src)
        assert new != src, 'injection %s produced no change' % s['variant_id']
        assert len(new) > 80, 'injection %s produced a suspiciously short answer' % s['variant_id']
        base = texts[s['substrate']]
        records.append({
            'variant_id': s['variant_id'],
            'item_id': s['substrate'],
            'topic': base['topic'],
            'question': base['question'],
            'chunk_ids': base['chunk_ids'],
            'expected_type': base['expected_type'],
            'inject_item': s['inject_item'],
            'inject_note': s['note'],
            'substrate_chars': len(src),
            'answer_chars': len(new),
            'answer': new,
        })
    return records


def main():
    texts = load_baseline()
    records = build(texts)
    with open(OUT, 'w', encoding='utf-8') as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print('wrote %d injected variants -> %s' % (len(records), OUT))
    for r in records:
        print('  %-12s <- %-3s  %d -> %d chars  [%s]'
              % (r['variant_id'], r['item_id'], r['substrate_chars'], r['answer_chars'], r['inject_item']))


if __name__ == '__main__':
    main()
