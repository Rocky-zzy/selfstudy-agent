# -*- coding: utf-8 -*-
r"""L0 知识结构的**校验器 + 渲染器**。

为什么需要一个会报错的校验器（而不是只写个渲染脚本）：
    这张图是**手写的**，手写数据一定会犯三类错——
    ① 引用了不存在的节点/页；② 前置关系成环（A 依赖 B，B 又依赖 A）；
    ③ 子目标挂在概念节点上（概念没有"步骤"，那是**层次放错**，
       正是 `docs/04` §三 记过的同一类错误）。
    这三类都不能靠"看一眼觉得对"发现，必须让脚本**报错**。

    ⚠️ 校验器必须能**拒绝坏数据**（verify 用负例），否则它等于没接线。
    见 `--selftest`：故意造三种坏图，断言它全部被拒。

用法：
    python scripts/graph_check.py                 # 校验 data/graph/*.json
    python scripts/graph_check.py --render L01    # 校验并生成 data/graph/L01.md
    python scripts/graph_check.py --selftest      # 用坏数据验证校验器本身有效
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPH_DIR = ROOT / "data" / "graph"
KB = ROOT / "knowledge_base" / "chunks.jsonl"

VALID_TYPES = {"concept", "procedure"}


class Bad(Exception):
    """图数据不合法。"""


def load_chunk_ids() -> set[str]:
    ids = set()
    with KB.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                ids.add(json.loads(line)["chunk_id"])
    return ids


def validate(g: dict, chunk_ids: set[str]) -> list[str]:
    """返回问题列表；空列表 = 通过。"""
    bad: list[str] = []
    nodes = g.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        return ["nodes 缺失或为空"]

    ids = [n.get("id") for n in nodes]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        bad.append(f"节点 id 重复：{dup}")
    idset = set(i for i in ids if i)

    for n in nodes:
        nid = n.get("id") or "<无 id>"
        if not re.fullmatch(r"[a-z][a-z0-9_]*", str(nid)):
            bad.append(f"{nid}：id 必须是 snake_case")
        if not n.get("title"):
            bad.append(f"{nid}：缺 title")
        if n.get("type") not in VALID_TYPES:
            bad.append(f"{nid}：type 必须是 {VALID_TYPES}")
        if not n.get("sources"):
            bad.append(f"{nid}：缺 sources（没有出处就无法回原文核对）")
        for s in n.get("sources", []):
            if s not in chunk_ids:
                bad.append(f"{nid}：sources 里的 {s!r} 在知识库里不存在")

        for key in ("prerequisites", "contrast"):
            for ref in n.get(key, []):
                if ref not in idset:
                    bad.append(f"{nid}：{key} 引用了不存在的节点 {ref!r}")
        b = n.get("broader")
        if b is not None and b not in idset:
            bad.append(f"{nid}：broader 引用了不存在的节点 {b!r}")
        if b == nid:
            bad.append(f"{nid}：broader 指向自己")

        # ★ 层次检查：子目标只能挂在程序性节点上
        subs = n.get("subgoals")
        if subs:
            if n.get("type") != "procedure":
                bad.append(f"{nid}：type={n.get('type')} 却有 subgoals"
                           f"——概念没有「步骤」，这是层次放错（docs/04 §三 同类错误）")
            for i, sg in enumerate(subs):
                if not sg.get("label"):
                    bad.append(f"{nid}：第 {i+1} 个子目标缺 label")
                if not sg.get("source_line"):
                    bad.append(f"{nid}：第 {i+1} 个子目标缺 source_line"
                               f"（子目标必须能对回课件原文）")

    # 前置关系不能成环
    deps = {n["id"]: list(n.get("prerequisites", [])) for n in nodes if n.get("id")}
    state: dict[str, int] = {}

    def dfs(u: str, path: list[str]) -> None:
        if state.get(u) == 1:
            bad.append("prerequisites 成环：" + " → ".join(path + [u]))
            return
        if state.get(u) == 2:
            return
        state[u] = 1
        for v in deps.get(u, []):
            if v in deps:
                dfs(v, path + [u])
        state[u] = 2

    for u in deps:
        dfs(u, [])
    return bad


def render(g: dict) -> str:
    n = {x["id"]: x for x in g["nodes"]}
    out: list[str] = []
    out.append(f"# L0 最小知识结构 · {g.get('scope')}（{g.get('lecture_title','')}）")
    out.append("")
    out.append("> ⚠️ **本文件由 `scripts/graph_check.py --render` 生成，不要手改。**")
    out.append("> 唯一真相源是 `data/graph/%s.json`。" % g.get("scope"))
    out.append("")
    out.append("> **这是什么**：一门课的最小知识结构——只做**几章强相关**的，"
               "**不是整门课图谱**。")
    out.append("> **解锁依据**：`docs/04` §十。**边界**：它服务决策层，"
               "**不用来证明**「讲解质量更高」（`docs/04` §三）。")
    out.append("")
    out.append("## 字段为什么是这几个")
    out.append("")
    out.append("| 字段 | 为什么需要它 |")
    out.append("|---|---|")
    for k, v in (g.get("field_rationale") or {}).items():
        out.append(f"| `{k}` | {v} |")
    out.append("")
    out.append("## 节点")
    out.append("")
    for x in g["nodes"]:
        src = "、".join(x.get("sources", []))
        out.append(f"### `{x['id']}` — {x['title']}")
        out.append("")
        out.append(f"- **类型**：{'程序性' if x['type']=='procedure' else '概念'}")
        out.append(f"- **出处**：{src}")
        if x.get("prerequisites"):
            out.append("- **前置**：" + "、".join(
                f"{p}（{n[p]['title']}）" for p in x["prerequisites"]))
        if x.get("broader"):
            out.append(f"- **上位**：{x['broader']}（{n[x['broader']]['title']}）")
        if x.get("contrast"):
            out.append("- **对比对象**：" + "、".join(
                f"{c}（{n[c]['title']}）" for c in x["contrast"]))
        if x.get("misconceptions"):
            out.append("- **易错点**：")
            for m in x["misconceptions"]:
                out.append(f"    - {m}")
        if x.get("subgoals"):
            out.append("")
            out.append(f"**★ 子目标（{len(x['subgoals'])} 步）**——"
                       "依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；"
                       "按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。")
            out.append("")
            out.append("| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |")
            out.append("|---|---|---|---|")
            for i, sg in enumerate(x["subgoals"], 1):
                out.append(f"| {i} | **{sg['label']}** | `{sg['source_line']}` "
                           f"| {sg.get('detail','')} |")
            gaps = [(i, sg) for i, sg in enumerate(x["subgoals"], 1)
                    if sg.get("not_in_source")]
            if gaps:
                out.append("")
                out.append("> ⚠️ **课件没交代的地方（讲解若补上，属补充解释而非课件内容）**：")
                for i, sg in gaps:
                    out.append(f"> - 第 {i} 步「{sg['label']}」：{sg['not_in_source']}")
        out.append("")
    return "\n".join(out)


BAD_CASES = {
    "引用了不存在的页": lambda g: g["nodes"][0]["sources"].append("l01-p99"),
    "前置成环": lambda g: (g["nodes"][0]["prerequisites"].append(g["nodes"][1]["id"]),
                          g["nodes"][1]["prerequisites"].append(g["nodes"][0]["id"])),
    "子目标挂在概念上": lambda g: g["nodes"][0].update(
        {"subgoals": [{"label": "x", "source_line": "y"}]}),
}


def selftest(base: dict, chunk_ids: set[str]) -> int:
    """用坏数据验证校验器**真的会拒**。"""
    print("=" * 78)
    print("校验器自检：故意造坏数据，断言全部被拒")
    print("=" * 78)
    fails = 0
    for name, mutate in BAD_CASES.items():
        g = json.loads(json.dumps(base))  # 深拷贝
        mutate(g)
        problems = validate(g, chunk_ids)
        ok = bool(problems)
        print(("  [OK] " if ok else "  [!!] ") + f"{name} → "
              + (problems[0][:70] if problems else "**没被拒**（校验器没接线）"))
        if not ok:
            fails += 1
    print()
    print("校验器有效" if not fails else f"{fails} 个坏例没被拒 —— 校验器无效")
    return 1 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--render", metavar="SCOPE", help="校验并渲染该 scope 的 md")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    chunk_ids = load_chunk_ids()
    files = sorted(GRAPH_DIR.glob("*.json"))
    if not files:
        print(f"没有图数据：{GRAPH_DIR}")
        return 1

    total = 0
    base = None
    for p in files:
        g = json.loads(p.read_text(encoding="utf-8"))
        if base is None:
            base = g
        problems = validate(g, chunk_ids)
        total += len(problems)
        print("=" * 78)
        print(f"{p.name}：{len(g.get('nodes', []))} 个节点")
        print("=" * 78)
        if problems:
            for x in problems:
                print("  [!!] " + x)
        else:
            types: dict[str, int] = {}
            for n in g["nodes"]:
                types[n["type"]] = types.get(n["type"], 0) + 1
            subs = sum(len(n.get("subgoals", [])) for n in g["nodes"])
            print(f"  [OK] 结构合法（{types}，子目标 {subs} 条）")

    if args.render:
        p = GRAPH_DIR / f"{args.render}.json"
        g = json.loads(p.read_text(encoding="utf-8"))
        if validate(g, chunk_ids):
            print("\n✗ 有结构问题，**拒绝渲染**（避免把坏数据固化成文档）")
            return 1
        out = GRAPH_DIR / f"{args.render}.md"
        out.write_text(render(g), encoding="utf-8")
        print(f"\n已渲染 {out}")

    if args.selftest and base is not None:
        print()
        total += selftest(base, chunk_ids)

    print()
    print("结论：" + ("全部通过" if total == 0 else f"{total} 处问题"))
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
