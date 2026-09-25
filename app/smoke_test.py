# -*- coding: utf-8 -*-
"""步骤 1 的冒烟测试：验证最小闭环真的通，而不是"看起来能跑"。

用法：
    python app/smoke_test.py            # 含一次真实模型调用（两条件各一次）
    python app/smoke_test.py --no-model # 只测检索与接口，不花钱

检查项（对应错题本里的坑）：
  读写同一份数据结构，先打印一条真实记录 -> 打印 citations / 首个评分行
  finish_reason == 'length' 截断检测     -> 断言未被静默截断
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
ROOT = APP_DIR.parent
sys.path.insert(0, str(APP_DIR))

from demo_app import DATA_DIR, RATINGS_PATH, flask_app, load_dotenv  # noqa: E402
from generator import GenConfig  # noqa: E402

OK, BAD = "  [OK] ", "  [!!] "
fails: list[str] = []


def check(cond: bool, msg: str) -> None:
    print((OK if cond else BAD) + msg)
    if not cond:
        fails.append(msg)


def main() -> int:
    no_model = "--no-model" in sys.argv
    load_dotenv(ROOT / ".env")
    cfg = GenConfig.from_env()

    print("=" * 72)
    print("1) 知识库与检索")
    from retrieval import build_context, load_chunks, search

    chunks = load_chunks()
    check(len(chunks) == 128, f"chunks.jsonl 读到 {len(chunks)} 条（期望 128）")
    q = "什么是仿射空间？它和向量空间差在哪？"

    # 回归：起步默认整讲直灌。L01 全讲必须含 p8 —— p8 是全讲唯一给出
    # 「仿射映射」定义的一页，纯词面检索命不中它（只有 282 字符、不含 "affine space"），
    # 于是"问了仿射空间、却漏掉讲仿射映射的那一页"。这条断言防止该问题无声复发。
    sel_whole = search(q, chunks, lecture="L01", whole_lecture=True)
    ids_whole = [c.chunk_id for c in sel_whole]
    check(len(sel_whole) == 8, f"整讲模式返回 {len(sel_whole)} 页（L01 共 8 页）")
    check("l01-p08" in ids_whole, "整讲模式包含 l01-p08（仿射映射定义所在页）")

    sel = search(q, chunks, lecture="L01", top_k=3)
    check(1 <= len(sel) <= 5, f"命中页模式返回 {len(sel)} 页（上限 top_k+2=5）")
    check(all(c.chunk_id.startswith("l01-") for c in sel), "返回的页全部属于 L01")
    ctx = build_context(sel)
    check(len(ctx) > 1000, f"拼出的课件原文 {len(ctx)} 字符")
    print("     命中页模式 citations:", [f"{c.chunk_id}(s={round(c.score,1)})" for c in sel])
    ctx_whole = build_context(sel_whole)
    # 直接验真正关心的不变量，不猜分隔符常数：
    #   ① 每一页的正文都完整在场（build_context 只加来源标记、不改写内容）
    #   ② 每一页都有来源标记（可追溯到文件+页码）
    missing = [c.chunk_id for c in sel_whole if c.text.strip() not in ctx_whole]
    check(not missing, f"整讲上下文包含全部 8 页正文（缺失：{missing or '无'}）")
    check(all(f"<<<PAGE {c.chunk_id}" in ctx_whole for c in sel_whole),
          "整讲上下文里每一页都有来源标记")
    check(len(ctx_whole) < 16000, f"整讲上下文 {len(ctx_whole)} 字符，没有异常膨胀")

    # 桥接机制：命中页之间的缺页要补上，命中页之外的页不要乱加
    bridge_sel = search("why is the kernel a subspace", chunks, lecture="L01", top_k=3)
    bpages = [c.page for c in bridge_sel]
    check(len(bpages) <= 5, f"桥接后页数 {bpages} 不超过 top_k+2")
    check(bpages == sorted(bpages), "返回页按页码有序")

    print("=" * 72)
    print("2) 提示词：差异只在条件专属约束；范围/格式/讲法三档两条件必须完全相同")
    from generator import DEFAULT_TEACHING, TEACHING_LABEL, TEACHING_MODES, system_prompt_for, user_prompt

    s_base = system_prompt_for("baseline")
    s_opt = system_prompt_for("optimized")
    check(s_base != s_opt, "baseline 与 optimized 的系统指令不同")
    # 用户 2026-09-17 要求：输出范围约束两条件共用，
    # 否则优化版可能仅因"写得短"而赢，分不出是讲得好还是讲得短。
    for kw in ("只回答学生问到的那个点", "不要分章节"):
        check(kw in s_base and kw in s_opt, f"范围约束两条件都在：「{kw}」")
    # 用户 2026-09-18 要求：格式约束也两条件共用（呈现层问题，不是教学质量）
    for kw in ("围栏代码块", "LaTeX"):
        check(kw in s_base and kw in s_opt, f"格式约束两条件都在：「{kw}」")
    # 用户 2026-09-19 要求：讲法三档，两条件共用（讲多全属于决策层，不参与对照）
    for t in TEACHING_MODES:
        b = system_prompt_for("baseline", teaching=t)
        o = system_prompt_for("optimized", teaching=t)
        label = TEACHING_LABEL[t]
        check(f"怎么讲：{label}" in b and f"怎么讲：{label}" in o,
              f"讲法「{label}」两条件都在（{t}）")
    check("600–800 字" in system_prompt_for("optimized", teaching="brief"),
          "概览档仍保留 600–800 字上限")
    d_opt = system_prompt_for("optimized", teaching="detailed")
    for kw in ("范围内一个都不许漏", "只讲课件里有的", "代码逐行注释", "不设字数上限"):
        check(kw in d_opt, f"详细档含约束：「{kw}」")
    # 2026-09-22：详细档改为**教学骨架**。骨架部件必须在**两条件**里都在
    # （讲法两条件共用，基线也必须拿到同一套骨架，否则"讲多全"会变成变量）。
    SKELETON = ("是什么", "为什么需要它", "直觉", "形式表达", "怎么做",
                "例子", "算出来怎么看", "常见的坑", "什么时候用")
    d_base = system_prompt_for("baseline", teaching="detailed")
    for kw in SKELETON:
        check(kw in d_opt and kw in d_base, f"骨架部件两条件都在：「{kw}」")
    # 骨架取代了"设问"：实测抓到模板化设问会产生"问题与答案不一致"的段落
    # （CNF 那问；Rubrik 判 Coherence=No、MQI 判编码 13=1），所以详细档已移出设问约束。
    check("设问" not in d_opt,
          "详细档不再有「设问」约束（已由骨架的『为什么需要它』『每一步为什么』取代）")
    check("设问" in system_prompt_for("optimized", teaching="followup"),
          "追问档仍保留设问（追问场景没有骨架可依）")
    # 骨架的"逐段讲全"与专属约束的"不重复"必须能共存，否则两条会打架
    check("不冲突" in d_opt, "optimized 明确说明「骨架走一遍」与「不重复」不冲突")
    check("600–800 字" not in d_opt, "详细档**不再有**字数上限（这是用户定义的核心）")
    # 约束编号必须**连续唯一**。曾经出过两个问题：拼起来有两个"13"（撞号）、
    # brief 档 11→22（断号）。现在各块只写 `- ` 占位符，由 number_constraints 统一编号，
    # 这条断言就是防止有人又把编号手写回去。
    import re as _re
    for _t in TEACHING_MODES:
        for _c in ("baseline", "optimized"):
            _s = system_prompt_for(_c, teaching=_t)
            _nums = [int(m) for m in _re.findall(r"^(\d+)\. ", _s, _re.M)]
            check(_nums == list(range(1, len(_nums) + 1)),
                  f"约束编号连续唯一（{_t}/{_c}：{len(_nums)} 条）")
    # 术语首现给白话：**两条件共用**（呈现层问题，只给一侧会变成"谁加注谁赢"）
    for _t in TEACHING_MODES:
        for _c in ("baseline", "optimized"):
            _s = system_prompt_for(_c, teaching=_t)
            check("第一次出现时落地" in _s, f"术语约束两条件都在（{_t}/{_c}）")
    check("构造（成分）" in d_opt or "constituent（成分）" in d_opt,
          "术语约束给了 `English（中文）` 的示例格式")
    check("讲 why" not in s_base and "讲 why" in s_opt, "「讲 why」只在 optimized（条件专属）")
    check("课件里真实存在的内容" in s_base,
          "追问推荐必须绑定课件（实测推荐过课件外的问题，见 docs/07 第 8 条）")
    check(DEFAULT_TEACHING in TEACHING_MODES, f"默认讲法合法（{DEFAULT_TEACHING}）")

    # L0 知识结构挂载（2026-09-23）。契约有三条，都要锁住：
    #   ① 问了某个知识点，**那个节点必须在注入里**（第一版按"页命中"选，曾把目标挤掉）；
    #   ② 注入内容两条件完全相同（它在 user prompt 的课件原文里，不参与对照）；
    #   ③ 命中不了目标就**不注入**，不要塞一堆无关节点。
    print("-" * 72)
    print("2b) L0 知识结构挂载")
    from graph_inject import GraphError, build_injection, load_graph, wrap
    try:
        _g = load_graph("L01")
        check(True, f"载入知识结构 L01（{len(_g['nodes'])} 个节点）")
        _inj, _ids = build_injection(
            _g, ["l01-p01", "l01-p02", "l01-p03", "l01-p04", "l01-p05", "l01-p06", "l01-p07", "l01-p08"],
            "基变换的矩阵 T^{-1}A_φS 是怎么推出来的？")
        check("basis_change" in _ids,
              f"问「基变换」时 basis_change 被注入（实际 {_ids[:3]}）")
        check(_ids and _ids[0] == "basis_change",
              "目标节点排在注入列表第一位")
        check("换到标准基" in _inj and "施加线性映射" in _inj and "换到目标基" in _inj,
              "子目标标签进入注入文本（Morrison 等 2020：给标签优于自己生成）")
        check("课件没交代" in _inj, "子目标的『课件没交代』提示进入注入文本")
        _inj2, _ids2 = build_injection(_g, ["l01-p03"], "你喜欢什么颜色？")
        check(not _ids2 or "basis_change" not in _ids2,
              "与知识结构无关的问题**不注入**目标节点")
        check(wrap("x").startswith("<<<KNOWLEDGE-STRUCTURE>>>"),
              "注入块有独立标记（便于事后核对）")
    except GraphError as e:
        check(False, f"知识结构加载失败：{e}")
    up = user_prompt(ctx, q)
    check("<<<COURSEWARE>>>" not in up and "<<<STUDENT QUESTION>>>" not in up,
          "占位符已被替换（无残留 <<<...>>>）")
    check(q in up, "学生问题已进入 user prompt")
    check(ctx[:200] in up, "课件原文已进入 user prompt（两条件共用）")
    check("不等于你这次要讲的范围" in up, "user prompt 明确区分「输入范围」与「输出范围」")
    for t in TEACHING_MODES:
        st = system_prompt_for("optimized", strip_opt_constraints=True, teaching=t)
        check(st == system_prompt_for("baseline", teaching=t),
              f"APP_STRIP_OPT 关掉优化约束后与 baseline 同指令（{t}）")
    try:
        system_prompt_for("baseline", teaching="nope")
        check(False, "非法讲法应当报错")
    except ValueError:
        check(True, "非法讲法被拒绝（不静默退回默认档）")

    print("=" * 72)
    print("3) Flask 接口（test client，不开端口）")
    flask_app.config["DRY_RUN"] = True
    cli = flask_app.test_client()
    r = cli.get("/")
    check(r.status_code == 200 and b"<title>" in r.data, f"GET / -> {r.status_code}")
    body = r.data.decode("utf-8")
    check("自由切换" in body, "首页含 A/B 自由切换的说明")
    check('id="tab-A"' in body and 'id="tab-B"' in body, "首页含 A/B 页签（可自由切换对比）")
    check("基线" not in body and "优化（" not in body,
          "首页 HTML 里不含条件名（盲测：不能从前端看出哪个是哪个）")

    r = cli.post("/api/ask", json={"question": q, "lecture": "L01", "top_k": 3, "whole_lecture": False, "material": "kb"})
    check(r.status_code == 200, f"POST /api/ask (dry-run, 命中页) -> {r.status_code}")
    d = r.get_json() or {}
    check(bool(d.get("trace_id")), "返回 trace_id")
    check(len(d.get("citations", [])) == len(sel), "dry-run 的 citations 与检索一致")
    check(d.get("mode") == "hit_pages", f"mode 标记正确（{d.get('mode')}）")
    check(d.get("dry_run") is True, "dry-run 标记正确")

    # 不传 whole_lecture 时必须是整讲（起步默认值，UI 依赖它）。
    # 这里显式 use_graph=False：这条断言只测"检索拼出的整讲上下文"，
    # 不该把知识结构注入的字数算进去（那是另一条断言的事）。
    r = cli.post("/api/ask", json={"question": q, "lecture": "L01", "material": "kb", "use_graph": False})
    d2 = r.get_json() or {}
    check(d2.get("mode") == "whole_lecture", f"默认走整讲（{d2.get('mode')}）")
    check(len(d2.get("citations", [])) == 8, f"默认整讲返回 {len(d2.get('citations', []))} 页")
    check(d2.get("ctx_chars") == len(ctx_whole), f"默认整讲上下文 {d2.get('ctx_chars')} 字符与本地一致")

    r = cli.post("/api/ask", json={"question": "   ", "material": "kb"})
    check(r.status_code == 400, f"空问题被拒 -> {r.status_code}")

    # 评分：trace 不匹配必须被拒（防止答非所问地把分记到上一次）
    r = cli.post("/api/rate", json={"trace_id": "deadbeef", "slot": "A", "score": 5})
    check(r.status_code == 409, f"过期 trace_id 被拒 -> {r.status_code}")

    r = cli.post("/api/rate", json={"trace_id": d.get("trace_id"), "slot": "Z", "score": 5})
    check(r.status_code == 400, f"非法 slot 被拒 -> {r.status_code}")

    r = cli.post("/api/rate", json={"trace_id": d.get("trace_id"), "slot": "A", "score": 9})
    check(r.status_code == 400, f"越界 score 被拒 -> {r.status_code}")

    r = cli.get("/api/stats")
    check(r.status_code == 200, f"GET /api/stats -> {r.status_code}")

    print("-" * 72)
    print("3b) 临时素材（Machine Learning I，**不得进 knowledge_base/**）")
    r = cli.get("/api/materials")
    mats = {m["key"]: m for m in (r.get_json() or {}).get("materials", [])}
    check("kb" in mats and "ml1" in mats, f"素材清单含 kb 与 ml1（{sorted(mats)}）")
    check(mats["ml1"]["temp"] is True, "ml1 被标为 temp（临时素材）")
    kb_path = (ROOT / "knowledge_base" / "chunks.jsonl")
    ml1_path = ROOT / "temp_material" / "ml1" / "chunks.jsonl"
    check(ml1_path.exists(), f"临时素材存在：{ml1_path.relative_to(ROOT)}")
    # 物理隔离：临时素材的 chunk 绝不能出现在知识库里
    kb_text = kb_path.read_text(encoding="utf-8")
    check("ml1-p" not in kb_text, "知识库里没有 ml1 的 chunk（临时素材未混入）")
    check("temp_material" not in kb_text, "知识库里没有指向 temp_material 的引用")
    check(len(mats["ml1"]["topics"]) == 5, f"ml1 登记了 {len(mats['ml1']['topics'])} 个分区")
    check(mats["ml1"]["lectures"] and mats["ml1"]["lectures"][0]["pages"] == 83,
          "ml1 登记为 83 页")

    for ti, t in enumerate(mats["ml1"]["topics"]):
        r = cli.post("/api/ask", json={
            "question": "什么是向量化？为什么它更快？", "material": "ml1",
            "topic": ti, "whole_lecture": True, "top_k": 4})
        dd = r.get_json() or {}
        check(r.status_code == 200, f"分区 {ti}（{t['title']}）-> {r.status_code}")
        check(dd.get("topic") == t["title"], f"分区 {ti} 回传了分区名")
        check(len(dd.get("citations", [])) == t["hi"] - t["lo"] + 1,
              f"分区 {ti} 命中 {len(dd.get('citations', []))} 页（应为 p{t['lo']}–p{t['hi']}）")
        check(dd.get("downgrade") is None,
              f"分区 {ti} 未被降级（{dd.get('ctx_chars')} 字符 < 上限）")
        print(f"     分区 {ti}: {t['title']}  p{t['lo']}–p{t['hi']}  "
              f"{len(dd.get('citations', []))} 页 / {dd.get('ctx_chars')} 字符")

    r = cli.post("/api/ask", json={"question": "x", "material": "ml1", "topic": 99})
    check(r.status_code == 400, f"越界 topic 被拒 -> {r.status_code}")
    r = cli.post("/api/ask", json={"question": "x", "material": "nope"})
    check(r.status_code == 400, f"未知素材被拒 -> {r.status_code}")

    print("-" * 72)
    print("3c) 第二份临时素材（AIAA 4051 L6；该 PDF 正文残缺、关键定义在图里）")
    mats = {m["key"]: m for m in (cli.get("/api/materials").get_json() or {}).get("materials", [])}
    check("nlp6" in mats, f"素材清单含 nlp6（{sorted(mats)}）")
    nlp_path = ROOT / "temp_material" / "nlp6" / "chunks.jsonl"
    check(nlp_path.exists(), f"nlp6 素材存在：{nlp_path.relative_to(ROOT)}")
    check("nlp6-p" not in kb_text, "知识库里没有 nlp6 的 chunk（隔离成立）")
    check(len(mats["nlp6"]["topics"]) == 4, f"nlp6 登记了 {len(mats['nlp6']['topics'])} 个分区")
    rows_nlp = [json.loads(x) for x in nlp_path.read_text(encoding="utf-8").splitlines() if x.strip()]
    check(len(rows_nlp) == 31, f"nlp6 共 {len(rows_nlp)} 页")
    # 核心回归：p7 的 CFG 定义**只存在于图里**，文本层是空的，必须靠转写补回
    p07 = next(x for x in rows_nlp if x["page"] == 7)
    for kw in ("non-terminal", "terminal symbols", "start symbol", "Derivations"):
        check(kw in p07["text"], f"nlp6 p07 含图内定义「{kw}」（文本层里没有）")
    # 去重回归：同一内容不许贴两遍（redundancy 有害，且会污染"全讲"判断）
    p21 = next(x for x in rows_nlp if x["page"] == 21)
    check(p21["text"].count("dynamic programming (DP) algorithm") == 1,
          "nlp6 p21 同一内容只出现一次（去重生效）")
    for ti, t in enumerate(mats["nlp6"]["topics"]):
        r = cli.post("/api/ask", json={
            "question": "什么是上下文无关文法？", "material": "nlp6",
            "topic": ti, "whole_lecture": True, "teaching": "detailed"})
        dd = r.get_json() or {}
        check(r.status_code == 200, f"nlp6 分区 {ti}（{t['title']}）-> {r.status_code}")
        check(dd.get("downgrade") is None,
              f"nlp6 分区 {ti} 未被降级（{dd.get('ctx_chars')} 字符）")

    print("-" * 72)
    print("3d) 主数据集（Rosen 第 1 章 逻辑与证明，**不进 knowledge_base/**）")
    mats = {m["key"]: m for m in (cli.get("/api/materials").get_json() or {}).get("materials", [])}
    check("rosen-ch1" in mats, f"素材清单含 rosen-ch1（{sorted(mats)}）")
    rosen_path = ROOT / "data" / "rosen" / "ch1" / "chunks.jsonl"
    check(rosen_path.exists(), f"主数据集存在：{rosen_path.relative_to(ROOT)}")
    check("rosen" not in kb_text, "知识库里没有 rosen 的 chunk（隔离成立）")
    rows_r = [json.loads(x) for x in rosen_path.read_text(encoding="utf-8").splitlines() if x.strip()]
    check(len(rows_r) == 120, f"rosen-ch1 共 {len(rows_r)} 页（1.1–1.8）")
    # 页号守恒：解析器曾因"左右页页眉不对称"漏掉整半本书（见 docs/00 M13），
    # 所以这里必须有守恒检查——数字对不上先怀疑解析器。
    # 注意两个页号不是一回事：page=PDF 页（24–143），printed_page=书上印的页（1–120）。
    check(sorted(x["printed_page"] for x in rows_r) == list(range(1, 121)),
          "rosen-ch1 书上页码连续 1–120")
    check(all(x["page"] == x["printed_page"] + 23 for x in rows_r),
          "rosen-ch1 全部满足 PDF 页 = 书上页 + 23")
    secs = {}
    for x in rows_r:
        secs[x["lecture"]] = secs.get(x["lecture"], 0) + 1
    check(len(secs) == 8, f"rosen-ch1 分 8 节（{sorted(secs)}）")
    check(all(v > 0 for v in secs.values()), f"每节都有页：{secs}")
    check(len(mats["rosen-ch1"]["lectures"]) == 8,
          f"rosen-ch1 登记了 {len(mats['rosen-ch1']['lectures'])} 节")
    # 该素材没有 topics 分区（每节 38k–93k 字符，靠 topic 切页区间没有意义），
    # 学习单位就是节：用 lecture 选节。
    check(len(mats["rosen-ch1"]["topics"]) == 0, "rosen-ch1 不登记 topics（按节选）")
    for lec in [l["lecture"] for l in mats["rosen-ch1"]["lectures"]]:
        r = cli.post("/api/ask", json={
            "question": "什么是命题？", "material": "rosen-ch1",
            "lecture": lec, "whole_lecture": True, "top_k": 4, "use_graph": False})
        dd = r.get_json() or {}
        check(r.status_code == 200, f"rosen {lec} -> {r.status_code}")
        check(dd.get("error") is None, f"rosen {lec} 无错误（{dd.get('error')}）")
        check(dd.get("lecture") == lec, f"rosen {lec} 回传了节号（{dd.get('lecture')}）")
        # 本节实测 38k–93k 字符 > WHOLE_LECTURE_CHAR_LIMIT(20000)，
        # 所以"整节"必然被降级成命中页——这是**已知行为**，断言它被明确告知（有 downgrade 文案），
        # 而不是断言"没降级"（那是愿望，不是当前行为）。
        check(bool(dd.get("downgrade")) or dd.get("ctx_chars", 0) <= 20000,
              f"rosen {lec} 要么未降级、要么明确告知降级（{dd.get('ctx_chars')} 字符）")
        print(f"     {lec}: 命中 {len(dd.get('citations', []))} 页 / "
              f"{dd.get('ctx_chars')} 字符 / 降级={bool(dd.get('downgrade'))}")

    if no_model:
        print("=" * 72)
        print("--no-model：跳过真实模型调用")
        return report(fails)

    print("=" * 72)
    print("4) 真实模型调用（两条件各一次，串行以便看清差异）")
    if not cfg.api_key:
        check(False, "没有 DEEPSEEK_API_KEY，无法测模型链路")
        return report(fails)

    flask_app.config["DRY_RUN"] = False
    t0 = time.time()
    r = cli.post("/api/ask", json={"question": q, "lecture": "L01", "top_k": 3, "material": "kb"})
    dt = time.time() - t0
    check(r.status_code == 200, f"POST /api/ask (真实模型) -> {r.status_code}  {dt:.1f}s")
    d = r.get_json() or {}
    if d.get("error"):
        check(False, f"模型调用失败：{d['error']}")
        return report(fails)

    answers = d.get("answers", {})
    check(set(answers) == {"A", "B"}, f"返回 A/B 两个槽位（{sorted(answers)}）")
    # 盲测的关键：HTTP 响应里不能出现条件名
    raw = json.dumps(d, ensure_ascii=False)
    check("baseline" not in raw, "响应里不出现 'baseline'（盲测不泄露标签）")
    check("optimized" not in raw, "响应里不出现 'optimized'（盲测不泄露标签）")

    for slot in ("A", "B"):
        aa = answers.get(slot) or {}
        txt = aa.get("text") or ""
        check(bool(txt), f"槽位 {slot}: 拿到讲解 {len(txt)} 字符")
        check(aa.get("error") is None, f"槽位 {slot}: 无错误（{aa.get('error')}）")
        check(aa.get("finish_reason") != "length" and not aa.get("truncated"),
              f"槽位 {slot}: 未被截断（finish_reason={aa.get('finish_reason')}）")
        # 用户 2026-09-17：一次读两段 1.5k–2.2k 字太重。范围约束是否收住了长度？
        # 实测（见 docs/05 §六）：**软约束，收不住**。多轮实测 1049 / 1055 / 1176 / 1888 字符，
        # 目标写的是 600–800，实际常超。所以这里只断言"没有回到整章串讲那个量级"，
        # **不**断言 600–800（那是愿望，不是当前行为；按愿望写断言只会得到假红灯）。
        check(len(txt) < 2400, f"槽位 {slot}: 输出 {len(txt)} 字符（未回到整章串讲量级）")
        if len(txt) > 900:
            print(f"     ⚠️ 槽位 {slot} 超出 600–800 字目标（实际 {len(txt)}）——软约束，已知会超")
        print(f"     {slot}: {len(txt)} 字, {aa.get('completion_tokens')} tok, "
              f"{aa.get('attempts')} 次尝试")
        print("     ---- 开头 200 字 ----")
        print("     " + txt[:200].replace("\n", "\n     "))

    check((answers["A"].get("text") or "") != (answers["B"].get("text") or ""),
          "两槽位产出不同文本（否则说明差异没生效，是最严重的静默失败）")

    print("=" * 72)
    print("5) 盲测流程 + 评分落盘（真实写一条，再读回验证）")
    if RATINGS_PATH.exists():
        before = RATINGS_PATH.read_text(encoding="utf-8").count("\n")
    else:
        before = 0

    # 打分前不许揭晓
    r = cli.post("/api/reveal", json={"trace_id": d["trace_id"]})
    labels = (r.get_json() or {}).get("labels", {})
    check(set(labels) == {"A", "B"}, "reveal 能返回 A/B 的标签")
    slot_of = {s: labels[s]["condition"] for s in labels}
    check(sorted(slot_of.values()) == ["baseline", "optimized"], f"A/B 覆盖两个条件（{slot_of}）")

    # 按槽位打分（模拟盲测：A、B 各一条）
    for slot in ("A", "B"):
        r = cli.post(
            "/api/rate",
            json={
                "trace_id": d["trace_id"],
                "slot": slot,
                "score": 3,
                "reason": f"[smoke test] 槽位 {slot} 的验证记录",
            },
        )
        check(r.status_code == 200, f"POST /api/rate slot={slot} -> {r.status_code}")

    check(RATINGS_PATH.exists(), f"评分文件已生成：{RATINGS_PATH}")
    lines = [l for l in RATINGS_PATH.read_text(encoding="utf-8").splitlines() if l.strip()]
    check(len(lines) == before + 2, f"行数 {before} -> {len(lines)}")
    last_two = [json.loads(l) for l in lines[-2:]]
    check({r_["slot"] for r_ in last_two} == {"A", "B"}, "两行分别记了槽位 A、B")
    check(
        {r_["condition"] for r_ in last_two} == {"baseline", "optimized"},
        "两行落盘时各自还原出了真实条件",
    )
    check(all(r_.get("blind") is True for r_ in last_two), "两行都标了 blind=True")
    check(all(bool(r_["answer"]) for r_ in last_two), "评分行里带上了对应的讲解原文（可回溯）")
    check(
        all(r_["citations"] == [c["chunk_id"] for c in d["citations"]] for r_ in last_two),
        "评分行里带上了引用页",
    )
    print("     最后两行（先打印真实记录，再断言）:")
    for r_ in last_two:
        print("     " + json.dumps(
            {k: (v[:60] + "…" if isinstance(v, str) and len(v) > 60 else v) for k, v in r_.items()},
            ensure_ascii=False,
        ))

    print("=" * 72)
    print("6) 统计口径只报分布，不下结论")
    r = cli.get("/api/stats")
    st = r.get_json() or {}
    check(st.get("n", 0) >= 2, f"/api/stats 记到 {st.get('n')} 条")
    print("     " + json.dumps(st.get("by_condition", {}), ensure_ascii=False)[:400])
    print(f"     数据目录：{DATA_DIR}")

    return report(fails)


def report(fails: list[str]) -> int:
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
