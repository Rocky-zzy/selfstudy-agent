# -*- coding: utf-8 -*-
r"""把 L0 知识结构挂进讲解：按本次上下文**只抽相关子图**，注入 prompt。

## 依据

- 子目标标注：Morrison, Margulieux & Decker (2020), *Computer Science Education* 30(2)——
  子目标标注提高新问题表现且**不增加学习时间**；**无反馈条件下"给标签"优于让学生自己生成**。
  出处：[NSF PAR 10171483](https://par.nsf.gov/biblio/10171483/media/xml)。
  标签写**功能/目的**不绑符号（Catrambone 1995/1998：抽象标签更利迁移）。
- 前置/层级：先行组织者 / pre-training 方向（`docs/03` 机制一）。
  ⚠️ 先行组织者与知识地图**只有方向性依据、未取到效应量**（`docs/15` §二 已如实标注）。

## 为什么只注入相关子图，而不是整张图

① 图谱是**决策层**的东西，把全图塞进 prompt 会把上下文撑大且引入无关节点；
② 只注入"这次上下文真的出现过"的节点，注入内容才**可核对**（每个节点都有 chunk_id 出处）。

## 选择规则（2026-09-23 修正过一版，第一版是错的）

**第一版**：只按"节点 sources 与本次页有无交集"选。**实测发现它会把目标节点挤掉**——
问"基变换矩阵怎么推"时，一次注入 6 个节点里**没有 basis_change**，
因为大量节点都是 1 个页命中，按上限截断后目标反而落选。

**现在**（两步，可解释）：

1. **定目标**：把问题文本按**最长公共子串**去对节点 `title`（≥2 字算命中），
   再叠加 `keywords` 字段（若节点提供）。命中最多者 = 目标节点。
2. **补上下文**：把目标节点的 `prerequisites` 与 `contrast` **一并带上**（这是它们存在的理由），
   再按"页面命中数"补足到 `MAX_NODES`。

**命中不了目标就不注入**（宁可不注入，也不注入一堆无关节点）。
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPH_DIR = ROOT / "data" / "graph"

# 注入块的标记。与课件原文分开，便于两种条件下的对照与事后核对。
MARK_BEGIN = "<<<KNOWLEDGE-STRUCTURE>>>"
MARK_END = "<<<END KNOWLEDGE-STRUCTURE>>>"

MAX_NODES = 5  # 上限：目标 + 前置/对比 + 少量补充
MIN_TITLE_OVERLAP = 2  # 标题至少要有 2 个连续字命中才算目标


class GraphError(Exception):
    """图数据有问题（缺失、结构非法）。"""


def load_graph(scope: str = "L01") -> dict:
    p = GRAPH_DIR / f"{scope}.json"
    if not p.exists():
        raise GraphError(f"没有图谱数据：{p}")
    g = json.loads(p.read_text(encoding="utf-8"))
    if not g.get("nodes"):
        raise GraphError(f"{p} 里没有 nodes")
    return g


def _longest_common_run(a: str, b: str) -> int:
    """a、b 的最长公共子串长度（用于标题匹配；不引第三方库）。"""
    if not a or not b:
        return 0
    prev = [0] * (len(b) + 1)
    best = 0
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best = cur[j]
        prev = cur
    return best


def find_target(g: dict, question: str) -> dict | None:
    """按标题（含 keywords）匹配出本次要讲的那个知识点。挑不出就返回 None。"""
    best, best_score = None, 0
    for n in g["nodes"]:
        cands = [n.get("title", "")] + list(n.get("keywords") or [])
        score = max((_longest_common_run(question, c) for c in cands if c), default=0)
        # 程序性节点在同等命中下优先（有步骤可讲）
        if score >= MIN_TITLE_OVERLAP and (score, n["type"] == "procedure") > (
            best_score, (best or {}).get("type") == "procedure"
        ):
            best, best_score = n, score
    return best


def select_nodes(g: dict, present_chunk_ids: list[str], question: str = "") -> list[dict]:
    """挑出本次该注入的节点：目标优先 → 其前置/对比 → 按页命中补足。"""
    by_id = {n["id"]: n for n in g["nodes"]}
    present = set(present_chunk_ids)

    target = find_target(g, question)
    picked: list[dict] = []
    if target:
        picked.append(target)
        for ref in list(target.get("prerequisites") or []) + list(target.get("contrast") or []):
            if ref in by_id and by_id[ref] not in picked:
                picked.append(by_id[ref])

    # 补足：按"与本次页面的交集"排序
    rest = []
    for n in g["nodes"]:
        if n in picked:
            continue
        hit = len([s for s in n.get("sources", []) if s in present])
        if hit:
            rest.append((hit, n))
    rest.sort(key=lambda x: -x[0])
    for _h, n in rest:
        if len(picked) >= MAX_NODES:
            break
        picked.append(n)
    return picked[:MAX_NODES]


def _block_for(node: dict, by_id: dict[str, dict]) -> list[str]:
    L: list[str] = []
    kind = "程序（有步骤）" if node["type"] == "procedure" else "概念"
    L.append(f"◆ {node['title']}（{kind}）｜出处 {'、'.join(node.get('sources', []))}")

    pre = node.get("prerequisites") or []
    if pre:
        L.append("  先修：" + "、".join(f"{by_id[p]['title']}" for p in pre if p in by_id))
    broader = node.get("broader")
    if broader and broader in by_id:
        L.append(f"  上位（讲到它就够，不必下钻）：{by_id[broader]['title']}")
    con = node.get("contrast") or []
    if con:
        L.append("  易混对比对象：" + "、".join(by_id[c]["title"] for c in con if c in by_id))
    ms = node.get("misconceptions") or []
    if ms:
        L.append("  学生常见错误（讲到时点出来）：")
        for m in ms:
            L.append(f"    - {m}")

    subs = node.get("subgoals") or []
    if subs:
        L.append("  ★ 讲解步骤请**用这些标签组织**（标签写功能，别改写成符号）：")
        for i, sg in enumerate(subs, 1):
            L.append(f"    {i}. 【{sg['label']}】{sg.get('detail','')}")
            if sg.get("not_in_source"):
                L.append(f"       ⚠️ 课件没交代：{sg['not_in_source']}"
                         f"——若你要补这个理由，必须标明是补充解释")
    return L


def build_injection(g: dict, present_chunk_ids: list[str], question: str = "") -> tuple[str, list[str]]:
    """返回（注入文本, 被注入的节点 id 列表）。没有可注入的节点时返回 ("", [])。"""
    nodes = select_nodes(g, present_chunk_ids, question)
    if not nodes:
        return "", []
    by_id = {n["id"]: n for n in g["nodes"]}
    L: list[str] = []
    L.append("以下是这门课**已有的知识结构**里，与本次课件内容相关的部分。")
    L.append("请用它来组织讲解——尤其是「讲解步骤」那几行：**照那些标签讲，不要自己另编步骤**。")
    L.append("凡标了「课件没交代」的地方，你若补充理由，必须说明那是补充解释而非课件内容。")
    L.append("")
    for n in nodes:
        L.extend(_block_for(n, by_id))
        L.append("")
    return "\n".join(L).rstrip() + "\n", [n["id"] for n in nodes]


def wrap(text: str) -> str:
    return f"{MARK_BEGIN}\n{text}{MARK_END}"
