# -*- coding: utf-8 -*-
"""把无文本层的课件页渲染成图片，用 DeepSeek 视觉接口逐页转写。

背景：Lecture 1-9 的 PDF 是 WPS 导出的「矢量轮廓」型（无字体、无文本层、无嵌入图像），
PyMuPDF 取不到任何文字，因此必须自己渲染成位图后再做视觉转写。

特点：
- 逐页一个 markdown 文件，可断点续跑（已存在的非空文件直接跳过）；
- 失败重试 + 失败清单，便于二次补跑；
- 输出路径 knowledge_base/transcripts/<lecture>-p<NN>.md
"""
import base64
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import fitz
from openai import OpenAI

ROOT = r'C:\Users\27059\Desktop\自学agent'
SRC = os.path.join(ROOT, '2711课件')
KB = os.path.join(ROOT, 'knowledge_base')
PNG_DIR = os.path.join(KB, '_pages')
TR_DIR = os.path.join(KB, 'transcripts')

DPI = 150
WORKERS = 4
MAX_ATTEMPTS = 3
MAX_TOKENS = 8192

PROMPT = """You are transcribing ONE page of a university lecture handout for the graduate course "AIAA 2711" (linear algebra, vector calculus, optimization, backpropagation, probability, information theory for AI).

Transcribe ALL visible text faithfully, in natural reading order. Requirements:
- Keep all mathematics; use LaTeX ($...$ or $$...$$) when clearer, otherwise plain unicode.
- Keep numbering, labels, bullet hierarchy, definition/theorem/example markers, and operators exactly as shown.
- Do NOT translate, summarize, explain, add commentary, or invent content.
- Write [unreadable] for genuinely illegible regions.
- Plain markdown only, no code fences around the whole answer."""

_lock = threading.Lock()


def load_key():
    key = os.environ.get('DEEPSEEK_API_KEY')
    if key:
        return key
    for line in open(os.path.join(ROOT, '.env'), encoding='utf-8'):
        if line.startswith('DEEPSEEK_API_KEY='):
            return line.split('=', 1)[1].strip()
    raise RuntimeError('DEEPSEEK_API_KEY not found')


def lecture_prefix(fname):
    m = re.match(r'Lecture\s+(\d+)\b', fname, re.I)
    return ('l%02d' % int(m.group(1))) if m else None


def collect_targets():
    """返回 [(prefix, pdf_path, page_index)]，只取无文本层的页。"""
    targets = []
    for root, _d, fs in os.walk(SRC):
        for f in sorted(fs):
            if not f.lower().endswith('.pdf'):
                continue
            prefix = lecture_prefix(f)
            doc = fitz.open(os.path.join(root, f))
            for pno in range(doc.page_count):
                if prefix is None:
                    continue
                if not doc.load_page(pno).get_text('text').strip():
                    targets.append((prefix, os.path.join(root, f), pno))
            doc.close()
    return targets


def render(pdf_path, pno, out_png):
    doc = fitz.open(pdf_path)
    pix = doc.load_page(pno).get_pixmap(dpi=DPI)
    pix.save(out_png)
    doc.close()
    return pix.width, pix.height


def transcribe(client, png_path):
    b64 = base64.b64encode(open(png_path, 'rb').read()).decode()
    last = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            r = client.chat.completions.create(
                model='deepseek-v4-flash',
                max_tokens=MAX_TOKENS,
                messages=[{
                    'role': 'user',
                    'content': [
                        {'type': 'text', 'text': PROMPT},
                        {'type': 'image_url',
                         'image_url': {'url': 'data:image/png;base64,' + b64}},
                    ],
                }],
            )
            txt = (r.choices[0].message.content or '').strip()
            if txt:
                return txt
            last = 'empty response'
        except Exception as e:  # noqa: BLE001
            last = '%s: %s' % (type(e).__name__, str(e)[:200])
        if attempt < MAX_ATTEMPTS:
            time.sleep(3 * attempt)
    raise RuntimeError(last)


def main():
    only = sys.argv[1:]  # 可选：只跑指定 lecture，如 l01 l02
    os.makedirs(PNG_DIR, exist_ok=True)
    os.makedirs(TR_DIR, exist_ok=True)
    client = OpenAI(api_key=load_key(), base_url='https://api.deepseek.com', timeout=180.0)

    targets = collect_targets()
    if only:
        targets = [t for t in targets if t[0] in only]

    todo = []
    for prefix, pdf, pno in targets:
        md = os.path.join(TR_DIR, '%s-p%02d.md' % (prefix, pno + 1))
        if os.path.exists(md) and os.path.getsize(md) > 20:
            continue
        todo.append((prefix, pdf, pno, md))
    print('targets=%d  todo=%d  workers=%d' % (len(targets), len(todo), WORKERS), flush=True)

    failures = []

    def work(item):
        prefix, pdf, pno, md = item
        png = os.path.join(PNG_DIR, '%s-p%02d.png' % (prefix, pno + 1))
        if not os.path.exists(png):
            render(pdf, pno, png)
        try:
            txt = transcribe(client, png)
        except Exception as e:  # noqa: BLE001
            with _lock:
                failures.append({'page': '%s-p%02d' % (prefix, pno + 1), 'error': str(e)[:300]})
                print('FAIL %s-p%02d  %s' % (prefix, pno + 1, str(e)[:160]), flush=True)
            return
        with open(md, 'w', encoding='utf-8') as f:
            f.write('<!-- source: %s | page %d | vision transcription -->\n\n'
                    % (os.path.basename(pdf), pno + 1))
            f.write(txt + '\n')
        with _lock:
            print('ok   %s-p%02d  %d chars' % (prefix, pno + 1, len(txt)), flush=True)

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = [ex.submit(work, it) for it in todo]
        for _ in as_completed(futs):
            pass

    if failures:
        with open(os.path.join(KB, 'transcribe_failures.json'), 'w', encoding='utf-8') as f:
            json.dump(failures, f, ensure_ascii=False, indent=2)
    print('done. failures=%d' % len(failures), flush=True)


if __name__ == '__main__':
    main()
