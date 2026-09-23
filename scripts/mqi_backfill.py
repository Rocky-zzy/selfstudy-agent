# -*- coding: utf-8 -*-
r"""MQI 回填：用已有的 MQI 编码给已存的讲解打分（盲评 + 对照汇总）。

## 与上一轮（Rubrik's Cube）的关系

Rubrik 那套**已被否决**（`docs/13`）。本脚本沿用它留下的**可复用流程**：
**先做判据映射 → 再盲评 → 再联结回条件**。
但判据换成 MQI，而且量级从「二元」变成 **MQI 的四级（0–3）**——
这一点很重要：Rubrik 那轮 77 个判定格里只有 2 格不同，**部分原因可能是"二元"太粗**。

## 判据来源（原文）

`docs/refs/MQI判据_原文摘录.md`（逐字摘录自 `mqi_4point_modeling.pdf` 第 6–8、19–22 页）

| 编码 | 名称 | 极性 |
|---|---|---|
| 3 | Explanations | ⬆ 高分好 |
| 4 | Mathematical Sense-Making | ⬆ 高分好 |
| 12 | Mathematical Content Errors | ⚠️ **高分坏** |
| 13 | Imprecision in Language or Notation | ⚠️ **高分坏** |
| 14 | Lack of Clarity in Presentation | ⚠️ **高分坏** |

**极性陷阱**：Richness 域高分是好的，Errors and Imprecision 域高分是坏的。
本脚本用 `higher_is_better` 显式区分，**汇总时分开报，不混算**。

用法：
    python scripts/mqi_backfill.py --map      # 判据映射说明
    python scripts/mqi_backfill.py --export   # 导出盲评输入（抹掉条件名）
    python scripts/mqi_backfill.py --report data/mqi/judge_result.json
"""

from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RATINGS = ROOT / "data" / "ratings.jsonl"
OUT = ROOT / "data" / "mqi"
EXPORT = OUT / "blind_input.json"
KEY = OUT / "_key.json"

LEVELS = ["Not Present", "Low", "Mid", "High"]

# (编码, 名称, 域, higher_is_better, 本项目是否适用, 判定理由)
CODES = [
    (3, "Explanations", "Richness", True, True,
     "对应「讲 why 不讲 how」。原文明确：只描述步骤不算解释。"
     "分级靠「出现一处的孤立 / 两处以上或较长 / 是这篇的焦点」"),
    (4, "Mathematical Sense-Making", "Richness", True, True,
     "对应「给程序与定义赋予意义、讨论合理性、找反例」。"
     "与编码 3 的区别是：它只计真正在讲意义的篇幅，**不计铺垫**"),
    (12, "Mathematical Content Errors", "Errors", False, True,
     "可查：定义错、漏掉关键条件、把不相同的概念等同。注意「段内被纠正的错误不计」"),
    (13, "Imprecision in Language or Notation", "Errors", False, True,
     "可查：符号误用、术语误用、日常含义与数学含义混同。"
     "**正好覆盖用户抱怨的「符号杂乱、术语密度」**"),
    (14, "Lack of Clarity in Presentation", "Errors", False, True,
     "可查：要点含混/被歪曲、**对同一概念给出冲突定义**。"
     "上一轮 Rubrik 盲评抓到过一个实例（模板化设问标题与正文自相矛盾），本条可复核它"),
]

# MQI 是**整段课堂观察**量表（segment ≈ 5–7.5 分钟），分级依据是时间与篇幅。
# 我们是静态文本、没有"段"。所以必须写明映射，并且**不得把它当成原量表的原样使用**。
SEGMENT_MAPPING = """把整篇讲解当作一个 segment：

| 原文措辞 | 本项目映射 |
|---|---|
| in the segment | 整篇讲解 |
| isolated instance | 全篇只出现 1 处 |
| two or more brief / more than briefly | 出现 ≥2 处，或有 1 处篇幅较长 |
| focus of instruction / major feature | 是这篇讲解的主要特征 |
| sustained（编码 4） | 该行为贯穿相当篇幅 |

⚠️ 这个映射是本项目做的，**未经验证**。结论只能说「按上述映射……」。"""

POLARITY_NOTE = """**极性提醒（错题本里记过的陷阱）**：
- 编码 3、4 属 Richness 域 → **高分是好的**
- 编码 12、13、14 属 Errors and Imprecision 域 → **高分是坏的**
汇总时**分开报**，绝不混算成一个总分。"""


def load_pairs() -> list[dict]:
    rows = [json.loads(l) for l in RATINGS.read_text(encoding="utf-8").splitlines() if l.strip()]
    by_q: dict[str, dict[str, dict]] = defaultdict(dict)
    meta: dict[str, dict] = {}
    for r in rows:
        cond = r.get("condition")
        if not cond:
            continue
        q = r.get("question") or ""
        by_q[q][cond] = r
        meta[q] = {"teaching": r.get("teaching"), "material": r.get("material")}
    pairs = []
    for q, d in by_q.items():
        if "baseline" in d and "optimized" in d:
            pairs.append({"question": q, **meta[q], "baseline": d["baseline"],
                          "optimized": d["optimized"]})
    return pairs


def cmd_map() -> int:
    print("=" * 78)
    print("MQI 判据映射：5 条编码，逐条说明")
    print("=" * 78)
    for num, name, dom, hib, applies, why in CODES:
        pol = "⬆ 高分好" if hib else "⚠️ 高分坏"
        print(f"{'✅ 采用' if applies else '❌ 不适用'}  编码 {num}. {name}")
        print(f"        域={dom}  极性={pol}")
        print(f"        理由：{why}")
    print()
    print(SEGMENT_MAPPING)
    print()
    print(POLARITY_NOTE)
    return 0


def cmd_export() -> int:
    pairs = load_pairs()
    OUT.mkdir(parents=True, exist_ok=True)
    items, key = [], []
    for i, p in enumerate(pairs):
        order = ["baseline", "optimized"]
        random.shuffle(order)
        for j, cond in enumerate(order):
            slot = "X" if j == 0 else "Y"
            items.append({
                "id": f"q{i:02d}{slot}",
                "question": p["question"],
                "teaching": p["teaching"],
                "text": p[cond].get("answer") or "",
                # ⚠️ 刻意**不放** user_score。
                # 第一轮盲评我把它放进去了，评判者能看到用户当时打的分——
                # 那是一个比条件名更间接的引导（用户分高的地方，评判者可能倾向于挑错以显得independent，
                # 或者相反）。X/Y 两组的用户分分布是平衡的，所以它不会制造系统性的组间偏差，
                # 但会影响**单条**判定。按"验证必须具体"，修掉重跑一遍看结论稳不稳。
            })
            key.append({"id": f"q{i:02d}{slot}", "condition": cond, "question": p["question"]})
    EXPORT.write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    KEY.write_text(json.dumps(key, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"导出 {len(items)} 条（{len(pairs)} 问 × 2）-> {EXPORT}")
    print(f"答案键（**不要给评判者看**）-> {KEY}")
    print("item 字段：id / question / teaching / text —— **没有 condition，也没有 user_score**。")
    return 0


def cmd_report(judge_path: str) -> int:
    jp = Path(judge_path)
    if not jp.is_absolute():
        jp = ROOT / jp
    judged = {d["id"]: d for d in json.loads(jp.read_text(encoding="utf-8"))}
    key = {d["id"]: d for d in json.loads(KEY.read_text(encoding="utf-8"))}

    lvl_idx = {lv.lower(): i for i, lv in enumerate(LEVELS)}
    agg: dict[int, dict[str, list[int]]] = {c[0]: {"baseline": [], "optimized": []} for c in CODES}
    per_q: dict[str, dict[str, dict[int, int]]] = defaultdict(lambda: defaultdict(dict))
    bad = []
    for iid, d in judged.items():
        if iid not in key:
            bad.append(iid)
            continue
        cond = key[iid]["condition"]
        q = key[iid]["question"]
        for num, *_ in CODES:
            v = d.get(str(num), d.get(f"code{num}", d.get(f"Code {num}")))
            if v is None:
                bad.append(f"{iid}:code{num}")
                continue
            if isinstance(v, int):
                idx = v
            else:
                idx = lvl_idx.get(str(v).strip().lower(), None)
                if idx is None:
                    bad.append(f"{iid}:code{num}={v!r}")
                    continue
            agg[num][cond].append(idx)
            per_q[q][cond][num] = idx

    if bad:
        print(f"⚠️ {len(bad)} 个判定无法解析（前 8 个）：{bad[:8]}")
        print()

    def mean(xs):
        return sum(xs) / len(xs) if xs else float("nan")

    print("=" * 78)
    print("MQI 四级评分对照（0=Not Present … 3=High）")
    print("=" * 78)
    print(f"{'编码':<6}{'名称':<38}{'极性':<10}{'base':>7}{'opt':>7}{'差':>7}")
    for num, name, dom, hib, applies, _why in CODES:
        b, o = agg[num]["baseline"], agg[num]["optimized"]
        pol = "高分好" if hib else "高分坏"
        print(f"{num:<6}{name[:36]:<38}{pol:<10}{mean(b):>7.2f}{mean(o):>7.2f}"
              f"{mean(o) - mean(b):>+7.2f}")
    print()
    print("分级分布（每格是 0/1/2/3 的计数）：")
    for num, name, *_ in CODES:
        for cond in ("baseline", "optimized"):
            xs = agg[num][cond]
            dist = [xs.count(i) for i in range(4)]
            print(f"  编码 {num:<3}{cond:<11} NotPresent={dist[0]}  Low={dist[1]}  "
                  f"Mid={dist[2]}  High={dist[3]}")
    print()
    print("逐问明细（看方向是否一致，不要只看均值）：")
    for q, d in per_q.items():
        b, o = d.get("baseline", {}), d.get("optimized", {})
        seg = "  ".join(f"c{n}:{b.get(n,'-')}->{o.get(n,'-')}" for n, *_ in CODES)
        print(f"  {q[:44]:<46} {seg}")
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
