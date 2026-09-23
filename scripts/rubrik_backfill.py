# -*- coding: utf-8 -*-
"""回填工具：用**已有的**评判准则给已存的讲解打分（判据映射诊断 + 盲评 + 对照汇总）。

## ⚠️ 首次使用的那套准则（Rubrik's Cube）**已被否决**，不要再用

- 否决记录：`docs/13_已否决_Rubriks_Cube.md`
- 原因（一句话）：在我们的小样本上**零区分度**（77 个判定格只有 2 格不同），
  根因是**体裁错配**——它默认「多选题 + 解释选了哪个答案」，而用户真正不满的
  维度（内容覆盖全不全、该给代码有没有给）它根本不测。
- **本脚本本身是可复用的**：换掉 `CRITERIA` 与 `APPLICABILITY` 两张表，
  就能用同一套"先映射判据 → 再盲评 → 再联结回条件"的流程去测**别的**量表
  （下一步是用 MQI 的编码 3 / 4 / 12 / 13 / 14）。

为什么要先做判据映射（而不是直接套用）：
    首次那套准则的 13 条是为**多选题的解释**设计的——上下文里明确要求
    「提供理解：为什么选了这个答案」。我们的产物是**知识点讲解**，不是「我为什么选 A」。
    所以必须先逐条判断「这条判据在我们的文本上有没有意义」，
    否则会得出「全都判不过」的假结论（这正是错题本 M9：拿不适用的尺子量出假红灯）。

用法：
    python scripts/rubrik_backfill.py --map        # 只做判据映射诊断（不调模型）
    python scripts/rubrik_backfill.py --export     # 导出盲评输入（条件已抹掉）
    python scripts/rubrik_backfill.py --report <judge.json>   # 汇总对照表
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RATINGS = ROOT / "data" / "ratings.jsonl"
OUT = ROOT / "data" / "rubrik"
EXPORT = OUT / "blind_input.json"
JUDGE_IN = OUT / "judge_result.json"

# Rubrik's Cube 的 13 条判据（原文见 templates/logic/explanation_judgement.j2.md）
CRITERIA = [
    ("Action", "语言/结构", "解释是否明确指出「被解释的决定/选择」"),
    ("Reason", "语言/结构", "是否给出该选择背后的理由"),
    ("Grammaticality", "Language", "语法正确、无影响理解的错误"),
    ("Word Choice", "Language", "措辞是否贴合给定语境与读者"),
    ("Cohesion", "Language", "是否恰当使用连接词（because/therefore 等）"),
    ("Conciseness", "Language", "是否没有多余、无关、可省的句子"),
    ("Appropriateness", "Language", "内容是否契合语境期待、无不当"),
    ("Coherence", "Language", "整体是否讲得通（语义一致、句间因果/时序合理）"),
    ("Evidence", "Content", "是否给出支持推理的具体证据"),
    ("Plausibility", "Content", "证据是否可信、符合人类推理"),
    ("Affective Appeals", "Argument", "是否用情感化语言打动读者"),
    ("Qualifiers", "Argument", "是否用限定词/态度标记表明自身立场"),
    ("Stance Clarity", "Argument", "立场是否清晰无歧义"),
]

# 逐条判定「用在本项目（知识点讲解）上是否有意义」，并写明理由。
# 这一步是**诊断**，必须留痕；改判据要有依据，不能随手调。
APPLICABILITY = {
    "Action": (False, "Rubrik 的 Action = 指明选了哪个选项。我们的讲解没有「选项」，"
                      "强行映射会把「说了要讲什么」当 Action，属于改写判据"),
    "Reason": (True, "对应「讲 why」，与 docs/03 §六 的 MQI 编码 3 同向"),
    "Grammaticality": (True, "通用，直接可用"),
    "Word Choice": (True, "通用，且正好能测用户抱怨的「术语密度」"),
    "Cohesion": (True, "通用"),
    "Conciseness": (True, "通用，且 Rubrik 自己的结论说「低质量主要来自不简洁」"),
    "Appropriateness": (True, "可映射为「是否契合自学学生的语境」"),
    "Coherence": (True, "通用"),
    "Evidence": (False, "Rubrik 的 Evidence = 引用题目语境或常识来支持选项，"
                        "属于**论证**；知识点讲解不需要为某个选择举证"),
    "Plausibility": (False, "为 Evidence 服务，Evidence 不适用则此条不适用"),
    "Affective Appeals": (False, "属 Argument（说服）；教学讲解不是说服"),
    "Qualifiers": (False, "同上"),
    "Stance Clarity": (False, "同上，测的是作者对任务的态度"),
}


def load_pairs() -> list[dict]:
    """把 ratings.jsonl 变成"同一问题的 A/B 两段"配对。"""
    rows = [json.loads(l) for l in RATINGS.read_text(encoding="utf-8").splitlines() if l.strip()]
    by_q: dict[str, dict[str, dict]] = defaultdict(dict)
    meta: dict[str, dict] = {}
    for r in rows:
        q = r.get("question") or ""
        cond = r.get("condition")
        if not cond:
            continue
        by_q[q][cond] = r
        meta[q] = {
            "teaching": r.get("teaching"),
            "material": r.get("material"),
            "topic": r.get("topic"),
        }
    pairs = []
    for q, d in by_q.items():
        if "baseline" in d and "optimized" in d:
            pairs.append(
                {
                    "question": q,
                    "teaching": meta[q]["teaching"],
                    "material": meta[q]["material"],
                    "topic": meta[q]["topic"],
                    "baseline": d["baseline"],
                    "optimized": d["optimized"],
                }
            )
    return pairs


def cmd_map() -> int:
    pairs = load_pairs()
    ok = sum(1 for k, (a, _) in APPLICABILITY.items() if a)
    print("=" * 78)
    print("判据映射诊断：Rubrik 的 13 条，哪些能用在「知识点讲解」上")
    print("=" * 78)
    for name, cat, desc in CRITERIA:
        applies, why = APPLICABILITY[name]
        mark = "✅ 可用" if applies else "❌ 不适用"
        print(f"{mark}  {name:<18} [{cat}]")
        print(f"        Rubrik 原意：{desc}")
        print(f"        判定理由  ：{why}")
    print()
    print(f"结论：13 条里 **{ok} 条可用**，{13 - ok} 条属于「论证/说服」或「多选题」语境，不适用。")
    print()
    print(f"已配对的问题数：{len(pairs)}")
    for p in pairs:
        print(f"  - [{p['teaching']}/{p['material']}] {p['question'][:52]}")
    return 0


def cmd_export() -> int:
    """导出盲评输入：**抹掉条件名**，A/B 随机化成 slot。"""
    import random

    pairs = load_pairs()
    OUT.mkdir(parents=True, exist_ok=True)
    items = []
    key = []
    for i, p in enumerate(pairs):
        order = ["baseline", "optimized"]
        random.shuffle(order)
        for j, cond in enumerate(order):
            r = p[cond]
            slot = "X" if j == 0 else "Y"
            items.append(
                {
                    "id": f"q{i:02d}{slot}",
                    "question": p["question"],
                    "teaching": p["teaching"],
                    "text": r.get("answer") or "",
                    "user_score": r.get("score"),
                }
            )
            key.append({"id": f"q{i:02d}{slot}", "condition": cond, "question": p["question"]})
    EXPORT.write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "_key.json").write_text(json.dumps(key, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"导出 {len(items)} 条（{len(pairs)} 问 × 2）-> {EXPORT}")
    print(f"答案键（**不要给评判者看**）-> {OUT / '_key.json'}")
    print()
    print("注意：item 里**没有** condition 字段，评判者只能看到 X/Y。")
    return 0


def cmd_report(judge_path: str) -> int:
    jp = Path(judge_path)
    if not jp.is_absolute():
        jp = ROOT / judge_path
    judged = {d["id"]: d for d in json.loads(jp.read_text(encoding="utf-8"))}
    key = {d["id"]: d for d in json.loads((OUT / "_key.json").read_text(encoding="utf-8"))}
    items = {d["id"]: d for d in json.loads(EXPORT.read_text(encoding="utf-8"))}

    usable = [name for name, _cat, _d in CRITERIA if APPLICABILITY[name][0]]
    agg: dict[str, dict[str, list[int]]] = {name: {"baseline": [], "optimized": []} for name in usable}
    per_q = defaultdict(dict)
    for iid, d in judged.items():
        cond = key[iid]["condition"]
        q = key[iid]["question"]
        row = {}
        for name in usable:
            v = d.get(name)
            b = 1 if (isinstance(v, str) and v.strip().lower().startswith("y")) else (1 if v is True else 0)
            agg[name][cond].append(b)
            row[name] = b
        per_q[q][cond] = row

    print("=" * 78)
    print("Rubrik 可用判据：通过率对照（baseline vs optimized）")
    print("=" * 78)
    print(f"{'判据':<18}{'baseline':>12}{'optimized':>12}{'差':>8}")
    for name in usable:
        b, o = agg[name]["baseline"], agg[name]["optimized"]
        rb = sum(b) / len(b) if b else 0
        ro = sum(o) / len(o) if o else 0
        print(f"{name:<18}{rb:>11.0%}{ro:>12.0%}{ro - rb:>+8.0%}")
    print()
    print("逐问明细：")
    for q, d in per_q.items():
        b, o = d.get("baseline", {}), d.get("optimized", {})
        print(f"  {q[:50]}")
        for name in usable:
            print(f"      {name:<16} base={b.get(name, '-')}  opt={o.get(name, '-')}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", action="store_true")
    ap.add_argument("--export", action="store_true")
    ap.add_argument("--report")
    args = ap.parse_args()
    if args.map:
        return cmd_map()
    if args.export:
        return cmd_export()
    if args.report:
        return cmd_report(args.report)
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
