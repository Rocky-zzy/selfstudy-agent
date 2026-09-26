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
import re
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


def _hits_only(node: dict) -> list[str]:
    """节点自己的标题/关键词（不含"问题里出现过"这层过滤）。"""
    return [node.get("title", "")] + list(node.get("keywords") or [])


def _hits(question: str, node: dict) -> list[str]:
    """问题里**逐字出现**的标题/关键词。"""
    return [c for c in _hits_only(node) if c and c in question]


def _score(question: str, node: dict, distinctive: set[str] | None = None) -> tuple[int, int, int, int]:
    """(是否具体, 最长命中词长度, -命中词最早出现位置, 命中个数)。字典序越大越优先。

    排序为什么是"最长词"在前、"位置"在后：实测问"什么是构造性存在性证明？"，
    "证明（proof）"只命中 2 个字的泛词 `证明` 却因为它出现得更早就当了目标，
    把 8 个字的 `构造性存在性证明` 挤成配角。**命中越长越说明问的就是它**；
    位置只在同样长的时候用来分先后（"怎么用反证法证明？它和逆否证明有什么区别？"
    里两个词一样长，先问的那个才是主语）。
    """
    hits = _hits(question, node)
    longest = max((len(c) for c in hits), default=0)
    if distinctive is None:
        distinctive = {c for c in hits}
    specific = len(hits) >= 2 or any(c in distinctive for c in hits)
    # 定位只看**具体命中词**：泛词（"证明""命题"）不参与"谁先被问到"的判断
    spots = [question.find(c) for c in hits if c in distinctive]
    earliest = min(spots) if spots else 10 ** 6
    return (1 if specific else 0, longest, -earliest, len(hits))


def _term_freq(nodes: list[dict]) -> dict[str, int]:
    """每个标题/关键词在这张图里被几个节点用着。"""
    freq: dict[str, int] = {}
    for n in nodes:
        for c in {n.get("title", "")} | set(n.get("keywords") or []):
            if c:
                freq[c] = freq.get(c, 0) + 1
    return freq


def _distinctive_terms(nodes: list[dict], max_df: int = 2) -> set[str]:
    """"说得够具体"的词：全图里只有 ≤ max_df 个节点在用。

    ⚠️ 不能改成按节点总数的比例（试过 4% ≈ 5 个节点）：那样"证明""命题""等价"
    这类到处都在用的泛词也会被算成"稀有"，于是**任何**问题都能匹配上一堆节点
    （实测问"1.1 这一节整体在讲什么"竟然展开了"位串""真值表"）。
    泛词就是泛词，它跟这张图有多少个节点无关。
    """
    return {c for c, k in _term_freq(nodes).items() if k <= max_df}


def _is_specific(question: str, node: dict, distinctive: set[str]) -> bool:
    """这个词面命中是否"说得够具体"，值得**展开**这个节点的完整内容。

    只要求"命中 ≥1 个词"太松：`证明` 是所有证明类节点共有的关键词；
    `论域` 同时挂在"论域"和"证明全称量化的条件语句"上。太松会让无关节点被展开。

    但**光看词长也不行**（第一版就是这么定的）：`反证法` 只有 3 个字，
    没通过 ≥4 字的要求，于是问"怎么用反证法证明？"时目标被**逆否证明**抢走
    （"逆否证明"正好 4 个字）。词长不是"具体"的判据，**在全图里出现得少才是**：
      · 命中 ≥2 个词 → 具体
      · 命中 1 个词 → 该词在全图只有 ≤2 个节点在用（`distinctive`）才算具体
    没过的不是丢掉，而是降到 `page_index` 那种"只列名字"的目录里。
    """
    hits = _hits(question, node)
    if len(hits) >= 2:
        return True
    return any(c in distinctive for c in hits)


# 节点在"同一节"内才算位置相关（"1.7" → 7）
_SECTION_NUM = re.compile(r"^s(\d+)__")


def _location_ok(node: dict, present: set[str], pool: list[dict],
                 distinctive: set[str]) -> bool:
    """位置守门：默认要求"与本次选中的页有交集"或"与目标节点同节"。

    为什么要这道门：词面匹配会跨节乱抓。实测问"条件语句 p → q 的真值表为什么是那样？"，
    "空证明"因为关键词里含"空真"被展开——它在 1.7 节，而这一问在 1.1 节。
    同一个词在不同节里可以是不同的知识点，跨节只按词面抓就会跑题。

    ⚠️ 但**命中"稀有词"时位置不设限**（实测）：问"什么是构造性存在性证明？"，
    检索命中的是 1.8 节那几页，而 `constructive_existence_proof` 的出处页恰好不在其中，
    于是正确答案被位置门挡在外面、一个节点都没展开。
    "构造性存在性证明"这种全图只有 4 个节点在用的词，本身就是强证据，
    不该因为"检索没捞到那一页"而作废。
    """
    if set(node.get("sources") or []) & present:
        return True
    if not pool:
        return False
    secs = {_SECTION_NUM.match(n["id"]).group(1) for n in pool
            if _SECTION_NUM.match(n["id"])}
    m = _SECTION_NUM.match(node["id"])
    if m and m.group(1) in secs:
        return True
    # 稀有词命中 → 放行（构造性存在性证明就属于这种情况）
    return any(len(c) >= 4 and c in distinctive for c in _hits_only(node))


def find_target(g: dict, question: str, present: set[str] | None = None,
                distinctive: set[str] | None = None) -> dict | None:
    """按标题（含 keywords）匹配出本次要讲的那个知识点。挑不出就返回 None。

    优先在"本次检索真的命中了的页"上的节点里挑——那是最强的相关性证据；
    这些页上一个都对不上，才退回到全图去挑（避免"图里没有就硬塞一个"）。
    """
    if distinctive is None:
        distinctive = _distinctive_terms(g["nodes"])
    pool = [n for n in g["nodes"]
            if present and (present & set(n.get("sources") or []))] or list(g["nodes"])
    best = max(pool, key=lambda n: _score_longest_first(question, n, distinctive),
               default=None)
    if best is None:
        return None
    _specific, _title, longest, _e, n_hits = _score_longest_first(
        question, best, distinctive)
    if n_hits == 0 and longest < MIN_TITLE_OVERLAP:
        return None
    return best


def _score_longest_first(question: str, node: dict,
                         distinctive: set[str]) -> tuple[int, int, int, int, int]:
    """目标排序：**标题被整句问到 > 最长命中词 > 先问到的**（越大越优先）。

    实测为什么必须这样：问"什么是构造性存在性证明？"，
    "证明（proof）"只命中 2 个字的泛词 `证明` 却因为它出现得更早就当了目标，
    把 8 个字的 `构造性存在性证明` 挤成了配角。
    """
    hits = _hits(question, node)
    longest = max((len(c) for c in hits), default=0)
    specific = 1 if (len(hits) >= 2 or any(c in distinctive for c in hits)) else 0
    # 标题被整句问到 > 只命中关键词：问"什么是构造性存在性证明？"时，
    # 标题就叫这个的节点必须压过"关键词里恰好有 4 个字对上"的节点。
    title_hit = 1 if node.get("title") and node["title"] in question else 0
    # 全同分时按**提问里先出现的那个**定先后（"怎么用反证法证明？它和逆否证明有什么区别？"
    # 两个词一样长、标题都没整句命中，此时先问的才是主语）。
    spots = [question.find(c) for c in hits if c in distinctive]
    earliest = min(spots) if spots else 10 ** 6
    return (specific, title_hit, longest, -earliest, len(hits))


def select_nodes(g: dict, present_chunk_ids: list[str], question: str = "") -> list[dict]:
    """只挑"该展开讲"的节点：目标 → 其前置/对比 → 与问题词面对上的（≤ MAX_NODES）。

    ⚠️ **不要拿"页命中的多少"去补足**。原来这么做，实测出过一次真事故：
    问"1.1 这一节整体在讲什么？"（没有任何节点标题能对上），补足规则把
    **位串 / 按位运算**这两个恰好横跨多页的节点排到了最前面——
    于是一次"讲这一节概览"的提问，注入的知识结构是"位运算"。
    页命中多不等于该讲，它只说明这个知识点的出处页多。

    剩下的相关内容改由 `page_index` **只列名字**，不展开。

    ⚠️ 另有**绝对优先**的一条：问题里点了节号（"1.1 这一节整体在讲什么"）时，
    这是**概览类**提问——根本不该去"展开某个知识点"。实测不加这条，
    泛词匹配会让它展开"位串""真值表""逻辑门"这种无关节点（`_distinctive_terms` 有记录）。
    """
    by_id = {n["id"]: n for n in g["nodes"]}
    present = set(present_chunk_ids)
    distinctive = _distinctive_terms(g["nodes"])

    if section_outline(g, question):
        return []

    target = find_target(g, question, present, distinctive)
    picked: list[dict] = []
    if target:
        picked.append(target)

    # 顺序：目标 → **问题明确问到的其他节点** → 目标的前置/对比 → 无。
    # 为什么"问到的"要排在前置前面：实测问"直接证明、空证明、平凡证明分别在什么情况下用？"，
    # 前置（证明/证明全称量化的条件语句）把名额占满，**用户点名要的"空证明"反而没进来**。
    # 用户点名的东西优先于系统认为的"先修"。
    asked = [n for n in g["nodes"]
             if n not in picked and _is_specific(question, n, distinctive)
             and _location_ok(n, present, picked, distinctive)]
    asked.sort(key=lambda n: _score(question, n, distinctive), reverse=True)
    for n in asked:
        if len(picked) >= MAX_NODES:
            break
        picked.append(n)

    if target:
        for ref in list(target.get("prerequisites") or []) + list(target.get("contrast") or []):
            if len(picked) >= MAX_NODES:
                break
            if ref in by_id and by_id[ref] not in picked:
                picked.append(by_id[ref])
    return picked[:MAX_NODES]


def page_index(g: dict, present: set[str], picked: set[str],
               question: str = "") -> str:
    """本次这几页上"还有哪些知识点"——**只给名字和类型，不展开**。

    为什么不展开：实测"哪些节点出现在本次页上"主要由**出处页多少**决定，
    与该讲什么无关（见 `select_nodes` 的注释）。所以它们只配当一个"目录"。

    两类会被列进来：
      · 与本次选中的页有交集的（判据可核对：sources ∩ present ≠ ∅）；
      · **问题问到、但说得不够具体**的（如只命中了"证明""论域"这种泛词）——
        不展开它，但也不能装作没有这个知识点。
    """
    rows: list[str] = []
    for n in g["nodes"]:
        if n["id"] in picked:
            continue
        if not ((set(n.get("sources") or []) & present) or _hits(question, n)):
            continue
        kind = "程序" if n.get("type") == "procedure" else "概念"
        rows.append(f"{n['title']}（{kind}）")
        if len(rows) >= 8:
            break
    if not rows:
        return ""
    return ("  本次这几页上还涉及（**只列名字，不要逐个展开讲**）："
            + "、".join(rows))


_SECTION_RE = re.compile(r"(?:^|[^0-9.])([1-9])\.([1-9])(?![0-9.])")


def section_outline(g: dict, question: str) -> str:
    """问题里点了节号（如"1.1 这一节整体在讲什么"）→ 列出**整节**的知识点清单。

    为什么需要它：概览类提问挑不出"目标节点"（没有哪个知识点叫"整体"），
    而按页命中的目录只覆盖本次选中的那几页——实测问"1.1 整体讲什么"时，
    目录里只列出了"位串 / 按位运算"两项，反而更误导。
    节号是问题里**明说的**，所以按它出整节清单是可核对的，不是猜的。
    """
    m = _SECTION_RE.search(question or "")
    if not m:
        return ""
    sec = f"{m.group(1)}.{m.group(2)}"
    secs = {n.get("section") for n in g["nodes"]}
    if sec not in secs:
        return ""
    rows = []
    for n in g["nodes"]:
        if n.get("section") != sec:
            continue
        kind = "程序" if n.get("type") == "procedure" else "概念"
        rows.append(f"{n['title']}（{kind}）")
    if not rows:
        return ""
    return (f"  第 {sec} 节的知识点清单（**只列名字，本节要讲哪些由课件内容决定**）："
            + "、".join(rows))


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
    """返回（注入文本, 被注入的节点 id 列表）。没有可注入的节点时返回 ("", [])。

    注意"没有目标节点"和"没有可注入内容"是两件事：
    问"这一节整体在讲什么"时挑不出目标节点（没有哪个知识点叫"整体"），
    但本次页上的知识点目录仍然有用——**这时也不能返回空**。
    """
    nodes = select_nodes(g, present_chunk_ids, question)
    by_id = {n["id"]: n for n in g["nodes"]}
    # 目录行：问题点明了节号 → 给整节清单；否则只给本次页上的知识点
    index_line = (section_outline(g, question)
                  or page_index(g, set(present_chunk_ids), {n["id"] for n in nodes},
                                question))
    if not nodes and not index_line:
        return "", []
    L: list[str] = []
    L.append("以下是这门课**已有的知识结构**里，与本次课件内容相关的部分。")
    L.append("请用它来组织讲解——尤其是「讲解步骤」那几行：**照那些标签讲，不要自己另编步骤**。")
    L.append("凡标了「课件没交代」的地方，你若补充理由，必须说明那是补充解释而非课件内容。")
    L.append("")
    for n in nodes:
        L.extend(_block_for(n, by_id))
        L.append("")
    # 本次这几页上还有别的知识点 → 只列名（防止模型以为"这门课只有这两三个概念"）
    if index_line:
        L.insert(3, index_line)
    return "\n".join(L).rstrip() + "\n", [n["id"] for n in nodes]


def wrap(text: str) -> str:
    return f"{MARK_BEGIN}\n{text}{MARK_END}"
