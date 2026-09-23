# -*- coding: utf-8 -*-
"""把指定页引用的图片剥出来，供人工查看（判断代码是否为截图）。

临时工具，不参与产品链路。
"""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_pptx_temp import PPTX  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "temp_material" / "_imgs"


def main() -> int:
    nums = [int(x) for x in sys.argv[1:]] or [9, 17, 20, 72, 76]
    z = zipfile.ZipFile(PPTX)
    OUT.mkdir(parents=True, exist_ok=True)
    for num in nums:
        rels = f"ppt/slides/_rels/slide{num}.xml.rels"
        if rels not in z.namelist():
            print(f"slide {num}: 没有 rels")
            continue
        xml = z.read(rels).decode("utf-8")
        targets = re.findall(r'Target="\.\./media/([^"]+)"', xml)
        print(f"slide {num:<3} -> {targets}")
        for t in targets:
            src = "ppt/media/" + t
            if src in z.namelist():
                dst = OUT / f"s{num:02d}_{t}"
                dst.write_bytes(z.read(src))
                print(f"      saved {dst.name}  {z.getinfo(src).file_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
