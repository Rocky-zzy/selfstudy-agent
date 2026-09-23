# M0：Explanation Quality Rubric v0.2 校准

目的：用真实样本回答 `docs/05_Explanation_Quality_Rubric_v0.2.md` §E 的三个问题——
**区分度**（基线是否已经通过该条目）、**一致性**（两个评分者能否一致）、**准则效度**（该条目与整体质量判断是否相关）。

---

## 一、设计

| 环节 | 文件 | 说明 |
|---|---|---|
| 题库 | `items.json` | 8 个知识点：7 个多步解释题（T2）+ 1 个事实题（T1，q8，用来测适用性门槛） |
| 基线回答 | `baseline.jsonl` | 中性助教 prompt（`prompt_baseline.txt`）+ 知识库材料。**检索不是本实验变量**（属材料侧研究），所以两边给同样的材料，只考察「同样的材料怎么讲」 |
| 缺陷注入 | `inject.py` → `injected.jsonl` | 每条 rubric 条目一个定向缺陷，注入到该条目当前通过的基线回答上 |
| 评判 | `judge.py` → `verdicts.jsonl` | 4 个独立 pass |
| 分析 | `analyze.py` | 输出区分度 / 灵敏度 / 特异度 / 一致性 / 准则效度 |
| 人工盲评 | `human_rating_sheet.md` | 成对比较 + 单独评分，答案钥匙在 `human_rating_key.json` |

### 四个评判 pass

| id | prompt | 作用 |
|---|---|---|
| `sat_a` / `sat_b` | `prompt_judge_satisfaction.txt` | 同一 prompt 跑两次 → **自一致性** |
| `def` | `prompt_judge_defect.txt` | 问法相反（问「缺陷是否存在」）、条目乱序 → 近似跨评分者一致性 |
| `hol` | `prompt_holistic.txt` | 不带 rubric 的整体 1–5 分 → **准则效度**的参照 |

> ⚠️ 三个 rubric 评判者都是同一个模型，误差相关。它们之间的一致率**只能当作真实评分者间一致性的上界近似**，真实 IAA 必须靠 `human_rating_sheet.md`。

### 为什么用「缺陷注入」而不只是随机取样

随机取样回答不了「这一条是否**专门**测到了它该测的东西」。注入给每个条目一个干净的 2×2：注入后**目标条目应翻成 fail**（灵敏度），**其他条目应保持原判**（特异度）。

---

## 二、今晚要跑的命令

```powershell
$env:PYTHONIOENCODING='utf-8'
cd C:\Users\27059\Desktop\自学agent

# 1) 评判（64 次 API 调用，8 并发，可中断续跑）
python experiments\M0_rubric_calibration\judge.py

# 2) 分析
python experiments\M0_rubric_calibration\analyze.py | Tee-Object experiments\M0_rubric_calibration\analysis.txt
```

**耗时**：单次评判调用约 1–2 分钟（要按 8 条 rubric 逐条推理），64 次 ÷ 8 并发 ≈ **8–16 分钟**。

**太慢的话**，跳过自一致性那一轮，省 16 次调用（不影响区分度/灵敏度/特异度）：

```powershell
python experiments\M0_rubric_calibration\judge.py --judges sat_a,def,hol
```

**中断了就直接重跑同一条命令**：`verdicts.jsonl` 里已有的 `(response_id, judge)` 会自动跳过。
若最后一轮改过 `--judges`，注意 `sat_b` 的缺失会让 `analyze.py` 的自一致性一栏变成空——不影响其他结论。

进度可以边跑边看：`Get-Content experiments\M0_rubric_calibration\verdicts.jsonl | Measure-Object -Line`。

---

## 三、跑完之后

把 `analyze.py` 的输出贴给我，或者只说一句「跑完了」，我来读文件写 `report.md`。

人工盲评（`human_rating_sheet.md`，8 对 + 3 个单评）**不急着做**，可以等 LLM 结果出来后再挑最需要验证的几对做，节省时间。

---

## 四、已知的坑（三个都是实际踩过的）

1. **prompt 里含 JSON 输出示例时不能用 `str.format()`**：示例的字面大括号会被当成占位符并抛 `KeyError`。评判 prompt 现在用 `<<<MATERIAL>>>` 这类占位符 + `str.replace`。
2. **`Out-String` 会缓冲全部输出**，后台任务的进度行一条都看不到，看起来像卡死。现在输出直接流到 `judge.log`。
3. **`src/llm_client.py` 的 `MAX_TOKENS=4096` 把 thinking 的推理 token 也算在内**，推理长时输出会被**静默截断**（第 3 题的基线回答就是这样被截掉的）。`gen.py` 因此自带 API 调用：提高预算并检测 `finish_reason == "length"`，截断就加大预算重试。**这个缺陷仍在 `src/llm_client.py` 里，side-line 若用它跑批量实验需要注意。**
