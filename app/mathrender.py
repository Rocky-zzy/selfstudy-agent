# -*- coding: utf-8 -*-
r"""数学渲染：把讲解里的 LaTeX 转成浏览器能直接显示的 MathML。

用户 2026-09-21：「先做渲染，记住错题本中说的，**解决任何问题先去找有没有可以复用的东西**」。

## 选型（先找，不自己造）

| 候选 | 结论 |
|---|---|
| KaTeX（事实标准） | 是 **npm/浏览器端** JS 库；本机没有，项目惯例**不引 CDN** → 需要额外 vendoring |
| MathJax | 同上，且体积更大 |
| **`latex2mathml`（PyPI）** | ✅ **采用**。纯 Python，可离线分发；输出 MathML，**现代 Chromium/Edge 原生支持**，浏览器侧零依赖 |
| matplotlib mathtext | 只能出位图/路径，不适合网页文字排版 |

**覆盖率实测**（`docs/10` 记录）：拿本项目课件里**真实出现**的 14 类记法测，
`bmatrix` / `underbrace` / `operatorname` / `mathcal` / `mathbb` / `widehat` /
`xRightarrow` / `displaystyle` / `\text{}` / 大 `\sum` 等 **14/14 通过**。

## 边界（必须写清）

- 转换**失败**时**不静默丢弃**：把原 LaTeX 原样返回并标记 `ok=False`，
  前端显示成等宽小字（至少是可读的），**绝不显示成"符号汤"**。
- 只做渲染，**不校验数学正确性**（那是 MQI 编码 12 的事，不在这一层）。
"""

from __future__ import annotations

import re
import threading

try:
    import latex2mathml.converter as _l2m
except ImportError:  # 没装也要能降级启动，而不是整个服务起不来
    _l2m = None

# 行内 / 块级定界符。顺序重要：先长后短，先显式后隐式。
_PATTERNS: list[tuple[str, re.Pattern[str], bool]] = [
    ("dollar_block", re.compile(r"\$\$(.+?)\$\$", re.S), True),
    ("bracket_block", re.compile(r"\\\[(.+?)\\\]", re.S), True),
    ("paren_inline", re.compile(r"\\\((.+?)\\\)", re.S), False),
    # 行内 $...$：要求两侧不是数字，避免把 "$5 and $10" 当公式
    ("dollar_inline", re.compile(r"(?<![0-9$])\$(?!\s)([^$\n]+?)(?<!\s)\$(?![0-9])"), False),
]


def _convert_one(tex: str, block: bool) -> tuple[str, bool]:
    """返回 (MathML 或原 LaTeX, 是否成功)。"""
    tex = tex.strip()
    if not tex:
        return "", False
    if _l2m is None:
        return tex, False
    try:
        mathml = _l2m.convert(tex)
        if not mathml.lstrip().startswith("<math"):
            return tex, False
        if block:
            # 块级公式：让它在自己的行上居中显示
            mathml = mathml.replace(
                "<math ", '<math display="block" ', 1
            ) if 'display=' not in mathml[:80] else mathml
        return mathml, True
    except Exception:
        # 转换失败不能吞掉内容：原样返回，前端会用等宽样式显示
        return tex, False


def extract_math(text: str) -> list[dict]:
    """从讲解正文里找出所有 LaTeX 片段。

    做法：把所有定界符的匹配**全部收集**，再按
    「起点靠前优先 → 同起点时长的优先 → 块级优先」解决重叠。

    为什么不按定界符顺序逐类处理（踩过的坑）：
        先跑行内 `$...$` 时，`$$...$$` 会被它**从中间跨过去匹配**，
        导致块级公式识别失败；而且 `$5 到 $10` 这种货币金额也会被当成公式。
        所以必须"先收集、后判重叠"，并给块级更高的优先级。
    """
    cands: list[dict] = []
    for name, pat, block in _PATTERNS:
        for m in pat.finditer(text):
            s, e = m.span()
            cands.append(
                {"start": s, "end": e, "tex": m.group(1), "raw": m.group(0),
                 "block": block, "kind": name}
            )
    # 起点靠前优先；同起点时块级优先、更长的优先
    cands.sort(key=lambda c: (c["start"], 0 if c["block"] else 1, -(c["end"] - c["start"])))
    spans: list[dict] = []
    for c in cands:
        if any(c["start"] < te and ts < c["end"] for ts, te in ((x["start"], x["end"]) for x in spans)):
            continue
        spans.append(c)
    spans.sort(key=lambda x: x["start"])
    return spans


def render_math(text: str) -> tuple[str, list[dict], int]:
    """把正文里的 LaTeX 换成占位符，并返回替换表。

    返回 (带占位符的文本, [{token, mathml, ok, tex, block}], 失败数)

    为什么用占位符：前端要先把正文做 HTML 转义（防注入），
    转义会把 MathML 的尖括号吃掉。所以先换成不含特殊字符的占位符，
    转义之后再替换回来。
    """
    spans = extract_math(text)
    if not spans:
        return text, [], 0

    out = []
    prev = 0
    items: list[dict] = []
    fails = 0
    for i, sp in enumerate(spans):
        out.append(text[prev : sp["start"]])
        token = f"\u2981MATH{i}\u2981"  # 生僻括号，正文里不会自然出现
        mathml, ok = _convert_one(sp["tex"], sp["block"])
        if not ok:
            fails += 1
        items.append(
            {"token": token, "mathml": mathml, "ok": ok, "tex": sp["tex"], "block": sp["block"]}
        )
        out.append(token)
        prev = sp["end"]
    out.append(text[prev:])
    return "".join(out), items, fails


# ---------------------------------------------------------------------------
# 小缓存：同一条讲解里公式会重复，跨轮也常重复。
# 这不是"优化"，是为了让失败可复现（同一输入永远同一结果）。
# ---------------------------------------------------------------------------
_CACHE: dict[str, tuple[str, bool]] = {}
_CACHE_LOCK = threading.Lock()
_CACHE_MAX = 2000


def convert_cached(tex: str, block: bool = False) -> tuple[str, bool]:
    key = ("B:" if block else "I:") + tex
    with _CACHE_LOCK:
        hit = _CACHE.get(key)
    if hit is not None:
        return hit
    res = _convert_one(tex, block)
    with _CACHE_LOCK:
        if len(_CACHE) >= _CACHE_MAX:
            _CACHE.clear()
        _CACHE[key] = res
    return res


def self_check() -> dict:
    """自检用：报告依赖是否就绪、样例是否通过。"""
    samples = {
        "inline_vec": r"\vec{x}_0 \in V",
        "matrix": r"\begin{bmatrix} a & b \\ c & d \end{bmatrix}",
        "underbrace": r"\underbrace{a+b}_{c}",
        "operatorname": r"\operatorname{rank}(\tilde{W}) = n",
        "sum": r"\sum_{i=1}^{k}\lambda_i \vec{x}_i = \vec{0}",
        "xRightarrow": r"S \xRightarrow{*} w",
    }
    results = {}
    for name, tex in samples.items():
        _ml, ok = convert_cached(tex)
        results[name] = ok
    return {
        "engine": "latex2mathml" if _l2m is not None else None,
        "available": _l2m is not None,
        "samples": results,
        "all_ok": all(results.values()) and _l2m is not None,
    }
