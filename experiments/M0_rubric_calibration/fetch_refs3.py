# -*- coding: utf-8 -*-
"""第三批：多轮文本对话（教程对话）会话级编码方案的原始文献。"""
import os
import ssl
import urllib.request

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, 'docs', 'refs')
os.makedirs(OUT, exist_ok=True)

TARGETS = [
    ('chi_tutorial_dialogues',
     'https://www.learnlab.org/research/wiki/images/8/83/Chi_Observing_Tutorial_Dialogues.pdf'),
    ('autotutor_expectations_flairs05',
     'https://new.aaai.org/Papers/FLAIRS/2005/Flairs05-085.pdf'),
]

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

for name, url in TARGETS:
    print('== %s' % name)
    pdf = os.path.join(OUT, name + '.pdf')
    if not os.path.exists(pdf):
        ok = False
        for label, ctx in [('verify', ssl.create_default_context()), ('noverify', CTX)]:
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
                    data = r.read()
                if len(data) < 1000:
                    print('  [%s] too small' % label)
                    continue
                open(pdf, 'wb').write(data)
                print('  [%s] ok %d KB' % (label, len(data) / 1024))
                ok = True
                break
            except Exception as e:  # noqa: BLE001
                print('  [%s] %s: %s' % (label, type(e).__name__, str(e)[:110]))
        if not ok:
            print('  FAILED')
            continue
    try:
        doc = fitz.open(pdf)
        txt = '\n\n'.join('--- page %d ---\n%s' % (i + 1, doc.load_page(i).get_text('text'))
                          for i in range(doc.page_count))
        doc.close()
        open(os.path.join(OUT, name + '.txt'), 'w', encoding='utf-8').write(txt)
        print('  extracted %d chars, %d pages' % (len(txt), txt.count('--- page ')))
    except Exception as e:  # noqa: BLE001
        print('  extract failed: %s' % e)
print('done ->', OUT)
