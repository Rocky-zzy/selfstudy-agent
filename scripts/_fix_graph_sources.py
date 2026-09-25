# -*- coding: utf-8 -*-
"""定向修复：子目标的 `source_line` 找不到时，**去全节原文里搜**再判断。

三种结局，分开处理（不许"看着差不多就放过"）：
  A. 这段话在**本节另一页**上 → 把那一页加进该节点的 sources（引用出处写错了，不是编的）
  B. 这段话**跨页**（在拼接后的全节文本里才连得上）→ 同样把相关页并进 sources
  C. 全节都搜不到 → **拒绝**，打印出来给人/模型改。编造就是编造，不能自动"修"成能过的样子。
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
SECTIONS = ["1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8"]

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def norm(s: str) -> str:
    s = s or ""
    for a, b in (("\ufb01", "fi"), ("\ufb02", "fl"), ("\ufb00", "ff"),
                 ("\ufb03", "ffi"), ("\ufb04", "ffl"),
                 ("\u2013", "-"), ("\u2014", "-"), ("\u2212", "-"),
                 ("\u2018", "'"), ("\u2019", "'"), ("\u201c", '"'), ("\u201d", '"'),
                 ("\u00a0", " ")):
        s = s.replace(a, b)
    return re.sub(r"\s+", "", s)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="把能定位到的修复写回 json")
    args = ap.parse_args()

    chunks: dict[str, str] = {}
    for line in KB.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            chunks[r["chunk_id"]] = r.get("text") or ""

    unresolved = 0
    fixed = 0
    for sec in SECTIONS:
        p = SRC / f"graph_{sec}.json"
        if not p.exists():
            continue
        g = json.loads(p.read_text(encoding="utf-8"))
        sec_chunks = sorted([k for k in chunks if k.startswith(f"rosen-c{sec}-")])
        joined = "".join(norm(chunks[k]) for k in sec_chunks)
        dirty = False
        for n in g["nodes"]:
            hay = "".join(norm(chunks.get(s, "")) for s in n.get("sources", []))
            for i, sg in enumerate(n.get("subgoals") or [], 1):
                sl = sg.get("source_line") or ""
                if not sl or norm(sl) in hay:
                    continue
                # A：落在本节某一页上 → 把那一页并进 sources
                where = [k for k in sec_chunks if norm(sl) in norm(chunks[k])]
                if where:
                    for k in where:
                        if k not in n["sources"]:
                            n["sources"].append(k)
                    n["sources"] = sorted(set(n["sources"]),
                                          key=lambda x: sec_chunks.index(x))
                    print(f"  [A 修好] {sec} {n['id']} 第 {i} 步：原文在 {'、'.join(where)}"
                          f"（原本只写了 {'、'.join(sg.get('_old_src') or []) or '该页之外的页'}）")
                    fixed += 1
                    dirty = True
                    continue
                # B：跨页 → 用"任意相邻两页拼接"再试
                pair = None
                for a, b in zip(sec_chunks, sec_chunks[1:]):
                    if norm(sl) in norm(chunks[a]) + norm(chunks[b]):
                        pair = [a, b]
                        break
                if pair:
                    for k in pair:
                        if k not in n["sources"]:
                            n["sources"].append(k)
                    print(f"  [B 修好] {sec} {n['id']} 第 {i} 步：跨页（{'、'.join(pair)}）")
                    fixed += 1
                    dirty = True
                    continue
                # C：编的
                print(f"  [C 编造] {sec} {n['id']} 第 {i} 步：全节都搜不到 → {sl[:70]!r}")
                if norm(sl) in joined:
                    print("        （但去空白后在整节拼接文本里能找到——检查是否跨了 2 页以上）")
                unresolved += 1
        if dirty and args.write:
            p.write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\n修复 {fixed} 条，无法定位 {unresolved} 条"
          + ("（已写回）" if args.write else "（未写回，加 --write 才写）"))
    return 1 if unresolved else 0


if __name__ == "__main__":
    raise SystemExit(main())
