# -*- coding: utf-8 -*-
"""构建 AIAA 2711 课件知识库。

输入：2711课件/ 下的 PDF + knowledge_base/transcripts/ 下的视觉转写
输出：knowledge_base/chunks.jsonl、manifest.json、raw/<file>.md

抽取策略（按页决定，来源可精确追溯到「哪个文件第几页」）：
- text_layer : PDF 自带文本层（4 个辅助 PDF：课程概览、进阶专题、Week2、实验室介绍）
- vision     : PDF 无文本层（Lecture 1-9 为 WPS 导出的矢量轮廓，字形是填充路径），
               先渲染成图再由 DeepSeek 视觉接口逐页转写

刻意不做的事：语义分块、向量检索（属后续讨论，且是组内另一位同学的研究方向）。
"""
import os
import re
import json
import hashlib

import fitz

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '2711课件')
OUT = os.path.join(ROOT, 'knowledge_base')
TRANSCRIPTS = os.path.join(OUT, 'transcripts')

# 视觉模型对空白页会返回「该页没有可见文字 / 页面为空白」这类元描述。
# 若同时确认页面上既无矢量绘图也无嵌入图像，就判定为真空白页并从知识库中剔除。
BLANK_RE = re.compile(
    r'(no visible text|appears (entirely )?blank|image is blank|page (is|appears) blank'
    r'|the page appears|^\s*\[unreadable\]\s*$)', re.I | re.M)


def clean_text(t: str) -> str:
    t = t.replace('\u00a0', ' ')
    t = re.sub(r'[ \t]+', ' ', t)
    t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip()


def lecture_meta(fname: str):
    """从文件名提取 Lecture 编号与标题（用 basename，文件名可能含子目录）。"""
    base = os.path.basename(fname)
    m = re.match(r'Lecture\s+(\d+)\s+(.*?)\.pdf$', base, re.I)
    if m:
        title = re.sub(r'\s*(Lecture Note|sldies|slides)\s*$', '', m.group(2), flags=re.I).strip()
        return 'L%02d' % int(m.group(1)), title
    return None, os.path.splitext(base)[0]


def page_prefix(fname: str) -> str:
    lec, _ = lecture_meta(fname)
    if lec:
        return lec.lower()
    stem = re.sub(r'[^A-Za-z0-9]+', '-', os.path.splitext(os.path.basename(fname))[0]).lower()
    return stem.strip('-')[:32]


def load_transcript(prefix: str, pno: int):
    p = os.path.join(TRANSCRIPTS, '%s-p%02d.md' % (prefix, pno + 1))
    if not os.path.exists(p):
        return None
    body = open(p, encoding='utf-8').read()
    body = re.sub(r'^<!--.*?-->\s*', '', body, flags=re.S)  # 去掉来源注释行
    body = clean_text(body)
    return body or None


def main():
    files = []
    for root, _dirs, fnames in os.walk(SRC):
        for f in fnames:
            if f.lower().endswith('.pdf'):
                files.append(os.path.relpath(os.path.join(root, f), SRC))
    files.sort()

    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, 'raw'), exist_ok=True)

    manifest = {
        'course': 'AIAA 2711',
        'source_dir': SRC,
        'chunking': 'one chunk per PDF page (source-traceable by file + page)',
        'extraction': {
            'text_layer': 'PDF embedded text layer (PyMuPDF)',
            'vision': 'page rendered to PNG, then transcribed by DeepSeek vision API '
                      '(used for Lectures 1-9, whose PDFs are vector-outline and carry no text layer)',
        },
        'files': [],
        'lectures': [],
        'total_pages': 0,
        'total_chunks': 0,
        'total_chars': 0,
        'chunks_by_extraction': {'text_layer': 0, 'vision': 0},
        'total_chars_by_extraction': {'text_layer': 0, 'vision': 0},
        'missing_transcripts': [],
        'blank_pages': [],
    }
    chunks = []

    for fn in files:
        path = os.path.join(SRC, fn)
        doc = fitz.open(path)
        lec, title = lecture_meta(fn)
        prefix = page_prefix(fn)
        raw_pages = []
        n_text = n_vision = 0

        for pno in range(doc.page_count):
            pg = doc.load_page(pno)
            txt = clean_text(pg.get_text('text'))
            extraction = 'text_layer'
            if not txt:
                txt = load_transcript(prefix, pno)
                extraction = 'vision'
                if not txt:
                    manifest['missing_transcripts'].append('%s-p%02d' % (prefix, pno + 1))
                    raw_pages.append('## page %d\n\n[no text layer and no transcript]\n' % (pno + 1))
                    continue
                if BLANK_RE.search(txt) and not pg.get_drawings() and not pg.get_images():
                    manifest['blank_pages'].append('%s-p%02d' % (prefix, pno + 1))
                    raw_pages.append('## page %d\n\n[blank page]\n' % (pno + 1))
                    continue
                n_vision += 1
            else:
                n_text += 1

            raw_pages.append('## page %d\n\n%s' % (pno + 1, txt))
            chunks.append({
                'chunk_id': '%s-p%02d' % (prefix, pno + 1),
                'source_file': fn,
                'lecture': lec,
                'lecture_title': title,
                'page': pno + 1,
                'text': txt,
                'char_count': len(txt),
                'extraction': extraction,
            })

        raw_name = re.sub(r'[\\/]+', '_', os.path.splitext(fn)[0]) + '.md'
        with open(os.path.join(OUT, 'raw', raw_name), 'w', encoding='utf-8') as f:
            f.write('# %s\n\n' % fn + '\n\n'.join(raw_pages))

        sha = hashlib.sha256(open(path, 'rb').read()).hexdigest()
        entry = {
            'file': fn,
            'lecture': lec,
            'title': title,
            'pages': doc.page_count,
            'pages_text_layer': n_text,
            'pages_vision': n_vision,
            'sha256_16': sha[:16],
            'size_mb': round(os.path.getsize(path) / 1e6, 2),
        }
        manifest['files'].append(entry)
        if lec:
            manifest['lectures'].append({
                'lecture': lec, 'title': title, 'pages': doc.page_count,
                'chunk_ids': ['%s-p%02d' % (prefix, p) for p in range(1, doc.page_count + 1)],
            })
        manifest['total_pages'] += doc.page_count
        doc.close()

    for c in chunks:
        manifest['chunks_by_extraction'][c['extraction']] += 1
        manifest['total_chars_by_extraction'][c['extraction']] += c['char_count']
    manifest['total_chunks'] = len(chunks)
    manifest['total_chars'] = sum(c['char_count'] for c in chunks)
    manifest['lectures'].sort(key=lambda x: x['lecture'])

    with open(os.path.join(OUT, 'chunks.jsonl'), 'w', encoding='utf-8') as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + '\n')
    with open(os.path.join(OUT, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print('files=%d | pages=%d | chunks=%d (text_layer=%d, vision=%d) | chars=%d'
          % (len(files), manifest['total_pages'], manifest['total_chunks'],
             manifest['chunks_by_extraction']['text_layer'],
             manifest['chunks_by_extraction']['vision'], manifest['total_chars']))
    if manifest['blank_pages']:
        print('blank pages excluded: %d  (%s)'
              % (len(manifest['blank_pages']), ', '.join(manifest['blank_pages'])))
    if manifest['missing_transcripts']:
        print('MISSING TRANSCRIPTS (%d): %s' % (
            len(manifest['missing_transcripts']),
            ', '.join(manifest['missing_transcripts'][:20])))
    for f in manifest['files']:
        print('  %-70s pages=%-3d text=%-3d vision=%-3d %s'
              % (f['file'][:68], f['pages'], f['pages_text_layer'], f['pages_vision'],
                 f['lecture'] or '-'))


if __name__ == '__main__':
    main()
