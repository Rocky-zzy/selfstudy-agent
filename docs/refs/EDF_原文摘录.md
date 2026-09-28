# EDF 框架原文摘录（Evidence-Decision-Feedback）

> **来源**：Cohn, C., Guo, S., Rayala, S., et al.（Vanderbilt / OELE Lab）。
> *Evidence-Decision-Feedback: Theory-Driven Adaptive Scaffolding for LLM Agents.*
> **AIED 2026**。arXiv: [2602.01415](https://arxiv.org/abs/2602.01415)（HTML v3 全文已取，2026-09-28）。
> **用途**：阶段二「短期适配」的已有框架候选（评估见 `docs/02` §四）。
> 引用纪律：下面逐字句均为 HTML 全文摘录；未逐字核对的转述处标明〔转述〕。

---

## 1. 框架定义（摘要/引言，逐字）

> "as LLMs evolve from chatbots into autonomous agents, tutoring systems must evolve in
> parallel. We introduce Evidence-Decision-Feedback (EDF), a theoretical framework for
> adaptive scaffolding with LLM agents."

> "EDF integrates elements of intelligent tutoring systems (ITS) and agentic behavior by
> organizing interactions around evidentiary inference, pedagogical decision-making, and
> adaptive feedback."

## 2. 三个模块（逐字，作者自己的模块说明）

**Evidence**：
> "Using Evidence-Centered Design (ECD) and Stealth Assessment, the Evidence module enables
> stakeholders to specify the student data to be monitored to continuously update a
> learner model."

**Decision**：
> "This provides mastery evidence and is used by the Decision module to determine
> pedagogical intent (e.g., boosting self-efficacy) by generating a dialogue policy that
> is consistent with SCT and within the ZPD."

**Feedback**：
> "The Feedback module operationalizes this policy into adaptive scaffolding. When a
> student responds, the response is stored as dialogue evidence to further update the
> learner model."

**可解释性是一等公民**（逐字）：
> "we define interpretability as the extent to which agent output can be traced through
> the input-to-evidence-to-policy-to-feedback chain using observable system artifacts"

## 3. 理论基础（出处，〔转述〕）

- **Evidence-Centered Design**（Mislevy 等 2003）：评估设计三模型——学生模型、证据模型、任务模型；"什么证据能支持什么主张"要先声明。
- **Stealth Assessment**（Shute 2011）：把评估藏进任务行为里，不打断学习。
- **社会文化理论 / ZPD**：策略须落在最近发展区内。

## 4. 实现（Copa 系统，〔转述〕）

- 四个子代理共享一个学习者模型：StrategyAgent / AssessmentAgent / KnowledgeAgent 组成 Evidence 侧，DialogueAgent 覆盖 Decision+Feedback；
- 对话策略族示例：**PROBE_UNDERSTANDING / SUGGEST_ACTION / PUSH_LIMIT**（不同情境下的教学意图）；
- "see what the student sees"：代理只依据学生可见的信息行动，避免信息不对等的"作弊"；
- "bounded autonomy"：子代理各有边界，共享学习者模型是唯一事实源。

## 5. 实证结果（摘要逐字）

> "Findings demonstrate significant negative correlations between student mastery and
> both PROBE talk moves (ρ=−0.46) and reliance behaviors (ρ=−0.26), along with positive
> alignment between understanding and mastery (ρ=0.40)."

〔转述〕n=33 组学生两两组队、6 周真实课堂；四条 RQ：① 脚手架淡出（掌握上升→PROBE 下降、SUGGEST/PUSH 上升）；② 理解与掌握对齐；③ 依赖度随掌握下降；④ 可解释性三条链路（Grounding/Alignment/Faithfulness）均可测且显著。

**helpfulness 悖论**（逐字）：
> "pedagogical agents must be helpful enough to earn trust and invite use when needed,
> yet restrained enough to avoid encouraging cognitive offloading that harms durable
> learning"

〔转述〕作者明确观察到：为防认知卸载而克制直接给答案时，**学生会不满**（frustration）。

## 6. 作者自报局限（逐字）

> "reported relationships are correlational rather than causal"；
> "we evaluate it through only one implementation, Copa"。

〔转述〕另有：适配只用了掌握度单一维度；无随机对照。

---

## 7. 对本项目的适配边界（评估详见 `docs/02` §四）

| EDF 的前提 | 本项目的现实 | 结论 |
|---|---|---|
| 证据源 = 任务工件 + 答题行为 | 只读+提问，**无答题日志** | 证据规格改用**已有的交互信号**（讲法档位/评分原因/追问方向/提问措辞） |
| 结果指标 = 学习侧（掌握、依赖） | 主指标 = **满意度** | helpfulness 悖论是**直接张力**，须作产品取舍摆给用户 |
| 多代理工程 | 单次成文讲解 | 借**职责分离**，不借架构 |
| 相关性证据、单一实现 | — | **方向性依据**，不是"已证明有效" |
