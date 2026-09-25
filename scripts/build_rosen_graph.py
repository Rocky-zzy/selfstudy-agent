# -*- coding: utf-8 -*-
"""把一节的抽取结果**先验一遍**，再把 8 节合并成一张图。

为什么要分两步：
    整章 120 页一次性抽完再检查，一旦提示词理解偏了就是 8 节全废（`docs/00` M11）。
    所以先在**单节**上把"结构 + 溯源"验通，再做**只做合并**这个纯机械步骤。

用法：
    python scripts/build_rosen_graph.py --check 1.1      # 只验一节
    python scripts/build_rosen_graph.py --merge          # 验证全部并合并
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "temp_material" / "rosen_sec"
KB = ROOT / "data" / "rosen" / "ch1" / "chunks.jsonl"
GRAPH_DIR = ROOT / "data" / "graph"
SECTIONS = ["1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8"]

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def norm(s: str) -> str:
    """去掉空白并统一排版变体，再比子串。

    为什么不能只 `re.sub(r"\\s+", "")`：PDF 抽出来的正文里有连字（ﬁ/ﬂ）和多种破折号，
    手抄或转述时会被"自动纠正"成 fi 和 --，于是**明明抄对了却报找不到**——
    校验器频繁假报错，人就会开始忽略它。宁可先统一，也不让假报错毁掉校验器的可信度。
    """
    s = s or ""
    for a, b in (("\ufb01", "fi"), ("\ufb02", "fl"), ("\ufb00", "ff"),
                 ("\ufb03", "ffi"), ("\ufb04", "ffl"),
                 ("\u2013", "-"), ("\u2014", "-"), ("\u2212", "-"),
                 ("\u2018", "'"), ("\u2019", "'"), ("\u201c", '"'), ("\u201d", '"'),
                 ("\u00a0", " ")):
        s = s.replace(a, b)
    return re.sub(r"\s+", "", s)


def load_chunks() -> dict[str, str]:
    out = {}
    for line in KB.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            out[r["chunk_id"]] = r.get("text") or ""
    return out


def validate_section(g: dict, section: str, chunks: dict[str, str]) -> list[str]:
    """单节校验：节点内部一致 + 每个 source_line 真能在该页找到。"""
    bad: list[str] = []
    raw = g.get("nodes")
    if not isinstance(raw, list) or not raw:
        return [f"{section}：nodes 缺失或为空"]
    nodes = [{**n, "id": f"s{section.replace('.', '')}__{n.get('id')}"} for n in raw]
    ids = [n["id"] for n in nodes]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        bad.append(f"{section}：id 重复 {dup}")
    idset = set(ids)
    # 本节允许引用的页：chunk_id 前缀
    allowed = {k for k in chunks if k.startswith(f"rosen-c{section}-")}
    for n in nodes:
        nid = n["id"]
        if not re.fullmatch(r"[a-z][a-z0-9_]*", str(nid).split("__", 1)[-1]):
            bad.append(f"{nid}：id 不是 snake_case")
        if not n.get("title"):
            bad.append(f"{nid}：缺 title")
        if n.get("type") not in ("concept", "procedure"):
            bad.append(f"{nid}：type={n.get('type')!r} 非法")
        if not n.get("keywords"):
            bad.append(f"{nid}：缺 keywords（没它就没法把提问匹配到节点）")
        if not n.get("sources"):
            bad.append(f"{nid}：缺 sources")
        for s in n.get("sources", []):
            if s not in allowed:
                bad.append(f"{nid}：sources 里的 {s!r} 不属于本节 {section}")
        for key in ("prerequisites", "contrast"):
            for ref in n.get(key) or []:
                if f"s{section.replace('.', '')}__{ref}" not in idset:
                    bad.append(f"{nid}：{key} 引用了本节不存在的节点 {ref!r}")
        b = n.get("broader")
        if b and f"s{section.replace('.', '')}__{b}" not in idset:
            bad.append(f"{nid}：broader 引用了本节不存在的节点 {b!r}")
        subs = n.get("subgoals") or []
        if subs and n.get("type") != "procedure":
            bad.append(f"{nid}：concept 却有 subgoals（层次放错）")
        if n.get("type") == "procedure" and not subs:
            bad.append(f"{nid}：procedure 却没有 subgoals（那它不是程序性知识）")
        for i, sg in enumerate(subs, 1):
            if not sg.get("label"):
                bad.append(f"{nid}：第 {i} 步缺 label")
            sl = sg.get("source_line") or ""
            if not sl:
                bad.append(f"{nid}：第 {i} 步缺 source_line")
                continue
            hay = "".join(norm(chunks.get(s, "")) for s in n.get("sources", []))
            if norm(sl) not in hay:
                bad.append(f"{nid}：第 {i} 步的 source_line 在 sources 里找不到"
                           f" —— 不许凭印象写原文：{sl[:44]!r}")
    # 前置不能成环
    deps = {n["id"]: [f"s{section.replace('.', '')}__{p}" for p in n.get("prerequisites") or []]
            for n in nodes}
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


def cross_links(nodes: list[dict], chunks: dict[str, str]) -> int:
    """跨节关系**不入库**，恒返回 0——理由见 `graph_inject.prior_index`。

    试过一版规则（"更早节的节点名出现在本节点原文页上就算前置"）：
    114 个节点被补出 **1211 条**前置，平均每个 10 条以上。
    那不是知识结构，是"同在一章"的同义词——注入时会等于把整章塞进去。
    所以跨节信息改成**讲解时现算、只给名字**（可核对：共用原文页）。"""
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", metavar="SECTION")
    ap.add_argument("--merge", action="store_true")
    ap.add_argument("--patch", action="store_true",
                    help="把某条 source_line 改成真原文（需与 --node/--step/--set-to 同用）")
    ap.add_argument("--node", help="节点 id（不带 sNN__ 前缀）")
    ap.add_argument("--step", type=int, help="第几步（从 1 起）")
    ap.add_argument("--set-to", dest="set_to", help="替换成的新 source_line（会被验证）")
    ap.add_argument("--add-source", dest="add_source", metavar="CHUNK_ID",
                    help="同时把该页加进节点 sources")
    args = ap.parse_args()

    chunks = load_chunks()

    if args.patch:
        if not (args.node and args.step and args.set_to):
            print("--patch 需要同时给 --node / --step / --set-to")
            return 2
        if args.add_source and args.add_source not in chunks:
            print(f"没有这个 chunk_id：{args.add_source}")
            return 2
        hit = 0
        for sec in SECTIONS:
            p = SRC / f"graph_{sec}.json"
            if not p.exists():
                continue
            g = json.loads(p.read_text(encoding="utf-8"))
            for n in g["nodes"]:
                if n["id"] != args.node:
                    continue
                sg = n["subgoals"][args.step - 1]
                old = sg["source_line"]
                if args.add_source and args.add_source not in n["sources"]:
                    n["sources"].append(args.add_source)
                hay = "".join(norm(chunks.get(s, "")) for s in n["sources"])
                if norm(args.set_to) not in hay:
                    print(f"✗ 拒绝写入：新 source_line 在 {n['sources']} 里找不到")
                    return 1
                sg["source_line"] = args.set_to
                p.write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")
                print(f"已修 {sec} {args.node} 第 {args.step} 步：")
                print(f"  旧：{old[:70]!r}")
                print(f"  新：{args.set_to[:70]!r}")
                hit += 1
        if not hit:
            print(f"✗ 没找到节点 {args.node!r}")
            return 1
        return 0

    todo = [args.check] if args.check else SECTIONS
    ok_files: list[tuple[str, dict]] = []
    total_bad = 0
    for sec in todo:
        p = SRC / f"graph_{sec}.json"
        if not p.exists():
            print(f"  [--] {sec}：还没有 {p.name}")
            total_bad += 1
            continue
        g = json.loads(p.read_text(encoding="utf-8"))
        bad = validate_section(g, sec, chunks)
        types = {}
        for n in g["nodes"]:
            types[n["type"]] = types.get(n["type"], 0) + 1
        subs = sum(len(n.get("subgoals") or []) for n in g["nodes"])
        if bad:
            print(f"  [!!] {sec}：{len(bad)} 处问题")
            for x in bad:
                print("        " + x)
            total_bad += len(bad)
        else:
            print(f"  [OK] {sec}：{len(g['nodes'])} 节点（{types}），子目标 {subs} 条")
            ok_files.append((sec, g))

    if args.merge:
        if total_bad:
            print(f"\n✗ 有 {total_bad} 处问题，**拒绝合并**（别把坏数据固化成图）")
            return 1
        nodes: list[dict] = []
        for sec, g in ok_files:
            pre = f"s{sec.replace('.', '')}__"
            for n in g["nodes"]:
                n = dict(n)
                n["section"] = sec
                n["id"] = pre + n["id"]
                for k in ("prerequisites", "contrast"):
                    if n.get(k):
                        n[k] = [pre + x for x in n[k]]
                if n.get("broader"):
                    n["broader"] = pre + n["broader"]
                nodes.append(n)
        cross_links(nodes, chunks)  # 目前是 no-op，保留调用点是为了让"跨节不入库"这个决定可见
        out = {
            "scope": "rosen-ch1",
            "lecture_title": "Rosen《离散数学及其应用》第 1 章 基础：逻辑与证明",
            "kb": "data/rosen/ch1/chunks.jsonl",
            "field_rationale": {
                "prerequisites": "决定先讲什么；缺前置要先补（先行组织者 / pre-training）",
                "broader": "决定讲多全（讲到上位就停还是下钻）",
                "contrast": "给骨架的「常见的坑」与对比提供明确对象（MQI 编码 13）",
                "misconceptions": "让「常见的坑」有清单可对，而不是自由发挥",
                "subgoals": "仅程序性节点；给标签优于自己生成（Morrison 等 2020）",
                "sources": "每个节点可回原文核对（chunk_id 真实存在 + 子目标原文可逐字命中）",
            },
            "nodes": nodes,
        }
        GRAPH_DIR.mkdir(parents=True, exist_ok=True)
        dst = GRAPH_DIR / "rosen-ch1.json"
        dst.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"\n已合并 {len(nodes)} 个节点 → {dst.relative_to(ROOT)}")
    return 1 if total_bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
