# -*- coding: utf-8 -*-
"""临时素材：把 PPTX 正文 + 视觉转写的图片内容合成逐页 chunks.jsonl。

产物：`temp_material/ml1/chunks.jsonl`（**不进 knowledge_base/**）
读取路径与正式知识库完全一致，所以 app 侧不需要第二套逻辑。

一页的文本 = 正文段落 + 逐图转写 + 演讲者备注（过滤纯页码）。
顺序：按 PPTX rels 里图片的出现顺序，插在正文之后并标出来源图，
      便于出现问题时回查 `temp_material/_imgs_all/` 下的原图。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from extract_pptx_temp import PPTX, load  # noqa: E402

OUT = ROOT / "temp_material" / "ml1"
STATE = OUT / "_transcribe_state.json"
CHUNKS = OUT / "chunks.jsonl"

# 纯页码/纯数字备注没有信息量，不要喂给模型（AIAA 2711 也做过同类过滤）
def is_noise(text: str) -> bool:
    t = text.strip().lstrip("\ufeff")
    if not t:
        return True
    if t.isdigit():
        return True
    # 幻灯片页码常以 "3 / 83" 之类出现
    if all(ch.isdigit() or ch in " /-–—" for ch in t):
        return True
    return False


def image_order(z, num: int) -> list[str]:
    import re
    import zipfile  # noqa: F401

    rels = f"ppt/slides/_rels/slide{num}.xml.rels"
    if rels not in z.namelist():
        return []
    xml = z.read(rels).decode("utf-8")
    tgts = re.findall(r'Target="\.\./media/([^"]+)"', xml)
    return [t for t in tgts if t.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))]


def main() -> int:
    import zipfile

    if not STATE.exists():
        print("没有转写状态文件，先跑 scripts/transcribe_pptx_images.py")
        return 2
    state = json.loads(STATE.read_text(encoding="utf-8"))
    z = zipfile.ZipFile(PPTX)
    pages, meta = load()

    rows = []
    n_img_used = 0
    n_img_missing = 0
    for num, body, notes, _nmedia in pages:
        parts: list[str] = []
        for t in body:
            t = t.strip().lstrip("\ufeff")
            if not is_noise(t):
                parts.append(t)
        for t in notes:
            t = t.strip().lstrip("\ufeff")
            if not is_noise(t):
                parts.append(f"（演讲者备注）{t}")
        for t in image_order(z, num):
            key = f"s{num:02d}_{t}"
            txt = (state.get(key) or "").strip()
            if txt:
                parts.append(f"【图 {t} 转写】\n{txt}")
                n_img_used += 1
            else:
                n_img_missing += 1
                parts.append(f"【图 {t} 未转写或转写为空】")
        text = "\n\n".join(parts).strip()
        rows.append(
            {
                "chunk_id": f"ml1-p{num:02d}",
                "source_file": PPTX.name,
                "lecture": None,
                "lecture_title": "Machine Learning I",
                "page": num,
                "text": text,
                "char_count": len(text),
                "extraction": "pptx_text+vision",
            }
        )

    OUT.mkdir(parents=True, exist_ok=True)
    with CHUNKS.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    empty = [r["chunk_id"] for r in rows if not r["text"]]
    print(f"写入 {CHUNKS}")
    print(f"页数 {len(rows)}   总字符 {sum(r['char_count'] for r in rows)}")
    print(f"用到转写图 {n_img_used}   转写缺失/空 {n_img_missing}")
    print(f"空页: {empty or '无'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
