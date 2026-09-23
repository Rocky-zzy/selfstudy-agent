# -*- coding: utf-8 -*-
"""数学渲染的测试：提取定界符 + LaTeX -> MathML。

为什么要单独一个测试文件：这些样例本身带大量反斜杠，
写在命令行里会被 shell 的转义规则吃掉（已经踩过），必须落在文件里。

跑法：
    python app/test_mathrender.py         # 全部
    python app/test_mathrender.py -v      # 打印每条的 MathML 片段
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mathrender import extract_math, render_math, self_check  # noqa: E402

fails: list[str] = []


def check(cond: bool, msg: str) -> None:
    print(("  [OK] " if cond else "  [!!] ") + msg)
    if not cond:
        fails.append(msg)


# --- 提取：定界符识别 ------------------------------------------------------
EXTRACT_CASES = [
    ("行内 \\(..\\)", "四元组是 \\(N\\) 与 \\(\\Sigma\\)。", 2, [False, False]),
    ("块级 $$..$$", "定义：\n\n$$L_G = \\{w \\mid w \\in \\Sigma^*\\}$$\n\n结束。", 1, [True]),
    ("方括号 \\[..\\]", "推导：\\[a^2+b^2=c^2\\] 完毕。", 1, [True]),
    ("单美元行内", "矩阵 $\\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix}$ 就这样。", 1, [False]),
    ("混合", "先 \\(x\\) 再 $$y = x^2$$ 最后 $z$。", 3, [False, True, False]),
]

# 不该被当成公式的（假阳性）
NEGATIVE_CASES = [
    ("货币金额", "实验花了 $5 到 $10 美元。"),
    ("美元符号单独出现", "成本是 $ 符号。"),
    ("无定界符的普通文本", "这就是一段没有公式的中文说明。"),
]

# --- 转换：真实课件里的硬记法 ---------------------------------------------
CONVERT_CASES = [
    ("向量下标", r"\vec{x}_0 \in V"),
    ("集合构造", r"\vec{x}_0 + U := \{\vec{x}_0 + \vec{u} \mid \vec{u} \in U\}"),
    ("矩阵 bmatrix", r"\begin{bmatrix} W_{11} & W_{21} \\ W_{12} & W_{22} \end{bmatrix}"),
    ("underbrace", r"\underbrace{a + b}_{c}"),
    ("operatorname", r"\operatorname{rank}(\tilde{W}) = n < m"),
    ("mathcal", r"\mathcal{L}_G"),
    ("mathbb 与集合差", r"\mathbb{R} \setminus \{0\}"),
    ("widehat", r"\widehat{A_\phi} = T^{-1}A_\phi S"),
    ("大求和与分式", r"L(\boldsymbol{w}) = -\sum_{n=1}^{N}\left[\sum_{j=1}^{K} p_{nj}\ln \hat{p}_{nj}\right]"),
    ("xRightarrow 星号", r"S \xRightarrow{*} w"),
    ("text 环境", r"\text{for each } n \in \{1,2,\dots,N\}"),
    ("存在否定", r"\nexists a \in \mathbb{R}"),
    ("overline 与 notin", r"\overline{\vec{x}_0 \notin U}"),
    ("CNF 产生式", r"A \to BC \quad \text{或} \quad A \to a"),
]


def main() -> int:
    verbose = "-v" in sys.argv

    print("=" * 72)
    print("0) 引擎自检")
    sc = self_check()
    check(sc["available"], f"latex2mathml 可用（engine={sc['engine']}）")
    check(sc["all_ok"], f"内置样例全通过（{sc['samples']}）")

    print("=" * 72)
    print("1) 定界符提取")
    for name, text, n_expect, blocks_expect in EXTRACT_CASES:
        spans = extract_math(text)
        got_blocks = [s["block"] for s in spans]
        check(len(spans) == n_expect, f"{name}：命中 {len(spans)} 处（期望 {n_expect}）")
        check(got_blocks == blocks_expect, f"{name}：块级标记 {got_blocks}（期望 {blocks_expect}）")

    print("=" * 72)
    print("2) 假阳性（不许把非公式当公式）")
    for name, text in NEGATIVE_CASES:
        spans = extract_math(text)
        check(len(spans) == 0, f"{name}：命中 0 处（实际 {len(spans)}）")

    print("=" * 72)
    print("3) LaTeX -> MathML（本项目课件真实出现的记法）")
    for name, tex in CONVERT_CASES:
        text = f"看这个：\\({tex}\\) 对吧。"
        out, items, fails_n = render_math(text)
        ok = len(items) == 1 and items[0]["ok"]
        check(ok, f"{name}：转换成功（失败 {fails_n}）")
        if verbose and items:
            print(f"        {items[0]['mathml'][:150]}")

    print("=" * 72)
    print("4) 占位符安全：正文里的尖括号必须被保护、MathML 不被转义")
    text = "比较 \\(a < b\\) 与 \\(c > d\\)，还有 <script> 这种正文。"
    out, items, _ = render_math(text)
    check("<script>" in out, "正文原样保留（占位符没有吃掉正文）")
    check(all(it["token"] in out for it in items), "每个公式都有占位符")
    check(all("<" not in it["token"] for it in items), "占位符本身不含尖括号")

    print("=" * 72)
    print("5) 转换失败时必须可读（不许静默丢弃）")
    bad = r"\thisIsNotACommand{x}"
    out, items, nfail = render_math(f"试试 \\({bad}\\) 结束。")
    check(len(items) == 1, "坏公式仍被识别")
    if items and not items[0]["ok"]:
        check(items[0]["mathml"] == bad.strip(), f"失败时原样返回 LaTeX：{items[0]['mathml']!r}")
    else:
        check(True, f"该引擎能处理它（也接受），ok={items[0]['ok'] if items else None}")

    print("=" * 72)
    if fails:
        print(f"结论：{len(fails)} 项未通过")
        for f in fails:
            print("  - " + f)
        return 1
    print("结论：全部通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
