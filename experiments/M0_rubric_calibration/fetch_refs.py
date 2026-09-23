# -*- coding: utf-8 -*-
"""下载 MQI 等评估量表的 PDF 并提取文本（web_fetch 不支持 PDF，故自己下）。

用法: python fetch_refs.py
输出: refs/<name>.pdf 与 refs/<name>.txt
"""
import os
import sys
import urllib.request

import fitz  # PyMuPDF

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, 'docs', 'refs')
os.makedirs(OUT, exist_ok=True)

PROXY = 'http://127.0.0.1:7897'

TARGETS = [
    ('mqi_4point_modeling',
     'http://drjennifersuh.onmason.com/wp-content/blogs.dir/1095/files/2016/02/MQI-4-Point-to-use-for-MATH-MODELING.pdf'),
    ('mqi_4point_excerpt',
     'https://s3.amazonaws.com/conference-handouts/2016-nctm-regionals/pdfs/MQI%204-Point_EXCERPT.pdf'),
    ('mqi_hill_ncte',
     'https://cepr.harvard.edu/files/cepr/files/ncte-conference-mqi-hill.pdf'),
]


def download(url, dest):
    for label, opener in [('direct', urllib.request.build_opener()),
                          ('proxy', urllib.request.build_opener(
                              urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY})))]:
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with opener.open(req, timeout=60) as r:
                data = r.read()
            if len(data) < 1000:
                print('  [%s] too small (%d bytes)' % (label, len(data)))
                continue
            with open(dest, 'wb') as f:
                f.write(data)
            print('  [%s] ok %d KB' % (label, len(data) / 1024))
            return True
        except Exception as e:  # noqa: BLE001
            print('  [%s] %s: %s' % (label, type(e).__name__, str(e)[:110]))
    return False


def main():
    for name, url in TARGETS:
        print('== %s' % name)
        pdf = os.path.join(OUT, name + '.pdf')
        if not os.path.exists(pdf):
            if not download(url, pdf):
                print('  FAILED')
                continue
        try:
            doc = fitz.open(pdf)
            txt = '\n\n'.join(
                '--- page %d ---\n%s' % (i + 1, doc.load_page(i).get_text('text'))
                for i in range(doc.page_count))
            doc.close()
            with open(os.path.join(OUT, name + '.txt'), 'w', encoding='utf-8') as f:
                f.write(txt)
            print('  extracted %d chars, %d pages'
                  % (len(txt), txt.count('--- page ')))
        except Exception as e:  # noqa: BLE001
            print('  extract failed: %s' % e)
    print('done ->', OUT)


if __name__ == '__main__':
    main()
