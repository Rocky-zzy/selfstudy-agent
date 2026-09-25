# 仓库里**没有**什么，以及为什么

> 这个仓库是**程序本体 + 知识结构 + 证据文档**。
> 第三方课程课件与数据集**不入库**（有版权、体积大）。所以 clone 之后，
> 部分流程**不能直接跑**——这份文件说清缺什么、怎么补。

## 没入库的东西

| 路径 | 大小 | 为什么没入库 | 缺了会怎样 |
|---|---|---|---|
| `2711课件/` | 69.8 MB | AIAA 2711 课程 PDF，**第三方版权**，不是本项目的产出 | 无法重建知识库 |
| `RosenDiscreteMath.pdf` | 36.7 MB | Rosen《离散数学及其应用》第 8 版，**第三方教材** | 无法重建第 1 章知识库 |
| `data/rosen/` | ~0.4 MB | 从上面那本教材抽取的知识库——**内容仍是第三方的**，只换了格式 | 同上（跑一次抽取脚本即可） |
| `temp_material/` | 24.7 MB | 用户提供的临时课件（PPTX/PDF）+ 视觉转写用的渲染图 | 临时素材相关的实验无法复现 |
| `datasets/` | 6.8 MB | 第三方数据集（MathDial 等），当前未使用 | 无影响（本来就没用） |
| `knowledge_base/_pages/` | 18.8 MB | 150 dpi 渲染出的页图；**可由课件 PDF 重建** | 无法回查原图核对公式（见下） |
| `data/ratings.jsonl` | — | 本机实测评分（含运行态数据） | 无影响；你跑起来就有了 |
| `data/mqi/` `data/rubrik/` | — | 盲评输入与判定结果（运行态） | 无影响；工具在 `scripts/`，可以重跑 |
| `.env` | — | **含 API key，绝不入库** | 需要自己建（见下） |
| `logs/` | — | 本机日志 | 无影响 |

## 入库的东西（以及为什么）

| 路径 | 为什么入库 |
|---|---|
| `app/` | 程序本体：检索、生成、数学渲染、盲评界面、自检 |
| `scripts/` | 知识库构建、课件转写、回填工具、知识结构校验 |
| `data/graph/` | **L0 知识结构**——手工策划的成果，不是运行产物（`L01.json` 是唯一真相源，`L01.md` 由脚本生成） |
| `knowledge_base/*.jsonl` `manifest.json` `raw/` `transcripts/` | 知识库**文本产物**（1.8 MB），体积小且正是产出 |
| `docs/` | 项目的方法纪律、证据基础、已否决路线、实测记录 |
| `experiments/` | 已封存实验的记录与结论 |

## 恢复步骤

```powershell
# 1) 配置 API key（唯一必需的凭据）
#    在仓库根目录新建 .env，内容一行：
#      DEEPSEEK_API_KEY=sk-你的key

# 2) 装依赖
python -m pip install -r requirements.txt

# 3) 自检（不需要任何课件）
python app\smoke_test.py --no-model
python app\test_mathrender.py
python scripts\ui_regression_test.py --headless
python scripts\graph_check.py --selftest

# 4) 想跑「课件 → 知识库」这条链，需要自己放课件 PDF 到 2711课件\，然后：
python scripts\transcribe_pages.py     # 无文本层的页走视觉转写
python scripts\build_kb.py
python scripts\verify_kb.py

# 5) Rosen 离散数学第 1 章（主数据集）：把 RosenDiscreteMath.pdf 放到仓库根目录，然后：
python scripts\build_rosen_kb.py --chapter 1 --out data\rosen\ch1\chunks.jsonl
python scripts\survey_rosen.py --json  # 需要看全书章节结构时
```

## 一个必须知道的限制

`knowledge_base/_pages/` 没入库，所以**无法回查渲染原图**。

这一点有实际影响：本项目的知识库说明（`knowledge_base/README.md`）里写明，
视觉转写的文本**"作为逐字引用级证据不足"**，凡涉及公式的严格结论建议回查原图。
要恢复这个能力：把课件 PDF 放回 `2711课件/`，跑一次渲染即可重建 `_pages/`。
