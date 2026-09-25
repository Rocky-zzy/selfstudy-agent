# -*- coding: utf-8 -*-
r"""Rosen 教材（Discrete Mathematics and Its Applications, 8th ed.）结构勘察。

用途：把 1118 页教材的**章节结构**扫出来，供"只挑几章强相关的"决策使用。

做法：Rosen 每页页眉带「节号 + 节名 + 原书页码」，例如 `1.6 Rules of Inference | 77`。
      用它把页归到节段，比按页切 chunk 更贴教材本身的结构。

用法：
    python scripts/survey_rosen.py            # 打印章节结构
    python scripts/survey_rosen.py --json     # 输出机器可读结构
"""

from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "RosenDiscreteMath.pdf"

# 页眉形如： "1.6 Rules of Inference \n 77 \n ..."
HDR = re.compile(r"^(\d{1,2}\.\d{1,2})\s+([A-Z][^\n]{2,60})\s*$", re.M)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    import fitz

    d = fitz.open(PDF)
    segs: dict[tuple[str, str], list[int]] = collections.OrderedDict()
    chars: dict[tuple[str, str], int] = collections.Counter()
    unlabeled = 0
    for i in range(d.page_count):
        t = d[i].get_text()
        m = HDR.search(t[:200])
        if not m:
            unlabeled += 1
            continue
        name = m.group(2).strip()
        # 目录页会有 "1.1 Propositional Logic . . . . 5" 这种点线，过滤掉
        if " . ." in name or name.endswith("."):
            unlabeled += 1
            continue
        key = (m.group(1), name)
        segs.setdefault(key, []).append(i + 1)
        chars[key] += len(t)

    # 真正的"节"：至少 2 页
    real = {k: v for k, v in segs.items() if len(v) >= 2}

    if args.json:
        out = [
            {"number": k[0], "title": k[1], "pages": [v[0], v[-1]],
             "page_count": len(v), "chars": chars[k]}
            for k, v in real.items()
        ]
        p = ROOT / "data" / "rosen_structure.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"写入 {p}（{len(out)} 节）")
        return 0

    print(f"总页数 {d.page_count}；识别出节段 {len(real)} 个；无页眉页 {unlabeled} 页")
    cur = None
    total_pages = 0
    for (num, name), pages in real.items():
        ch = num.split(".")[0]
        if ch != cur:
            cur = ch
            print()
            print("=" * 70)
            print(f"第 {ch} 章")
            print("=" * 70)
        total_pages += len(pages)
        print(f"  {num:<7} {name[:42]:<44} p{pages[0]:<5}–{pages[-1]:<5} "
              f"{len(pages):>2}页 {chars[(num, name)]:>7,}字")
    print()
    print(f"这些节合计 {total_pages} 页")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
