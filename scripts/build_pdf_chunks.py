# -*- coding: utf-8 -*-
"""临时素材：把 PDF 正文 + 整页视觉转写合成逐页 chunks.jsonl。

产物：`temp_material/nlp6/chunks.jsonl`（**不进 knowledge_base/**）

一页的文本怎么拼（有讲究）：
    1. **正文**取文本层，但**丢掉"光杆标题"行**——这种行在图上内容缺失时会是
       "A CFG consists of 4 elements:" 后面什么都没有，留着只会误导模型
       （实测：第 7 页文本层就长这样）。
    2. **图上内容只从整页转写里拿**，不从逐图里拿——否则同一份定义会出现两遍
       （重复信息会污染"讲全"的判断，而且本身就是有害的冗余）。
    3. 转写里**不重复正文已经说过的要点**做不到自动判断，所以顺序固定为
       "正文要点 → 图内内容"，并在图上内容前标出来源，便于人工核对。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(
    r"C:\Users\27059\.dsh\attachments\v1\files\32"
    r"\328aa1a8edee30493d8267b14cb3ceb2f6fdb33e4f3e698169cea10c3fb9d0dd\lecture-6-qa.pdf"
)
OUT = ROOT / "temp_material" / "nlp6"
STATE = OUT / "_transcribe_state.json"
CHUNKS = OUT / "chunks.jsonl"

HEADER_MARK = "AIAA 4051 Fall 2026 Natural Language Processing"
# 把整页转写的开头"标题："行剥掉（正文里已有标题）
TITLE_PREFIX = re.compile(r"^\s*(标题|Title)\s*[:：]\s*(.+)$")


BULLET_ONLY = re.compile(r"^[\-\*•·o○◦▪]\s*$", re.I)


def is_noise(line: str) -> bool:
    t = line.strip()
    if not t:
        return True
    if HEADER_MARK in t:
        return True
    if BULLET_ONLY.match(t):
        return True          # 光杆列表符号：去重后会剩下空壳，没有信息
    if t.isdigit():
        return True
    if all(ch.isdigit() or ch in " /-–—.:" for ch in t):
        return True
    # 乱码残片：既没有 ASCII 字母数字，也没有汉字，且很短
    has_word = re.search(r"[A-Za-z0-9\u4e00-\u9fff]", t)
    if not has_word and len(t) <= 8:
        return True
    return False


def is_bare_heading(line: str) -> bool:
    """光杆标题：以冒号结尾、或很短且没有句子结构 -> 丢弃。

    理由：正文里这类行在图上内容缺失时会把模型引向"这里应该有内容但没有"，
    而真正的内容在整页转写里。
    """
    t = line.strip()
    if not t:
        return False
    if t.endswith(":") or t.endswith("："):
        return True
    # "• Context-free grammar is a mathematical s" 这种是正文被截断的痕迹，不算标题
    return False


def _norm(s: str) -> str:
    """归一化用于比对：去掉 markdown 符号、空白、弯引号差异。"""
    s = s.strip().lower()
    s = re.sub(r"^[\-\*•o]\s+", "", s)          # 列表符号
    s = re.sub(r"[`*_$\\]", "", s)               # markdown / LaTeX 标记
    s = s.replace("’", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-")
    s = re.sub(r"\s+", " ", s)
    return s.strip(" .:：;；,，、")


def _words(s: str) -> set[str]:
    """取"有信息量"的词：长度 >= 4 的字母/数字串。"""
    return {w for w in re.findall(r"[a-z0-9]{4,}", _norm(s))}


def split_redundant_lines(body_lines: list[str], vision: str) -> tuple[list[str], int]:
    """把正文行分成「转写已覆盖」和「转写没有」两类。

    为什么要按行、按词，而不是整段子串比对：
        实测同一份内容在两处的**换行位置和引号样式不同**（’ vs '），
        整行/整段比对会判不出来，于是同一页内容被贴两遍。
        按"该行的实词是否基本都出现在转写里"判定，对换行和标点差异不敏感。

    返回 (只保留的正文行, 被判为重复的行数)。
    """
    if not body_lines or not vision:
        return body_lines, 0
    vwords = _words(vision)
    if not vwords:
        return body_lines, 0
    keep: list[str] = []
    dropped = 0
    for line in body_lines:
        w = _words(line)
        if len(w) >= 3 and len(w & vwords) / len(w) >= 0.8:
            dropped += 1
            continue
        keep.append(line)
    return keep, dropped


def main() -> int:
    if not STATE.exists():
        print("没有转写状态文件，先跑 scripts/transcribe_pdf_pages.py")
        return 2
    state = json.loads(STATE.read_text(encoding="utf-8"))
    doc = fitz.open(SRC)

    rows = []
    n_pages_with_vision = 0
    n_redundant = 0
    for i, pg in enumerate(doc, 1):
        key = f"p{i:02d}"
        body_lines = []
        for raw in pg.get_text().split("\n"):
            t = raw.strip()
            if is_noise(t):
                continue
            if is_bare_heading(t):
                continue
            body_lines.append(t)

        vision = (state.get(key) or "").strip()
        v_lines = []
        if vision:
            for j, raw in enumerate(vision.split("\n")):
                t = raw.rstrip()
                if j == 0:
                    m = TITLE_PREFIX.match(t)
                    if m:
                        continue  # 标题正文已有
                if HEADER_MARK in t:
                    continue
                v_lines.append(t)
            while v_lines and not v_lines[0].strip():
                v_lines.pop(0)
            while v_lines and not v_lines[-1].strip():
                v_lines.pop()

        parts = []
        vtext = "\n".join(v_lines).strip()
        if body_lines and vtext:
            extra, dropped = split_redundant_lines(body_lines, vtext)
            n_redundant += dropped
            if extra:
                # 正文里有转写没覆盖的内容（典型：文本层残缺、图上有定义）→ 两者都要
                n_pages_with_vision += 1
                # 去重后可能只剩空壳符号，再过一遍噪声过滤
                extra = [l for l in extra if not is_noise(l)]
                if extra:
                    parts.append("\n".join(extra))
                parts.append("【以下为页面图内内容（整页转写）】\n" + vtext)
            else:
                # 正文全被转写覆盖 → 只留转写（更完整、公式是 LaTeX），不贴两遍
                parts.append(vtext)
        elif body_lines:
            parts.append("\n".join(body_lines))
        elif vtext:
            n_pages_with_vision += 1
            parts.append(vtext)
        else:
            print(f"  ⚠️ page {i} 正文与转写都为空")

        text = "\n\n".join(parts).strip()
        title = body_lines[0] if body_lines else f"page {i}"
        rows.append(
            {
                "chunk_id": f"nlp6-p{i:02d}",
                "source_file": SRC.name,
                "lecture": None,
                "lecture_title": "AIAA 4051 L6 · Grammar and Syntax",
                "page": i,
                "text": text,
                "char_count": len(text),
                "extraction": "pdf_text+vision",
                "slide_title": title[:80],
            }
        )

    OUT.mkdir(parents=True, exist_ok=True)
    with CHUNKS.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    empty = [r["chunk_id"] for r in rows if not r["text"]]
    thin = [r["chunk_id"] for r in rows if 0 < r["char_count"] < 120]
    print(f"写入 {CHUNKS}")
    print(f"页数 {len(rows)}   总字符 {sum(r['char_count'] for r in rows)}")
    print(f"正文被转写覆盖、故只留一份的页 {n_redundant}")
    print(f"正文+图内内容都需要的页 {n_pages_with_vision}")
    print(f"空页 {empty or '无'}")
    print(f"偏短页（<120 字，需人工留意）{thin or '无'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
