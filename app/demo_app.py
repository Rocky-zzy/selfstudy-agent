# -*- coding: utf-8 -*-
"""最小闭环：课件 → 检索相关页 → LLM 生成讲解 → 用户读 → 打满意度分。

本文件对应 docs/00_错题本.md §四「步骤 1」。刻意做小：
一次提问 → 同一批检索页 → 两个条件的讲解并排出 → 各打一次分。

启动：
    python app/demo_app.py            # 需要 .env 里 DEEPSEEK_API_KEY
    python app/demo_app.py --dry-run  # 只跑检索，不调模型（验通路）
打开 http://127.0.0.1:5000
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import threading
import time
import uuid
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template, request

APP_DIR = Path(__file__).resolve().parent
ROOT = APP_DIR.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from generator import (  # noqa: E402
    DEFAULT_TEACHING,
    TEACHING_LABEL,
    TEACHING_MODES,
    GenConfig,
    generate,
)
from retrieval import build_context, list_lectures, load_chunks, search  # noqa: E402
from mathrender import render_math  # noqa: E402
from graph_inject import GraphError, build_injection, load_graph, wrap  # noqa: E402

DATA_DIR = ROOT / "data"
RATINGS_PATH = DATA_DIR / "ratings.jsonl"

# ---------------------------------------------------------------------------
# 素材登记表。**临时素材与知识库物理隔离**：
#   kb  → knowledge_base/chunks.jsonl（AIAA 2711，正式资产）
#   ml1 → temp_material/ml1/chunks.jsonl（Machine Learning I，用户 2026-09-17
#         明确说明"只是临时测试样本，不要进知识库"）
# 临时素材只是**换一条读取路径**，检索/生成/打分逻辑完全相同——
# 不为它单开一套代码。
# ---------------------------------------------------------------------------
MATERIALS: dict[str, dict] = {
    "kb": {
        "key": "kb",
        "title": "AIAA 2711 课件（知识库）",
        "path": ROOT / "knowledge_base" / "chunks.jsonl",
        "temp": False,
        "note": "13 PDF / 132 页 / 128 chunks。正式资产。",
    },
    "ml1": {
        "key": "ml1",
        "title": "Machine Learning I.pptx（临时素材）",
        "path": ROOT / "temp_material" / "ml1" / "chunks.jsonl",
        "temp": True,
        "note": "83 页课件，代码为截图、需视觉转写。**不进知识库**。",
        # 这份课件天然分 5 块。分区就是**页区间**，不另造切分逻辑；
        # 整份 51.5k 字符太大，按块学才符合"一个知识点一个知识点来"。
        "topics": [
            {"title": "NumPy：向量化与数组", "lo": 7, "hi": 29},
            {"title": "SciPy：优化 / 线代 / 统计 / 稀疏", "lo": 30, "hi": 39},
            {"title": "Pandas：Series / DataFrame / GroupBy", "lo": 40, "hi": 52},
            {"title": "Matplotlib & Seaborn：可视化", "lo": 53, "hi": 62},
            {"title": "机器学习基础：四类 ML 与工作流", "lo": 63, "hi": 83},
        ],
    },
    "nlp6": {
        "key": "nlp6",
        "title": "AIAA 4051 L6 · Grammar and Syntax（临时素材）",
        "path": ROOT / "temp_material" / "nlp6" / "chunks.jsonl",
        "temp": True,
        "note": "31 页 PDF。**关键定义在图里**（如 p7 的 CFG 四元组文本层是空的），已整页渲染转写。**不进知识库**。",
        # 分区=页区间（不另造切分逻辑）。每块 7–8 页，保证「详细」档能把整块喂进去
        "topics": [
            {"title": "语法基础与浅层句法（n-gram / HMM / 成分）", "lo": 1, "hi": 6},
            {"title": "上下文无关文法 CFG 的结构", "lo": 7, "hi": 14},
            {"title": "句法分析：自顶向下 / 自底向上 / 歧义", "lo": 15, "hi": 20},
            {"title": "CYK 算法：动态规划与 CNF 转换", "lo": 21, "hi": 31},
        ],
    },
    "rosen-ch1": {
        "key": "rosen-ch1",
        "title": "Rosen 离散数学 第1章 逻辑与证明（主数据集）",
        "path": ROOT / "data" / "rosen" / "ch1" / "chunks.jsonl",
        "temp": False,
        "note": "Rosen《离散数学及其应用》第8版，第 1 章 8 节 / 120 页。**第三方教材，不进仓库**（见 DATA_NOT_INCLUDED.md）。",
    },
}
DEFAULT_MATERIAL = "rosen-ch1"

# 「整讲直灌」的字符上限：超过就退回命中页模式，并且**必须报出去**（不静默降级）
WHOLE_LECTURE_CHAR_LIMIT = 20000

flask_app = Flask(__name__, template_folder=str(APP_DIR / "templates"))
flask_app.config["JSON_AS_ASCII"] = False
flask_app.json.ensure_ascii = False

# 内存态：本次进程内最近一次提问
LAST: dict = {}
LOCK = threading.Lock()

CONDITIONS = ("baseline", "optimized")
CONDITION_LABEL = {
    "baseline": "基线（同款 LLM + 整讲直灌 + 范围约束）",
    "optimized": "优化（整讲直灌 + 范围约束 + 讲解方式约束）",
}
SLOTS = ("A", "B")


def _slot_answer(slot: str) -> dict:
    """服务端持有 A/B -> condition 的映射。

    前端只拿 A/B 代号，**不下发标签**，所以盲测期间打开开发者工具也看不到
    哪个是优化版。这是防"知情偏见"的实现要点，不是锦上添花。
    """
    with LOCK:
        snap = dict(LAST)
    return (snap.get("slot_answer") or {}).get(slot) or {}


def load_dotenv(path: Path) -> None:
    """极简 .env 读取：只设 os.environ，不覆盖已存在的变量。"""
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


@flask_app.get("/")
def index():
    from generator import GenConfig

    cfg = GenConfig.from_env()
    return render_template(
        "index.html",
        has_key=bool(cfg.api_key),
        model=cfg.model,
        base_url=cfg.base_url,
        strip_opt=cfg.strip_opt_constraints,
        default_material=DEFAULT_MATERIAL,
    )


@flask_app.get("/api/materials")
def api_materials():
    """素材清单 + 每份素材可选的"讲"。供 UI 动态填下拉框（不写死讲次）。"""
    out = []
    for key, m in MATERIALS.items():
        item = {
            "key": key,
            "title": m["title"],
            "temp": m["temp"],
            "note": m["note"],
            "exists": Path(m["path"]).exists(),
            "lectures": [],
            "topics": m.get("topics", []),
        }
        if item["exists"]:
            try:
                item["lectures"] = list_lectures(load_chunks(m["path"]))
            except Exception as e:
                item["error"] = f"{type(e).__name__}: {e}"
        out.append(item)
    return jsonify({"default": DEFAULT_MATERIAL, "materials": out})


@flask_app.post("/api/ask")
def api_ask():
    body = request.get_json(silent=True) or {}
    question = (body.get("question") or "").strip()
    material_key = (body.get("material") or DEFAULT_MATERIAL).strip()
    mat = MATERIALS.get(material_key)
    if mat is None:
        return jsonify({"error": f"未知素材：{material_key!r}"}), 400
    # lecture 为空 → 该素材全库检索（临时课件常常只有一份"整讲"）
    lecture = (body.get("lecture") or "").strip() or None
    # topic = 分区的下标（页区间）。整份素材太大时按分区学，而不是硬灌 51k 字符
    topic_idx = body.get("topic")
    page_range = None
    topic_title = None
    topics = mat.get("topics") or []
    if topic_idx is not None and str(topic_idx) != "":
        try:
            ti = int(topic_idx)
        except (TypeError, ValueError):
            return jsonify({"error": f"topic 必须是整数下标，收到 {topic_idx!r}"}), 400
        if not 0 <= ti < len(topics):
            return jsonify({"error": f"topic 下标越界：{ti}（共 {len(topics)} 个分区）"}), 400
        t = topics[ti]
        page_range = (t["lo"], t["hi"])
        topic_title = t["title"]
    top_k = int(body.get("top_k") or 3)
    # 讲法三档：**两条件共用**（不参与对照，保证差异只来自"讲得好不好"）
    teaching = (body.get("teaching") or DEFAULT_TEACHING).strip()
    if teaching not in TEACHING_MODES:
        return jsonify({"error": f"teaching 必须是 {TEACHING_MODES}，收到 {teaching!r}"}), 400
    # 起步阶段默认给整讲：见 retrieval.search 的 whole_lecture 说明
    # （纯词面检索会漏掉"讲这个概念、但措辞不同"的那一页）
    whole = body.get("whole_lecture")
    if whole is None:
        whole = os.environ.get("APP_HIT_PAGES_ONLY", "") != "1"
    whole = bool(whole)
    # L0 知识结构是否注入（**两条件共用**，与讲法/范围同理：它不参与对照）。
    # 做成开关是为了能用同一批题跑开/关两轮，验证"图谱能不能改进讲解"这条通路。
    use_graph = body.get("use_graph")
    if use_graph is None:
        use_graph = os.environ.get("APP_NO_GRAPH", "") != "1"
    use_graph = bool(use_graph)

    if not question:
        return jsonify({"error": "问题为空"}), 400

    t0 = time.time()
    try:
        chunks = load_chunks(mat["path"])
        pool = [
            c
            for c in chunks
            if (lecture is None or c.lecture == lecture)
            and (page_range is None or page_range[0] <= c.page <= page_range[1])
        ]
        pool_chars = sum(len(c.text or "") for c in pool)
        effective_whole = whole
        # 不许静默降级：选中范围超过整讲上限时退回命中页，并把这件事明确报给前端
        if whole and pool_chars > WHOLE_LECTURE_CHAR_LIMIT:
            effective_whole = False
        selected = search(
            question,
            chunks,
            lecture=lecture,
            top_k=top_k,
            bridge=True,
            whole_lecture=effective_whole,
            whole_lecture_char_limit=WHOLE_LECTURE_CHAR_LIMIT,
            page_range=page_range,
        )
        context = build_context(selected)
    except Exception as e:
        return jsonify({"error": f"检索失败：{type(e).__name__}: {e}"}), 500

    # L0 知识结构注入：只注入"本次上下文真的出现过"的节点（可核对），命中不了就不注入。
    # 注入文本**追加在课件原文之后**——两条件拿到完全相同的一份，所以它不参与对照。
    graph_used: list[str] = []
    graph_note = ""
    if use_graph:
        scope = "L01" if (lecture or "").startswith("L01") else None
        candidates = [s for s in (["L01"] if scope else [])]
        # 先试该讲的图；没有对应图就跳过（不报错，因为不是每讲都建了图）
        for sc in candidates:
            try:
                g = load_graph(sc)
            except GraphError:
                continue
            inj, ids = build_injection(g, [c.chunk_id for c in selected], question)
            if inj:
                context = context + "\n\n" + wrap(inj)
                graph_used, graph_note = ids, f"已注入 {len(ids)} 个知识结构节点"
            break
    ctx_chars = len(context)

    citations = [c.to_dict() for c in selected]
    matched_terms = sorted({t for c in selected for t in c.matched})
    retrieval_ms = int((time.time() - t0) * 1000)
    # whole_lecture 模式下每页都带分数，若某页得分恒为 0 会被 UI 误标成"桥接页"，
    # 所以额外告诉 UI 这次是不是整讲模式
    mode = "whole_lecture" if effective_whole else "hit_pages"
    downgrade = None
    if whole and not effective_whole:
        scope_name = f"分区「{topic_title}」" if topic_title else "素材范围"
        downgrade = (
            f"{scope_name} {pool_chars} 字符超过整讲上限 {WHOLE_LECTURE_CHAR_LIMIT}，"
            f"已自动改为「命中页 + 桥接页」"
        )

    trace_id = uuid.uuid4().hex[:12]

    if flask_app.config.get("DRY_RUN"):
        payload = {
            "trace_id": trace_id,
            "question": question,
            "lecture": lecture,
            "material": material_key,
            "topic": topic_title,
            "topic_range": list(page_range) if page_range else None,
            "teaching": teaching,
            "teaching_label": TEACHING_LABEL[teaching],
            "mode": mode,
            "downgrade": downgrade,
            "pool_chars": pool_chars,
            "citations": citations,
            "matched_terms": matched_terms,
            "retrieval_ms": retrieval_ms,
            "ctx_chars": ctx_chars,
            "graph_used": graph_used,
            "graph_note": graph_note,
            "dry_run": True,
            "answers": {},
        }
        with LOCK:
            LAST.clear()
            LAST.update(payload)
        return jsonify(payload)

    cfg = GenConfig.from_env()
    if not cfg.api_key:
        return jsonify(
            {"error": "服务器没有读到 DEEPSEEK_API_KEY（检查工作区根目录 .env）"}
        ), 500

    results: dict[str, dict] = {}
    server_errs: list[str] = []  # 含条件名，只留在服务端
    lock = threading.Lock()

    def run(cond: str) -> None:
        r = generate(cond, context, question, cfg=cfg, teaching=teaching)
        # 数学渲染在服务端做：LaTeX -> MathML（浏览器原生支持，前端零依赖）
        # 正文里的公式被换成占位符，随答案一起下发替换表。
        # 依据：用户 2026-09-21「公式没渲染处理，一堆杂乱的符号根本看不懂」（连提三次）。
        tpl_text, math_items, math_fails = render_math(r.text or "")
        with lock:
            if r.error:
                server_errs.append(f"{cond}: {r.error}")
            results[cond] = {
                "condition": cond,
                "label": CONDITION_LABEL[cond],
                "text": r.text,
                "text_tpl": tpl_text,
                "math": [{"token": m["token"], "mathml": m["mathml"], "ok": m["ok"],
                          "tex": m["tex"], "block": m["block"]} for m in math_items],
                "math_count": len(math_items),
                "math_fails": math_fails,
                "model": r.model,
                "prompt_tokens": r.prompt_tokens,
                "completion_tokens": r.completion_tokens,
                "finish_reason": r.finish_reason,
                "truncated": r.truncated,
                "attempts": r.attempts,
                "error": r.error,
                "warnings": r.warnings,
            }

    threads = [threading.Thread(target=run, args=(c,), daemon=True) for c in CONDITIONS]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=cfg.timeout + 30)

    if not results:
        # 这是"两个都挂了"的硬失败，不涉及 A/B 盲测，可以说出条件名便于排查
        return jsonify({"error": "两个条件都没拿到结果：" + "；".join(server_errs)}), 502
    if server_errs:
        # 盲测：不下发条件名，只说"有一段失败"，条件名打印到服务端控制台
        print("[app] 生成失败（服务端明细，含条件名）：" + " | ".join(server_errs))

    # 盲测槽位：服务端随机决定 A/B 对应哪个条件，标签只留在服务端
    shuffled = list(CONDITIONS)
    random.shuffle(shuffled)
    slot_of = dict(zip(SLOTS, shuffled))
    answers = {
        slot: {
            "slot": slot,
            "model": (results.get(cond) or {}).get("model") or cfg.model,
            "text": (results.get(cond) or {}).get("text", ""),
            "text_tpl": (results.get(cond) or {}).get("text_tpl", ""),
            "math": (results.get(cond) or {}).get("math", []),
            "math_count": (results.get(cond) or {}).get("math_count", 0),
            "math_fails": (results.get(cond) or {}).get("math_fails", 0),
            "chars": len((results.get(cond) or {}).get("text", "") or ""),
            "completion_tokens": (results.get(cond) or {}).get("completion_tokens"),
            "finish_reason": (results.get(cond) or {}).get("finish_reason"),
            "truncated": (results.get(cond) or {}).get("truncated", False),
            "attempts": (results.get(cond) or {}).get("attempts", 1),
            "error": (results.get(cond) or {}).get("error"),
        }
        for slot, cond in slot_of.items()
    }

    payload = {
        "trace_id": trace_id,
        "question": question,
        "lecture": lecture,
        "material": material_key,
        "topic": topic_title,
        "topic_range": list(page_range) if page_range else None,
        "teaching": teaching,
        "teaching_label": TEACHING_LABEL[teaching],
        "mode": mode,
        "downgrade": downgrade,
        "pool_chars": pool_chars,
        "citations": citations,
        "matched_terms": matched_terms,
        "retrieval_ms": retrieval_ms,
        "ctx_chars": ctx_chars,
        "graph_used": graph_used,
        "graph_note": graph_note,
        "elapsed_ms": int((time.time() - t0) * 1000),
        "model": cfg.model,
        "answers": answers,
        # ⚠️ 这里**绝对不能**放含条件名的错误串：一旦某个条件失败就泄露了标签。
        # 盲测期间只告诉前端"有几段失败"。
        "failed_count": len(server_errs),
    }
    with LOCK:
        LAST.clear()
        LAST.update(payload)
        # 标签单独存，且**不放进 payload**（不进 HTTP 响应）
        LAST["slot_of"] = slot_of
        # 评分时要把"当时的讲解原文"一起落盘，所以整份 results 也留在服务端
        LAST["results"] = results
        LAST["slot_answer"] = {slot: results.get(cond) or {} for slot, cond in slot_of.items()}
    return jsonify(payload)


@flask_app.post("/api/reveal")
def api_reveal():
    """用户对 A、B 都打完分之后，才揭晓哪个是哪个。"""
    body = request.get_json(silent=True) or {}
    trace_id = body.get("trace_id")
    with LOCK:
        snap = dict(LAST)
    if not snap or snap.get("trace_id") != trace_id:
        return jsonify({"error": "trace_id 与最近一次提问不匹配"}), 409
    slot_of = snap.get("slot_of") or {}
    return jsonify(
        {
            "trace_id": trace_id,
            "labels": {slot: {"condition": cond, "label": CONDITION_LABEL[cond]} for slot, cond in slot_of.items()},
        }
    )


@flask_app.post("/api/rate")
def api_rate():
    """按**槽位**（A/B）打分，不按条件——这样盲测期间前端拿不到条件名。

    打分那一刻服务端才知道这个槽位是哪个条件，并把它连同讲解原文一起落盘。
    """
    body = request.get_json(silent=True) or {}
    trace_id = body.get("trace_id")
    slot = (body.get("slot") or "").strip().upper()
    score = body.get("score")
    reason = (body.get("reason") or "").strip()

    if slot not in SLOTS:
        return jsonify({"error": f"slot 必须是 {SLOTS}"}), 400
    try:
        score = int(score)
    except (TypeError, ValueError):
        return jsonify({"error": "score 必须是 1–5 的整数"}), 400
    if not 1 <= score <= 5:
        return jsonify({"error": "score 必须在 1–5 之间"}), 400

    with LOCK:
        snap = dict(LAST)
    if not snap or snap.get("trace_id") != trace_id:
        return jsonify({"error": "trace_id 与最近一次提问不匹配，请重新提问后再打分"}), 409

    slot_of = snap.get("slot_of") or {}
    condition = slot_of.get(slot)
    if condition is None:
        return jsonify({"error": f"槽位 {slot} 不属于本次提问"}), 409

    res = snap.get("slot_answer", {}).get(slot) or {}
    row = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "trace_id": trace_id,
        "question": snap.get("question"),
        "lecture": snap.get("lecture"),
        "material": snap.get("material"),
        "topic": snap.get("topic"),
        "teaching": snap.get("teaching"),
        "slot": slot,
        "condition": condition,
        "blind": True,
        "score": score,
        "reason": reason,
        "model": res.get("model") or snap.get("model"),
        "citations": [c["chunk_id"] for c in snap.get("citations", [])],
        "matched_terms": snap.get("matched_terms", []),
        "answer": res.get("text", ""),
        "answer_chars": len(res.get("text", "") or ""),
        "truncated": res.get("truncated", False),
        "error": res.get("error"),
    }
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with RATINGS_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return jsonify({"ok": True, "saved": row["ts"], "path": str(RATINGS_PATH)})


@flask_app.get("/api/stats")
def api_stats():
    """只报分布，不下结论。

    **零方差的一致率不是证据**：曾经把「100% 一致」当成可靠信号，
    实际是因为所有判定都落在同一侧。所以这里把 reasons 和分布一起返回。
    """
    if not RATINGS_PATH.exists():
        return jsonify({"n": 0, "by_condition": {}, "note": "还没有评分数据"})
    by: dict[str, dict] = {}
    n = 0
    with RATINGS_PATH.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            n += 1
            b = by.setdefault(r["condition"], {"n": 0, "scores": [], "sum": 0, "reasons": []})
            b["n"] += 1
            b["scores"].append(r["score"])
            b["sum"] += r["score"]
            if r.get("reason"):
                b["reasons"].append(r["reason"])
    for b in by.values():
        b["mean"] = round(b["sum"] / b["n"], 2) if b["n"] else None
        b["distribution"] = {str(s): b["scores"].count(s) for s in range(1, 6)}
    return jsonify({"n": n, "by_condition": by, "path": str(RATINGS_PATH)})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=5000)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--dry-run", action="store_true", help="只跑检索，不调模型")
    args = ap.parse_args()

    load_dotenv(ROOT / ".env")
    flask_app.config["DRY_RUN"] = args.dry_run
    cfg = GenConfig.from_env()
    print(f"[app] 知识库 : {ROOT / 'knowledge_base' / 'chunks.jsonl'}")
    print(f"[app] 评分落盘: {RATINGS_PATH}")
    print(f"[app] 模型    : {cfg.model} @ {cfg.base_url}")
    print(f"[app] API key : {'已读到' if cfg.api_key else '⚠️ 没读到（检查 .env）'}")
    if cfg.strip_opt_constraints:
        print("[app] ⚠️ APP_STRIP_OPT=1：optimized 条件的约束已被关掉（两条件同指令）")
    if args.dry_run:
        print("[app] dry-run 模式：不调用模型")
    print(f"[app] 打开 http://{args.host}:{args.port}")
    flask_app.run(host=args.host, port=args.port, debug=False, threaded=True)


if __name__ == "__main__":
    main()
