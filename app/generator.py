# -*- coding: utf-8 -*-
"""讲解生成层：两个条件。

性质（见 docs/00_错题本.md §四）：**对照实现，不是"消融分组"**。
两条件共用同一检索器、同一上下文拼装、同一模型、同一参数，
**唯一差异是系统指令**：

  baseline   —— 无任何"讲解方式"约束（=「同款 LLM 冷启动 + 整页课件原文直灌」）
  optimized  —— 只用 docs/03 §六 里有出处的 4 条约束

因此两组差异可归因到 prompt，而不是检索或模型。
APP_STRIP_OPT=1 可关掉 optimized 的 4 条约束（变成与 baseline 同指令），
用于自查"差异是否真的来自这些约束"。
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field

ROOT_ENV = ".env"

DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"

# ---------------------------------------------------------------------------
# 提示词
# ---------------------------------------------------------------------------

_COMMON_TASK = """你是一个课程自学辅助助手。学生会就下面的课件内容提问。

**下面是整讲的课件原文，是你唯一的依据；但它不等于你这次要讲的范围。**
只回答学生问到的那个点，不要因为原文里还有别的内容就顺带把整章串一遍。

<<<COURSEWARE>>>
{context}
<<<END COURSEWARE>>>

<<<STUDENT QUESTION>>>
{question}
<<<END STUDENT QUESTION>>>"""

# ---------------------------------------------------------------------------
# 范围约束：**两个条件完全相同**（用户 2026-09-17 要求）
#
# 为什么两条件都给：这是"输出范围"约束，属于**决策层**。若只给 optimized，
# 优化版可能仅因为"写得短"而赢，就分不出是"讲得好"还是"讲得短"了。
# 两条件共用 → 范围不是变量，差异仍可归因到讲解方式。
#
# ⚠️ 代价（不得隐去）：基线因此**不再是"完全无约束的冷启动"**。
#    定调里"优于同款 LLM 冷启动"严格来说需要一个无约束基线；
#    本阶段的基线是"同款 LLM + 整讲直灌 + 范围约束"，措辞不得僭越。
# ---------------------------------------------------------------------------
_SHARED_SCOPE = """## 这次讲解的范围（两个条件共同遵守）

- **只回答学生问到的那个点。** 课件原文里有别的内容，不代表这次要一起讲。
- **不要分章节、不要写"小结"、不要罗列课件里与问题无关的其它定义。**
- 结尾用一句话**主动提出可以继续深入的方向**，把"要不要展开"交给学生决定。
   **这个方向必须是课件里真实存在的内容**；课件里没有的不要提——实测发生过
   "推荐了课件里没有的问题"（see docs/07 第 8 条）。

## 输出格式（两个条件共同遵守）

学生在网页上读，看到的是**纯文本**。所以：

- **代码必须放进围栏代码块**（三反引号 + 语言名），每行独立成行、保留缩进。
   **不要**把代码混在句子里，也不要只写成行内 `代码` 的样子。
- 代码里的变量名、函数名用反引号包成 `行内代码`，与普通文字分开。
- 数学公式用 LaTeX（`$...$` 或 `$$...$$`）。
- 不要用"|"拼表格——纯文本里对不齐。

## 术语怎么处理（两个条件共同遵守）

- **专业术语第一次出现时落地**：写成 **`English（中文）` + 一句白话说明它在这门课里指什么**。
   例：**`constituent（成分）`**：一组词合起来当一个语法单位用。
   ★ **同一个术语全篇只加注这一次**；之后再出现**直接用英文，不要再加括号**。
   ⚠️ 只对"这门课的专业术语"这么做；**不要给普通词加注**。
   （实测：只写"不要重复解释"不够，模型仍会对同一个词加注两次 → 必须写成"只加注这一次"。）

   *依据*：用户两次反馈"专业术语让人读起来阻力很大"「既然我是要详细讲说明我对这两个知识点不熟悉」（`docs/07`）；
   MQI 编码 13 也要求区分日常含义与数学含义、讲不清就记为不精确。
   **共用而非条件专属**：呈现层问题，只给一侧会让"谁加注谁赢"。
"""

# ---------------------------------------------------------------------------
# 讲法三档：**两个条件共用**（用户 2026-09-19 定）
#
# 为什么必须共用：讲法是"讲多全"的层面，属于决策层。若只给 optimized，
# 优化版可能仅因为"讲得全"而赢，就分不出是"讲得好"还是"讲得多"。
#
#   brief    —— 与之前一致（实测在"粗略过一遍"上最好：4/4/4）
#   detailed —— 用户定义：「对我提出的范围内的所有知识点细讲」，
#               并且「不要超出课件内容，又要包含这个课件中知识点部分的全部内容」
#               **2026-09-22 改为按教学骨架走**（见下方"骨架"一节）
#   followup —— 针对追问：只补问到的那个点，不重复已讲过的
#
# ## 详细档的教学骨架（用户 2026-09-22 定：「以这个为骨架应该是没毛病的」）
#
# 八个部件：是什么 → 为什么需要它 → 直觉 → 形式表达 → 怎么做（每步给理由）
#          → 例子 → 结果怎么看 → 常见的坑 → 何时用/不用
#
# 依据：`docs/09` 的 L2–L4/L6/L8（提取自用户给的 L7 system prompt，用户判断支持）
#      + `docs/03` §六 已有出处的判据（讲 why 不讲 how、给反例/边界）。
# ⚠️ 证据状态：**Ⓒ 采自该案例，非实验结论**。所以只能写"按该案例先做一版"。
# 动机：MQI 编码 3 的 High 要求"解释**是这篇的主要特征**"，
#      而实测两轮都卡在 Mid（`docs/12`）——散文体没有骨架，撑不起"主要特征"。
#
# ## 关于"设问式自我解释"：已**移出详细档**（2026-09-22）
#
# 原约束 10 要求"设问 + 紧接着自答"。依据是 self-explanation 元分析
# （4 篇 / 112 研究 / 6,450 学生，加权 ES = 0.55；Visible Learning MetaX；
#  Bisra et al. 2018）。用户 2026-09-19 定的边界是"设问但不要求作答"，避免加重负担。
#
# ⚠️ **但实测抓到了它造成的具体缺陷**：模板化设问会产生"问题与答案不一致"的段落
#    （CNF 那问：标题问"为什么要引入新非终结符"，正文却说方案恰恰不引入）。
#    Rubrik 那轮判 Coherence=No，MQI 那轮判编码 13=1。
# → **骨架取代了它**：骨架里的"为什么需要它"与"每一步为什么"就是促发自行组织的机制，
#    而且是结构性的、不依赖模板化问句。所以详细档不再需要单独的设问约束。
#    followup 档仍保留一句，因为追问场景没有骨架可依。
# ---------------------------------------------------------------------------
_TEACHING_BRIEF = """## 这次怎么讲：概览

学生要的是一张地图，不是细节。

- **只给骨架**：这一块在讲什么、内部怎么组织、各部分什么关系。
- **长度控制在 600–800 字。** 写完若超出，**删掉次要内容，而不是把它们压成更短的句子**。
   宁可这一层讲透，也不要几层都浅浅带过。
"""

_TEACHING_DETAILED = """## 这次怎么讲：详细

学生明确要求详细讲。**他是因为不熟悉才要详细，所以术语和跳跃对他都是负担。**

### 每讲一个知识点，按这个骨架走

- ★ **骨架的九个部件**（顺序不要换）：
    **是什么 → 为什么需要它 → 直觉 → 形式表达 → 怎么做 → 例子 → 算出来怎么看 → 常见的坑 → 什么时候用 / 不该用**
- ★★ **不是每个知识点都要把九段写全——按"这段到底需不需要"决定**。
    判断规则如下。

    **必须写**（少一段就是没讲清）：
    · **是什么**：定义 / 结论本身。
    · **怎么做**：需要动手操作或推导的内容（算法、证明、代码、计算）。
      ★ **如果上文的「知识结构」给了这个知识点的讲解步骤（带【】的标签），
      「怎么做」就按那些步骤组织：一步一段、顺序照给、别自己另编一套步骤。**
      没给步骤标签时才自己拆。
    · **为什么需要它**：当学生可能问"为什么要造这个概念"时（新引入的抽象概念）。
    **按需写**（不需要就跳过；跳过时不要留空壳、不要写"此处略"）：
    · **直觉**：概念抽象或反直觉时才写；名字已自解释的不写。
    · **形式表达**：课件里有公式 / 代码时才写。
    · **例子**：概念是抽象定义时必写；课件里已给过的不重复。
    · **算出来怎么看**：只在"算 / 推导"类内容里写。
    · **常见的坑**：有真实易错点时才写，**不要为了凑格式硬编一个**。
    · **什么时候用 / 不该用**：只有方法、算法、公式、模型才需要。

    **判断标准就一句话**：*少了这一段，学生会不会就看不懂、或做不出来？*
    会 → 写；不会 → **跳过**。

    *依据*：专长逆转效应（Kalyuga 等；2025 元分析）——**教学支持应随先验知识增加而撤除**，
    对已掌握的人同样的支持会变成干扰；worked examples 的 fading 研究同样主张支持要逐步撤掉。
    ⚠️ 所以"每段都走一遍"是**错的**：它把支持量固定死了。
- **宁可短而全，不要长而空**：如果有哪一段只能写出套话，那说明这段本来就不需要。
- **复杂内容要再拆**：一个知识点里若含多层结构（如"三步的转换"），
    先讲清每一步在干什么，再把它们串起来——不要一口气倒完。
    前置知识不够时，用一两句先补上，但**不要跑题**。

### 还有三条硬要求

- ★ **范围内一个都不许漏**：学生问到范围内的**每一个知识点都要讲到**。
    范围内有几个就讲几个，每个都按上面的骨架走。**宁可这样显得长，也不许漏。**
- ★ **只讲课件里有的**：不许引入课件之外的结论。
    **例子/反例优先用课件里给的**；课件没给、你自己补的，必须标注 `（补充例子）`，
    且**不得改动课件里的数值与顺序**。
- ★ **代码逐行注释**：给出代码时，用注释说明每一行在做什么；
    循环、下标、累积这类操作，补一句**执行到这里变量是什么状态**。

- **详略由内容决定，不设字数上限**：该讲完的必须讲完。
    但骨架的每一段都只讲一遍，**不要用不同说法把同一件事讲两遍**。
"""

_TEACHING_FOLLOWUP = """## 这次怎么讲：追问

学生是在你已经讲过一遍之后的追问。

- **只回答追问的那个点**，不要重复已经讲过的整块内容。
- 讲"为什么"时用设问：先自己问一句，紧接着自己回答，**不要等学生作答**。
- 长度按需要定，不必压得很短，也不要借机把整个范围重讲一遍。
"""

TEACHING_MODES = ("brief", "detailed", "followup")
TEACHING_LABEL = {"brief": "概览", "detailed": "详细", "followup": "追问"}
DEFAULT_TEACHING = "brief"

_TEACHING_BLOCK = {
    "brief": _TEACHING_BRIEF,
    "detailed": _TEACHING_DETAILED,
    "followup": _TEACHING_FOLLOWUP,
}

_BASELINE_HEAD = """你是一个乐于助人的课程辅导助手。请针对学生的问题给出讲解。
"""

# optimized 在共用约束之上，再加 docs/03 §六 的 4 条（逐条对应出处）。
# **编号从 21 起**：共用块的讲法约束用到 20，两段拼在一起时不能撞号
# （曾经撞过：共用到 20、专属又从 13 起，出现两个"13"）。
#   22 → 机制一（Mayer / CLT: redundancy, coherence, split-attention）
#   23 → MQI 编码 3「Explanations」原文：focus on why, "Do NOT count 'how'"
#   24 → Thurm C1 四级措辞：至少一处"不止简短的、涉及含义的解释"
#   25 → MQI 编码 4 Mathematical Sense-Making：含义 / 合理性 / 找反例
_OPTIMIZED_HEAD = """你是一个课程自学辅助助手，为一名正在自学的学生讲解课件内容。
"""

_OPTIMIZED_EXTRA = """
## 怎么把那一层讲好（附加约束）

- **不重复**：同一信息不用两种形式说两遍。不写寒暄、不写无信息量的总结或鼓励话术。
    公式与解释它的文字必须紧邻。
    ⚠️ 这与"骨架里每个知识点都走一遍"**不冲突**：
    同一个知识点只走一遍骨架；不同知识点各走一遍，不算重复。
- **讲 why，不只讲 how**：说清"为什么这样做成立/为什么不成立""为什么这个方法合适"。
    只描述步骤不算解释。凡有定义或结论，交代其含义。
- 至少给出一处不止简短、真正涉及含义的解释，而不是一笔带过。
- 交代概念的合理性：它是什么意思、为什么这样定义是合理的；合适时给一个反例或边界情形。

只依据提供的课件原文回答。若课件原文不足以回答该问题，明确说出缺什么，
不要用课件之外的推测填充。"""

# 兼容：旧的模块级常量（早期引用过；保留以免打断外部脚本）
_BASELINE_SYSTEM = _BASELINE_HEAD + "\n" + _SHARED_SCOPE
_OPTIMIZED_SYSTEM = _OPTIMIZED_HEAD + "\n" + _SHARED_SCOPE + _OPTIMIZED_EXTRA


def number_constraints(text: str) -> str:
    """把行首的 `- ` 占位符按顺序编号成 `1. `、`2. `…

    为什么不让各块自己写编号：**手写编号每加一条就要全库排查，而且会因为
    "不同讲法档的共用块长度不同"而出现断号**——曾经出现过 brief 档 11→22 的断号，
    以及拼起来有两个 "13" 的撞号。改为拼装时统一编号，编号天然连续唯一。
    """
    n = 0
    out: list[str] = []
    for line in text.split("\n"):
        if line.startswith("- "):
            n += 1
            out.append(f"{n}. " + line[2:])
        else:
            out.append(line)
    return "\n".join(out)


@dataclass
class GenConfig:
    api_key: str
    base_url: str = DEFAULT_BASE_URL
    model: str = DEFAULT_MODEL
    temperature: float = 0.3
    max_tokens: int = 4000
    timeout: float = 180.0
    strip_opt_constraints: bool = False

    @classmethod
    def from_env(cls) -> "GenConfig":
        return cls(
            api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
            base_url=os.environ.get("DEEPSEEK_BASE_URL", DEFAULT_BASE_URL),
            model=os.environ.get("DEEPSEEK_MODEL", DEFAULT_MODEL),
            strip_opt_constraints=os.environ.get("APP_STRIP_OPT", "") == "1",
        )


@dataclass
class GenResult:
    condition: str
    text: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    finish_reason: str = ""
    truncated: bool = False
    attempts: int = 1
    system_prompt: str = ""
    error: str | None = None
    warnings: list[str] = field(default_factory=list)


def system_prompt_for(
    condition: str,
    strip_opt_constraints: bool = False,
    teaching: str = DEFAULT_TEACHING,
) -> str:
    """拼出 system prompt。

    结构：条件开头句 + （范围 + 格式 + 术语 + **讲法**：两条件完全相同）+ 条件专属约束。
    最后统一编号（`number_constraints`），所以各块自己**不要写编号**。
    teaching 校验放在这里，写错档位会直接报错，不会静默退回默认档。
    """
    if teaching not in _TEACHING_BLOCK:
        raise ValueError(f"未知讲法：{teaching!r}（只支持 {TEACHING_MODES}）")
    common = _SHARED_SCOPE + "\n" + _TEACHING_BLOCK[teaching]
    if condition == "baseline":
        return number_constraints(_BASELINE_HEAD + "\n" + common)
    if condition == "optimized":
        if strip_opt_constraints:
            return number_constraints(_BASELINE_HEAD + "\n" + common)
        return number_constraints(_OPTIMIZED_HEAD + "\n" + common + _OPTIMIZED_EXTRA)
    raise ValueError(f"未知条件：{condition!r}（只支持 baseline / optimized）")


def user_prompt(context: str, question: str) -> str:
    return _COMMON_TASK.replace("<<<COURSEWARE>>>", context, 1).replace(
        "<<<STUDENT QUESTION>>>", question, 1
    )


def _client(cfg: GenConfig):
    from openai import OpenAI  # 延迟导入，便于无依赖时也能跑检索自检

    if not cfg.api_key:
        raise RuntimeError(
            "没有读到 DEEPSEEK_API_KEY。请确认工作区根目录 .env 里有这一项。"
        )
    return OpenAI(api_key=cfg.api_key, base_url=cfg.base_url, timeout=cfg.timeout)


def generate(
    condition: str,
    context: str,
    question: str,
    cfg: GenConfig | None = None,
    client=None,
    teaching: str = DEFAULT_TEACHING,
) -> GenResult:
    """生成一段讲解。

    teaching: 讲法三档（brief / detailed / followup）。**两条件共用**，
              所以它不参与对照——保证差异仍只来自"讲得好不好"。

    实现注意：**必须检查 finish_reason == 'length'**——
    因为 max_tokens 会把推理 token 也算进预算，截断是**静默**发生的，
    且只在最长最复杂的输入上出现。命中则加大预算重试。
    """
    cfg = cfg or GenConfig.from_env()
    system = system_prompt_for(condition, cfg.strip_opt_constraints, teaching)
    user = user_prompt(context, question)
    client = client or _client(cfg)

    budget = cfg.max_tokens
    last_err: str | None = None
    for attempt in range(1, 4):
        try:
            resp = client.chat.completions.create(
                model=cfg.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                temperature=cfg.temperature,
                max_tokens=budget,
                stream=False,
            )
        except Exception as e:  # 网络 / 鉴权 / 配额
            last_err = f"{type(e).__name__}: {e}"
            if attempt < 3:
                time.sleep(1.5 * attempt)  # 简单退避：无间隔重试会直接撞限流
                continue
            return GenResult(
                condition=condition,
                text="",
                model=cfg.model,
                attempts=attempt,
                system_prompt=system,
                error=last_err,
            )

        choice = resp.choices[0]
        finish = getattr(choice, "finish_reason", "") or ""
        text = (choice.message.content or "").strip()
        usage = getattr(resp, "usage", None)

        if finish == "length":
            if attempt < 3:
                budget = int(budget * 1.8)
                continue
            return GenResult(
                condition=condition,
                text=text,
                model=cfg.model,
                prompt_tokens=getattr(usage, "prompt_tokens", 0) or 0,
                completion_tokens=getattr(usage, "completion_tokens", 0) or 0,
                finish_reason=finish,
                truncated=True,
                attempts=attempt,
                system_prompt=system,
                warnings=["达到 max_tokens 上限仍被截断，已重试 2 次加倍预算"],
            )

        return GenResult(
            condition=condition,
            text=text,
            model=cfg.model,
            prompt_tokens=getattr(usage, "prompt_tokens", 0) or 0,
            completion_tokens=getattr(usage, "completion_tokens", 0) or 0,
            finish_reason=finish,
            attempts=attempt,
            system_prompt=system,
        )

    return GenResult(
        condition=condition, text="", model=cfg.model, error=last_err, system_prompt=system
    )
