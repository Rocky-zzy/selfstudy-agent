# -*- coding: utf-8 -*-
"""UI 回归测试：真实浏览器跑盲测状态机。

**为什么需要它**（这是一个真实故障留下的）：
    用户在第二次提问后点"保存评分并换到另一段"，界面卡住、不跳到 B 段。
    服务端日志显示 `/api/rate`、`/api/reveal` 全是 200 —— 问题在**前端跨轮残留状态**：
    `rate()` 把保存按钮设成 `disabled = true` 之后，下一轮 `ask()` 只清了
    `state.saved` / `state.scores`，**没有复位按钮**，于是两个按钮都点不动。
    这个 bug 用接口测试抓不到，只有真实 DOM 能看见。

防的是同一类问题：**跨轮没复位的状态**。所以断言写成"第二轮必须和新的一样可用"。

用法：
    python scripts/ui_regression_test.py             # 有头（能看着它跑）
    python scripts/ui_regression_test.py --headless
退出码：0 = 通过，1 = 失败，0 = 跳过（没装 playwright / 没浏览器时打印 SKIP）
"""

from __future__ import annotations

import argparse
import json
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))

from demo_app import flask_app  # noqa: E402

PORT = 5098
BASE = f"http://127.0.0.1:{PORT}"

failures: list[str] = []


def check(cond: bool, msg: str) -> None:
    print(("  [OK] " if cond else "  [!!] ") + msg)
    if not cond:
        failures.append(msg)


def _fake_ask() -> dict:
    """假回答刻意带 markdown 结构 + **服务端预渲染好的数学**：
    标题、围栏代码块、行内代码、列表、行内 MathML、块级 MathML。
    这样"渲染 + 数学 + 跨轮状态"三件事能一起测。"""
    INLINE = ('<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline">'
              '<mrow><mi>N</mi></mrow></math>')
    BLOCK = ('<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">'
             '<mrow><mi>L</mi><mo>=</mo><msup><mi>x</mi><mn>2</mn></msup></mrow></math>')

    def ans(slot: str, text: str, tpl: str, math: list) -> dict:
        return {"slot": slot, "model": "deepseek-chat", "text": text, "text_tpl": tpl,
                "math": math, "math_count": len(math), "math_fails": 0,
                "chars": len(text), "completion_tokens": 10, "finish_reason": "stop",
                "truncated": False, "attempts": 1, "error": None}

    a_text = """## A 段标题

非终结符 \\(N\\) 是这样。非向量化写法：

```python
c = []
for i in range(len(a)):
    c.append(a[i] + b[i])
```

向量化写法就是 `c = a + b`。

$$L = x^2$$

- 要点一
- 要点二
"""
    a_tpl = (
        "## A 段标题\n\n非终结符 \u2981MATH0\u2981 是这样。非向量化写法：\n\n"
        "```python\nc = []\nfor i in range(len(a)):\n    c.append(a[i] + b[i])\n```\n\n"
        "向量化写法就是 `c = a + b`。\n\n\u2981MATH1\u2981\n\n- 要点一\n- 要点二\n"
    )
    a_math = [
        {"token": "\u2981MATH0\u2981", "mathml": INLINE, "ok": True, "tex": "N", "block": False},
        {"token": "\u2981MATH1\u2981", "mathml": BLOCK, "ok": True, "tex": "L = x^2", "block": True},
    ]

    b_text = "## B 段标题\n\n关键在 `c = a + b` 这一行。\n\n```python\nc = a + b\n```\n"
    b_tpl = "## B 段标题\n\n关键在 `c = a + b` 这一行。\n\n```python\nc = a + b\n```\n"
    return {
        "trace_id": "uitest01",
        "question": "UI 回归测试问题",
        "lecture": None,
        "material": "ml1",
        "topic": "NumPy：向量化与数组",
        "topic_range": [7, 29],
        "mode": "whole_lecture",
        "downgrade": None,
        "pool_chars": 15867,
        "citations": [
            {"chunk_id": "ml1-p09", "lecture": None, "lecture_title": "Machine Learning I",
             "page": 9, "extraction": "pptx_text+vision", "source_file": "ML.pptx",
             "score": 8.2, "matched": ["vector"]},
        ],
        "matched_terms": ["vector"],
        "retrieval_ms": 12,
        "ctx_chars": 15867,
        "elapsed_ms": 1000,
        "model": "deepseek-chat",
        "answers": {"A": ans("A", a_text, a_tpl, a_math),
                    "B": ans("B", b_text, b_tpl, [])},
        "failed_count": 0,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--headless", action="store_true")
    ap.add_argument("--channel", default="msedge", help="msedge / chrome / chromium")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("SKIP：没装 playwright（python -m pip install playwright）")
        return 0

    threading.Thread(
        target=lambda: flask_app.run(host="127.0.0.1", port=PORT, debug=False, threaded=True),
        daemon=True,
    ).start()
    time.sleep(1.5)

    errors: list[str] = []
    js_console: list[str] = []
    sent_bodies: list[str] = []

    try:
        pw = sync_playwright().start()
    except Exception as e:
        print(f"SKIP：playwright 起不来（{str(e)[:120]}）")
        return 0

    try:
        browser = pw.chromium.launch(channel=args.channel, headless=args.headless)
    except Exception as e:
        print(f"SKIP：找不到浏览器 {args.channel!r}（{str(e)[:120]}）")
        pw.stop()
        return 0

    with browser:
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        page.on("console", lambda m: js_console.append(f"{m.type}: {m.text}")
                if m.type == "error" else None)

        def handle(route):
            url = route.request.url
            if "/api/materials" in url:
                route.fulfill(status=200, content_type="application/json", body=json.dumps({
                    "default": "ml1",
                    "materials": [
                        {"key": "ml1", "title": "ML I（UI 测试）", "temp": True,
                         "note": "测试", "exists": True, "lectures": [],
                         "topics": [{"title": "NumPy：向量化与数组", "lo": 7, "hi": 29}]},
                    ],
                }, ensure_ascii=False))
            elif "/api/ask" in url:
                sent_bodies.append(route.request.post_data or "")
                route.fulfill(status=200, content_type="application/json",
                              body=json.dumps(_fake_ask(), ensure_ascii=False))
            elif "/api/rate" in url:
                route.fulfill(status=200, content_type="application/json",
                              body=json.dumps({"ok": True, "saved": "ui"}, ensure_ascii=False))
            elif "/api/reveal" in url:
                route.fulfill(status=200, content_type="application/json", body=json.dumps({
                    "trace_id": "uitest01",
                    "labels": {"A": {"condition": "baseline", "label": "基线（无讲解方式约束）"},
                               "B": {"condition": "optimized", "label": "优化（加讲解方式约束）"}},
                }, ensure_ascii=False))
            else:
                route.continue_()

        page.route("**/api/**", handle)
        page.goto(BASE + "/", wait_until="domcontentloaded")
        page.wait_for_timeout(600)

        def snap() -> dict:
            return page.evaluate("""() => ({
                displayA: document.getElementById('card-A').style.display,
                displayB: document.getElementById('card-B').style.display,
                reveal: document.getElementById('revealbox').style.display,
                cur: state.cur,
                saved: Object.keys(state.saved).sort(),
                btnA: document.querySelector('button.save[data-slot="A"]').disabled,
                btnB: document.querySelector('button.save[data-slot="B"]').disabled,
                btnA_text: document.querySelector('button.save[data-slot="A"]').textContent,
                markA: document.getElementById('mark-A').textContent,
                markB: document.getElementById('mark-B').textContent,
                tabAOn: document.getElementById('tab-A').classList.contains('on'),
                tabBOn: document.getElementById('tab-B').classList.contains('on'),
                preCount: document.querySelectorAll('#body-A pre.code').length,
                codeText: (document.querySelector('#body-A pre.code')||{}).textContent || '',
                inlineCount: document.querySelectorAll('#body-A code.inline').length,
                h2Count: document.querySelectorAll('#body-A h2, #body-A h3').length,
                liCount: document.querySelectorAll('#body-A li').length,
                mathCount: document.querySelectorAll('#body-A math').length,
                mathBlockCount: document.querySelectorAll('#body-A .mathblock math').length,
                // 检查"替换是否真的发生"：原文是"非终结符 \(N\) 是这样"，
                // 渲染后必须是"非终结符 N 是这样"（N 由 MathML 提供）。
                // ⚠️ 不能用 indexOf('\\(') 判断——JS 字符串里 '\\(' 就是 '\('，
                //    而代码块示例里本来就有反斜杠，那样检查恒为真（踩过这个坑）。
                mathReplaced: document.getElementById('body-A').textContent.indexOf('非终结符 N 是这样') >= 0,
                mathFailCount: document.querySelectorAll('#body-A .mathfail').length,
                rawVisible: document.getElementById('rawmode').checked,
            })""")

        def round_trip(qtext: str, score_a: int, score_b: int, tag: str) -> dict:
            page.fill("#q", qtext)
            page.click("#go")
            page.wait_for_timeout(700)
            s0 = snap()
            check(s0["cur"] == "A" and s0["displayA"] == "" and s0["displayB"] == "none",
                  f"{tag}：提问后显示 A 段")
            check(not s0["btnA"] and not s0["btnB"],
                  f"{tag}：提问后两个保存按钮都可用（🔴 跨轮残留 disabled 曾导致卡住）")
            check(s0["reveal"] == "none", f"{tag}：提问后未提前揭晓")
            # 渲染：用户 2026-09-18 反馈「代码块和字体等没有做渲染，讲得很割裂」
            check(s0["preCount"] == 1, f"{tag}：围栏代码块被渲染成 <pre class=code>（{s0['preCount']} 个）")
            check("c.append(a[i] + b[i])" in s0["codeText"],
                  f"{tag}：代码内容原样保留（未被 HTML 转义或吃掉）")
            check(s0["inlineCount"] >= 1, f"{tag}：行内代码被渲染（{s0['inlineCount']} 个）")
            check(s0["h2Count"] >= 1, f"{tag}：标题被渲染（{s0['h2Count']} 个）")
            check(s0["liCount"] == 2, f"{tag}：列表被渲染（{s0['liCount']} 项）")
            # 数学：用户 2026-09-21「公式没渲染处理，一堆杂乱的符号根本看不懂」（连提三次）
            check(s0["mathCount"] == 2, f"{tag}：公式被渲染成 MathML（{s0['mathCount']} 个）")
            check(s0["mathBlockCount"] == 1,
                  f"{tag}：整行公式独立成块（{s0['mathBlockCount']} 个）")
            check(s0["mathReplaced"],
                  f"{tag}：行内公式真的被替换成了 N（不是残留的 \\(N\\)）")
            check(s0["mathFailCount"] == 0, f"{tag}：没有渲染失败的公式")

            # 新行为（2026-09-22 用户要求）：A/B 用页签**自由切换**，
            # 保存 A 之后**不再强制跳到 B**。
            page.click('.stars[data-slot="A"] button[data-score="%d"]' % score_a)
            page.click('button.save[data-slot="A"]')
            page.wait_for_timeout(900)
            s1 = snap()
            check(s1["cur"] == "A" and s1["displayA"] == "",
                  f"{tag}：保存 A 后仍停在 A（不再强制跳转）")
            check(s1["saved"] == ["A"], f"{tag}：A 记为已保存（{s1['saved']}）")
            check(s1["reveal"] == "none", f"{tag}：只打了 A 时不应揭晓")
            check("✓" in s1["markA"], f"{tag}：页签 A 显示已打分（{s1['markA']!r}）")
            check("未打分" in s1["markB"], f"{tag}：页签 B 仍显示未打分（{s1['markB']!r}）")

            # 页签自由切换（**在任何时候都能切**，包括未打分时）
            page.click("#tab-B")
            page.wait_for_timeout(300)
            t1 = snap()
            check(t1["cur"] == "B" and t1["displayB"] == "" and t1["displayA"] == "none",
                  f"{tag}：点页签 B 就能切过去")
            page.click("#tab-A")
            page.wait_for_timeout(300)
            t2 = snap()
            check(t2["cur"] == "A" and t2["displayA"] == "",
                  f"{tag}：再点页签 A 能切回来（来回对比）")

            page.click("#tab-B")
            page.wait_for_timeout(200)
            page.click('.stars[data-slot="B"] button[data-score="%d"]' % score_b)
            page.click('button.save[data-slot="B"]')
            page.wait_for_timeout(900)
            s2 = snap()
            check(s2["saved"] == ["A", "B"], f"{tag}：A/B 都已保存（{s2['saved']}）")
            check(s2["reveal"] == "block", f"{tag}：两段都打完后揭晓")
            return s2

        print("=" * 72)
        print("第 1 轮：完整走一遍")
        round_trip("UI 测试第一问", 4, 2, "第1轮")

        print("=" * 72)
        print("第 2 轮：复现原故障场景（第二次提问后必须仍然可用）")
        s = round_trip("UI 测试第二问", 5, 3, "第2轮")
        check(s["btnA_text"] == "已保存", f"第2轮结束后 A 按钮显示已保存（{s['btnA_text']!r}）")

        print("=" * 72)
        print("第 3 轮：连问两次都不打分（不应残留状态）")
        page.fill("#q", "第三问")
        page.click("#go")
        page.wait_for_timeout(700)
        page.fill("#q", "第四问")
        page.click("#go")
        page.wait_for_timeout(700)
        s3 = snap()
        check(not s3["btnA"] and not s3["btnB"], "连问不答后两个按钮仍可用")
        check(s3["saved"] == [], "连问不答后 saved 为空")
        check(s3["cur"] == "A", "连问不答后回到 A 段")

        print("=" * 72)
        print("第 4 轮：「看原文」开关（渲染态与原文态都要能取回纯文本）")
        page.fill("#q", "渲染开关测试")
        page.click("#go")
        page.wait_for_timeout(700)
        rendered = page.evaluate("() => document.querySelectorAll('#body-A pre.code').length")
        page.check("#rawmode")
        page.wait_for_timeout(300)
        raw_pre = page.evaluate("() => document.querySelectorAll('#body-A pre.code').length")
        raw_text = page.evaluate("() => document.getElementById('body-A').textContent")
        check(rendered == 1, "渲染态：有 <pre class=code>")
        check(raw_pre == 0, "原文态：不再是渲染结构，只有纯文本")
        check("```python" in raw_text, "原文态：能看到模型原始输出的围栏标记")
        check("c.append(a[i] + b[i])" in raw_text, "原文态：代码内容完整")
        page.uncheck("#rawmode")
        page.wait_for_timeout(300)
        check(page.evaluate("() => document.querySelectorAll('#body-A pre.code').length") == 1,
              "切回渲染态：结构恢复")

        check(not errors, f"无 JS 异常（{errors or '无'}）")
        check(not js_console, f"无 console error（{js_console or '无'}）")

        print("=" * 72)
        print("第 5 轮：讲法下拉框必须真的传到后端")
        import json as _json
        bodies = [_json.loads(b) for b in sent_bodies if b]
        check(bool(bodies), f"捕获到 {len(bodies)} 次 /api/ask 请求体")
        check(all(b.get("teaching") for b in bodies), "每次请求都带 teaching 字段")
        check(bodies[0].get("teaching") == "brief", f"默认讲法是 brief（实际 {bodies[0].get('teaching')}）")
        page.select_option("#teaching", "detailed")
        page.fill("#q", "讲法切换测试")
        page.click("#go")
        page.wait_for_timeout(700)
        last = _json.loads(sent_bodies[-1])
        check(last.get("teaching") == "detailed",
              f"选「详细」后请求带 teaching=detailed（实际 {last.get('teaching')}）")
        page.select_option("#teaching", "followup")
        page.fill("#q", "讲法切换测试2")
        page.click("#go")
        page.wait_for_timeout(700)
        last = _json.loads(sent_bodies[-1])
        check(last.get("teaching") == "followup",
              f"选「追问」后请求带 teaching=followup（实际 {last.get('teaching')}）")

    pw.stop()
    print("=" * 72)
    if failures:
        print(f"结论：{len(failures)} 项未通过")
        for f in failures:
            print("  - " + f)
        return 1
    print("结论：全部通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
