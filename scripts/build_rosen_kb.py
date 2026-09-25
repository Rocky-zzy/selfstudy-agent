# -*- coding: utf-8 -*-
r"""把 Rosen 教材抽取成知识库格式（一页一 chunk）。

## 为什么是一页一 chunk（沿用现有架构）

现有知识库（AIAA 2711）就是"一页一 chunk、来源可精确追溯到文件+页码"，
`retrieval.py` / `app` 全都按这个假设写的。这里**不引入新的分块尺度**——
只为 Rosen 多做一件事：把**节号/节名/原书页码**记进字段，因为这三个是后面建知识结构的依据。

## 为什么先干跑

Rosen 有 1118 页，全本抽取是不可逆的大动作。所以支持 `--sections` 只抽指定节，
先用 1.1 / 1.2 两节验证"页眉解析 → chunk → 页码对不对"，通了再放全章。

用法：
    python scripts/build_rosen_kb.py --sections 1.1 1.2 --out data/rosen/_dry.jsonl
    python scripts/build_rosen_kb.py --chapter 1 --out knowledge_base_rosen/chunks.jsonl
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "RosenDiscreteMath.pdf"

# Rosen 的**左右页页眉格式不同**（2026-09-26 实测，看原始行才看清）：
#   右页： `1.1 Propositional Logic` / `3`
#   左页： `2` / `1 / The Foundations: Logic and Proofs` / `1.1.2`
#   章首： `1` / `C H A P T E R` / 章名 / 节名列表
# 第一版把页眉当成"一行"写正则（用了 re.M 去整页找），结果**只认出右页、漏掉一半页**
# ——13 页 vs 应有 24 页。教训：**先看原始行，再写正则**。
# 现在全部按**单行**匹配（不带 re.M），一页里逐行找线索，哪条在就用哪条。
HDR_RIGHT = re.compile(r"^(\d{1,2}\.\d{1,2})\s+([A-Z][^\n]{2,60})\s*$")
CHAP = re.compile(r"^(\d{1,2})\s*/\s*([A-Z][^\n]{2,70})\s*$")
PAGENO = re.compile(r"^(\d{1,4})$")
# 左页的小节号提示，如 "1.1.2"
SEC_HINT = re.compile(r"^(\d{1,2}\.\d{1,2})\.\d+$")


def parse_page(text: str, pdf_page: int) -> dict:
    """从一页文本里解析出节号、节名、小节号、原书页码。

    **按行解析，不按整页正则**。原因（2026-09-26 实测）：
      · 右页页眉：`1.1 Propositional Logic` / `3`        （节号+节名，然后页码）
      · 左页页眉：`2` / `1 / The Foundations: Logic and Proofs` / `1.1.2`  （页码、章名、小节号）
      · 章首页：  `1` / `C H A P T E R` / 章名 / 节名列表
    第一版把它们当"一行"写正则，结果**只认出右页、漏掉一半页**。
    改成一页里找三条线索，哪条在就用哪条。
    """
    lines = [l.strip() for l in text.split("\n")]
    head = lines[:8]

    printed = None
    for l in head:
        m = PAGENO.match(l)
        if m:
            printed = int(m.group(1))
            break

    sec_no = sec_title = None
    subsec = None
    mode = "none"

    for l in head:
        if not l:
            continue
        # 右页：节号 + 节名
        m = HDR_RIGHT.match(l)
        if m and not sec_no:
            sec_no, sec_title, mode = m.group(1), m.group(2).strip(), "section_right"
            continue
        # 左页/章首页：章号 / 章名
        m = CHAP.match(l)
        if m and not sec_title:
            sec_title, mode = m.group(2).strip(), "chapter_side"
            continue
        # 左页的小节号提示，如 1.1.2
        m = SEC_HINT.match(l)
        if m and not subsec:
            subsec = m.group(1)
            if not sec_no:
                sec_no = subsec
                mode = "subsec_left"

    return {
        "section": sec_no,
        "section_title": sec_title,
        "subsec": subsec,
        "head_mode": mode,
        "printed_page": printed,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sections", nargs="*", help="只抽这些节，如 1.1 1.2")
    ap.add_argument("--chapter", type=int, help="抽整章")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    import fitz

    d = fitz.open(PDF)
    # 先扫一遍确定每页属于哪节（页眉解析），再做**前向填充**：
    # 左页页眉只有 "页码 | 章号 / 章名"，解析不出节号；而节一旦开始就延续到下一节头。
    # 不做前向填充就会把一半页（左页）判成"无节"而漏掉。
    pages = []
    cur_sec, cur_title = None, None
    for i in range(d.page_count):
        t = d[i].get_text()
        info = parse_page(t, i + 1)
        if info["section"] and info["head_mode"] in ("section_right", "section_left"):
            cur_sec, cur_title = info["section"], info["section_title"]
        elif info["head_mode"] == "chapter_opener":
            cur_sec, cur_title = info["section"], info["section_title"]
        else:
            # 左页等：沿用当前节
            info["section"], info["section_title"] = cur_sec, cur_title
            if info["head_mode"] == "none":
                info["head_mode"] = "carried"
        info["pdf_page"] = i + 1
        info["text"] = t
        pages.append(info)

    keep = []
    for p in pages:
        if args.sections:
            if p["section"] in args.sections:
                keep.append(p)
        elif args.chapter is not None:
            pref = f"{args.chapter}."
            # 节号同章，或章首页
            if (p["section"] or "").startswith(pref) or (
                p["head_mode"] == "chapter_opener" and (p["section"] or "").startswith(pref)
            ):
                keep.append(p)
        else:
            keep.append(p)

    if not keep:
        print("没有匹配的页。检查 --sections / --chapter 参数。")
        return 1

    rows = []
    for p in keep:
        text = p["text"].strip()
        if not text:
            continue
        rows.append({
            "chunk_id": f"rosen-c{p['section'] or 'x'}-pdf{p['pdf_page']:04d}",
            "source_file": PDF.name,
            "lecture": p["section"] or None,
            "lecture_title": p["section_title"] or "",
            "page": p["pdf_page"],
            "printed_page": p["printed_page"],
            "head_mode": p["head_mode"],
            "text": text,
            "char_count": len(text),
            "extraction": "text_layer",
        })

    out = Path(args.out)
    if not out.is_absolute():
        out = ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    secs = sorted({r["lecture"] for r in rows if r["lecture"]})
    nohdr = [r["chunk_id"] for r in rows if r["head_mode"] == "none"]
    nopage = [r["chunk_id"] for r in rows if r["printed_page"] is None]
    print(f"写入 {out}")
    print(f"  页数 {len(rows)}   总字符 {sum(r['char_count'] for r in rows):,}")
    print(f"  覆盖节 {secs}")
    print(f"  无页眉的页 {len(nohdr)} {nohdr[:5]}")
    print(f"  取不到原书页码的页 {len(nopage)} {nopage[:5]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
