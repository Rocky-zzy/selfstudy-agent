# -*- coding: utf-8 -*-
"""继续下载参考文献（第二批）：Korntreff & Prediger (2022) 及其附录。"""
import os
import urllib.request

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, 'docs', 'refs')
os.makedirs(OUT, exist_ok=True)
PROXY = 'http://127.0.0.1:7897'

TARGETS = [
    ('kp2022_full',
     'https://eldorado.tu-dortmund.de/server/api/core/bitstreams/ee96b4bb-dd01-4d26-b370-37bc9aff6701/content'),
    ('kp2022_appendix',
     'https://wwwold.mathematik.tu-dortmund.de/~prediger/veroeff/22-JMD-YouTube-Korntreff-Prediger-Erklaervideos-Anhang.pdf'),
]


def download(url, dest):
    for label, opener in [('direct', urllib.request.build_opener()),
                          ('proxy', urllib.request.build_opener(
                              urllib.request.ProxyHandler({'http': PROXY, 'https': PROXY})))]:
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with opener.open(req, timeout=90) as r:
                data = r.read()
            if len(data) < 1000:
                print('  [%s] too small (%d)' % (label, len(data)))
                continue
            with open(dest, 'wb') as f:
                f.write(data)
            print('  [%s] ok %d KB' % (label, len(data) / 1024))
            return True
        except Exception as e:  # noqa: BLE001
            print('  [%s] %s: %s' % (label, type(e).__name__, str(e)[:110]))
    return False


for name, url in TARGETS:
    print('== %s' % name)
    pdf = os.path.join(OUT, name + '.pdf')
    if not os.path.exists(pdf) and not download(url, pdf):
        print('  FAILED')
        continue
    try:
        doc = fitz.open(pdf)
        txt = '\n\n'.join('--- page %d ---\n%s' % (i + 1, doc.load_page(i).get_text('text'))
                          for i in range(doc.page_count))
        doc.close()
        with open(os.path.join(OUT, name + '.txt'), 'w', encoding='utf-8') as f:
            f.write(txt)
        print('  extracted %d chars, %d pages' % (len(txt), txt.count('--- page ')))
    except Exception as e:  # noqa: BLE001
        print('  extract failed: %s' % e)
print('done ->', OUT)
