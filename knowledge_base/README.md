# AIAA 2711 课件知识库（v1）

面向自学辅助 Agent 的课程知识库，覆盖 AIAA 2711 一学期课件。

## 现状

| 项 | 值 |
|---|---|
| 源文件 | 13 个 PDF，132 页 |
| chunk 数 | **128**（剔除 4 个真空白页） |
| 总字符 | 151,365 |
| 抽取方式 | 文本层 61 页 / 视觉转写 67 页 |
| 课程覆盖 | Lecture 1–9（本学期正课内容）+ 课程概览 + 进阶专题 + Week2 + 实验室介绍 |
| 缺页 | 无 |
| 视觉转写失败 | 0 |

## 目录结构

| 路径 | 内容 |
|---|---|
| `chunks.jsonl` | **主产物**。一行一个 chunk，一行 = 课件的一页 |
| `manifest.json` | 构建清单：文件、页数、抽取方式、哈希、课程目录 |
| `raw/<文件名>.md` | 每个 PDF 的逐页纯文本，便于人工查阅 |
| `transcripts/<lecture>-p<NN>.md` | Lecture 1–9 的逐页视觉转写结果（中间产物，可复用） |
| `_pages/<lecture>-p<NN>.png` | 渲染出的页面图片（中间产物） |

## chunk 字段

```json
{
  "chunk_id": "l01-p03",            // <lecture>-p<页码>，全库唯一
  "source_file": "Lecture Slides S2026\\Lecture 1 ....pdf",
  "lecture": "L01",                  // 非 Lecture 文件为 null
  "lecture_title": "Affine Spaces",
  "page": 3,
  "text": "...",
  "char_count": 1234,
  "extraction": "vision"             // vision | text_layer
}
```

设计原则：**一页一个 chunk，来源可精确追溯到「哪个文件第几页」**。不做语义分块、不做向量检索——分块与检索是组内另一位同学的研究方向，也是后续再议的话题。

## 抽取方式（重要）

课件的两类 PDF 文本可得性完全不同：

1. **有文本层**（`extraction = "text_layer"`）
   `AIAA2711 Course Overview`、`AIAA2711 Advanced Topic`、`AIAA2711 Week 2 Before Class`、
   `Introduction to Research Topics in SSS-CPS Lab`。直接用 PyMuPDF 取文字，无损。

2. **无文本层**（`extraction = "vision"`）
   `Lecture 1`–`Lecture 9`。这些 PDF 由 WPS 导出，**字形被转成了矢量填充路径**：
   `fonts=[]`、`images=0`、`drawings` 每页上千条，PyMuPDF 取不到任何字符。
   处理办法：按 150 dpi 渲染成 PNG，再用 DeepSeek 视觉接口逐页转写为 markdown。

   因此这部分文本是**模型转写的重建结果**，不是原始文本层：
   - 已人工抽查：正文、编号、公式（含 `x^{-1}`、`\mathbb{R}\setminus\{0\}`、
     矩阵分块、下花括号标注）均与页面一致，未发现臆造；
   - 但**数学符号、上下标、下标索引仍可能有个别偏差**，作为「给 Agent 读的讲义内容」够用，
     作为「逐字引用级证据」不足。凡涉及公式的严格结论，建议回查 `_pages/` 下的原图。
   - 每页 md 首行保留了来源注释（文件名 + 页码），可回溯。

3. **空白页不是缺页**
   `Lecture 6` 的第 9–12 页在原 PDF 中即无任何内容（矢量绘图 0 条、渲染图墨迹 0.000%）。
   这类页不会进入 `chunks.jsonl`，只记录在 `manifest.json` 的 `blank_pages` 中，避免
   把「该页没有可见文字」这类元描述当作课件内容喂给 Agent。

## 重新构建

```powershell
# 1) 转写无文本层的页（可断点续跑，已生成的非空文件会跳过）
python scripts\transcribe_pages.py            # 全部
python scripts\transcribe_pages.py l03 l04    # 只补某几讲

# 2) 构建知识库
python scripts\build_kb.py

# 3) 质量自检（漏页 / 异常短页 / 拒答话术）
python scripts\check_transcripts.py

# 4) 结构自检（id 唯一 / 无空文本 / 字段完整 / 与 manifest 一致）
python scripts\verify_kb.py
```

`build_kb.py` 会在 `manifest.json` 的 `missing_transcripts` 中列出「既无文本层也无转写」的页，
正常情况下该列表应为空；`blank_pages` 则是原 PDF 本身就空白的页。

## 已知限制

- 视觉转写基于 150 dpi 渲染图，极小字号或复杂排版处可能丢失个别符号。
- 无文本层的页若转写失败，会被记为 `missing_transcripts`，不会静默填充空内容。
- 尚未做去重、章节切分、术语表、公式结构化（均属后续按需扩展）。
