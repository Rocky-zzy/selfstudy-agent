# L0 最小知识结构 · rosen-ch1（Rosen《离散数学及其应用》第 1 章 基础：逻辑与证明）

> ⚠️ **本文件由 `scripts/graph_check.py --render` 生成，不要手改。**
> 唯一真相源是 `data/graph/rosen-ch1.json`。

> **这是什么**：一门课的最小知识结构——只做**几章强相关**的，**不是整门课图谱**。
> **解锁依据**：`docs/04` §十。**边界**：它服务决策层，**不用来证明**「讲解质量更高」（`docs/04` §三）。

## 字段为什么是这几个

| 字段 | 为什么需要它 |
|---|---|
| `prerequisites` | 决定先讲什么；缺前置要先补（先行组织者 / pre-training） |
| `broader` | 决定讲多全（讲到上位就停还是下钻） |
| `contrast` | 给骨架的「常见的坑」与对比提供明确对象（MQI 编码 13） |
| `misconceptions` | 让「常见的坑」有清单可对，而不是自由发挥 |
| `subgoals` | 仅程序性节点；给标签优于自己生成（Morrison 等 2020） |
| `sources` | 每个节点可回原文核对（chunk_id 真实存在 + 子目标原文可逐字命中） |

## 节点

### `s11__proposition` — 命题（proposition）

- **类型**：概念
- **出处**：rosen-c1.1-pdf0025、rosen-c1.1-pdf0026
- **对比对象**：s11__compound_proposition（复合命题与逻辑联结词（compound proposition / logical connectives））
- **易错点**：
    - 把疑问句或祈使句当成命题（What time is it? / Read this carefully. 只是提问或命令，没有真值）
    - 把含未赋值变量的句子当成命题（x + 1 = 2 既不为真也不为假，只有给变量赋值之后才成为命题）
    - 因为自己不知道真假就断定某句不是命题（命题只要求客观上非真即假，不要求我们知道答案）

### `s11__compound_proposition` — 复合命题与逻辑联结词（compound proposition / logical connectives）

- **类型**：概念
- **出处**：rosen-c1.1-pdf0025、rosen-c1.1-pdf0026、rosen-c1.1-pdf0034
- **前置**：s11__proposition（命题（proposition））
- **对比对象**：s11__proposition（命题（proposition））
- **易错点**：
    - 把 ¬p ∧ q 读成 ¬(p ∧ q)（否定运算符先于所有二元运算符作用）
    - 以为合取与析取之间没有优先级，把 p ∨ q ∧ r 读成 (p ∨ q) ∧ r
    - 以为条件运算符优先于析取，把 p → q ∨ r 读成 (p → q) ∨ r

### `s11__truth_table` — 真值表（truth table）

- **类型**：概念
- **出处**：rosen-c1.1-pdf0027、rosen-c1.1-pdf0034
- **前置**：s11__proposition（命题（proposition））
- **对比对象**：s11__bit_string（位与位串（bit, Boolean variable, bit string））
- **易错点**：
    - 命题变元只写一行真值，漏掉另一种可能（每个变元都要取遍真与假）
    - 把中间子表达式的列当成最终结果，不知道最后一列才是整个复合命题的真值

### `s11__negation` — 否定（negation）

- **类型**：概念
- **出处**：rosen-c1.1-pdf0026、rosen-c1.1-pdf0027
- **前置**：s11__proposition（命题（proposition））
- **对比对象**：s11__converse_contrapositive_inverse（逆命题、否命题与逆否命题（converse, contrapositive, inverse））
- **易错点**：
    - 把 has at least 32 GB of memory 的否定写成 has at most 32 GB（正确否定是 has less than 32 GB）
    - 把否定理解成换一句意思相反的话，而不是把原命题的真值取反

### `s11__conjunction` — 合取（conjunction）

- **类型**：概念
- **出处**：rosen-c1.1-pdf0027
- **前置**：s11__compound_proposition（复合命题与逻辑联结词（compound proposition / logical connectives））
- **对比对象**：s11__disjunction（析取（disjunction））
- **易错点**：
    - 认为 but 不能算合取（The sun is shining, but it is raining 就是两个命题的合取）
    - 把合取的真值条件记反，以为有一个为真就为真

### `s11__disjunction` — 析取（disjunction）

- **类型**：概念
- **出处**：rosen-c1.1-pdf0027、rosen-c1.1-pdf0028
- **前置**：s11__compound_proposition（复合命题与逻辑联结词（compound proposition / logical connectives））
- **对比对象**：s11__exclusive_or（异或（exclusive or））
- **易错点**：
    - 把析取当成二者只能取其一（析取是相容或，两个都真时仍为真）
    - 看到 or 就直接译成析取，不判断句子本意是相容或还是排斥或

### `s11__exclusive_or` — 异或（exclusive or）

- **类型**：概念
- **出处**：rosen-c1.1-pdf0028、rosen-c1.1-pdf0029
- **前置**：s11__disjunction（析取（disjunction））
- **对比对象**：s11__disjunction（析取（disjunction））
- **易错点**：
    - 把异或当成至少一个为真（异或要求恰好一个为真，两个都真时为假）
    - 把自然语言里的 or 一律当成异或（学过微积分或计算机导论是相容或）

### `s11__conditional_statement` — 条件语句（conditional statement / implication）

- **类型**：概念
- **出处**：rosen-c1.1-pdf0029、rosen-c1.1-pdf0030、rosen-c1.1-pdf0031
- **前置**：s11__compound_proposition（复合命题与逻辑联结词（compound proposition / logical connectives））
- **对比对象**：s11__biconditional（双条件语句（biconditional））
- **易错点**：
    - 把 p only if q 当成 q → p（only 决定方向：p only if q 与 if p, then q 同义）
    - 前件为假时以为条件语句为假（前件为假时条件语句为真）
    - 把 q is necessary for p 与 p is sufficient for q 的方向搞反（两种说法都等价于 if p, then q）
    - 要求前件与后件之间有因果或语义关联，因而否认 If Juan has a smartphone, then 2 + 3 = 5 是真命题
    - 把编程语言里的 if p then S 当成逻辑蕴含（S 是程序段而不是命题）

### `s11__converse_contrapositive_inverse` — 逆命题、否命题与逆否命题（converse, contrapositive, inverse）

- **类型**：概念
- **出处**：rosen-c1.1-pdf0032
- **前置**：s11__conditional_statement（条件语句（conditional statement / implication））
- **对比对象**：s11__conditional_statement（条件语句（conditional statement / implication））
- **易错点**：
    - 认为逆命题或否命题与原条件语句等价（本节指出这是最常见的逻辑错误之一，只有逆否命题总与原命题同真值）
    - 把逆否命题写成对前件和后件直接取否（逆否命题要先交换前件与后件、再分别取否）
    - 当前件真而后件假时，以为逆命题和否命题也是假的（此时它们都是真的）
    - 把中文的否命题与命题的否定混为一谈

### `s11__biconditional` — 双条件语句（biconditional）

- **类型**：概念
- **出处**：rosen-c1.1-pdf0033
- **前置**：s11__conditional_statement（条件语句（conditional statement / implication））
- **对比对象**：s11__conditional_statement（条件语句（conditional statement / implication））
- **易错点**：
    - 把自然语言里的 if..., then... 直接当成双条件（If you finish your meal, then you can have dessert 字面上只断言一个方向，另一个方向只是隐含）
    - 把双条件当成条件语句之外的第三种东西，不知道它与两个方向的条件语句的合取真值完全相同
    - 在两个命题都假时把双条件判为假（同真或同假时双条件都为真）

### `s11__bit_string` — 位与位串（bit, Boolean variable, bit string）

- **类型**：概念
- **出处**：rosen-c1.1-pdf0035、rosen-c1.1-pdf0036
- **前置**：s11__truth_table（真值表（truth table））
- **对比对象**：s11__truth_table（真值表（truth table））
- **易错点**：
    - 把位串的长度当成它表示的数值（长度是位串中位的个数）
    - 把按位运算当成整数的算术运算
    - 记反位与真值的对应（1 表示真、0 表示假）

### `s11__build_truth_table` — 构造复合命题的真值表

- **类型**：程序性
- **出处**：rosen-c1.1-pdf0027、rosen-c1.1-pdf0034
- **前置**：s11__truth_table（真值表（truth table））、s11__compound_proposition（复合命题与逻辑联结词（compound proposition / logical connectives））

**★ 子目标（3 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **数清命题变元的个数，据此列出全部真值组合（每个组合占一行）** | `Because this truth table involves two propositional variables p and q, there are four rows in this truth table, one for each of the pairs of truth values TT, TF, FT, and FF.` |  |
| 2 | **按由内向外的构造顺序，为出现的每个子表达式各开一列** | `the truth value of each compound expression that occurs in the compound proposition as it is built up` |  |
| 3 | **逐列填完中间结果后，在最后一列读出整个复合命题的真值** | `Finally, the truth value of (p ∨¬q) →(p ∧q) is found in the last column.` |  |

### `s11__translate_natural_language` — 把自然语言语句翻译成命题逻辑表达式

- **类型**：程序性
- **出处**：rosen-c1.1-pdf0028、rosen-c1.1-pdf0030、rosen-c1.1-pdf0033
- **前置**：s11__proposition（命题（proposition））、s11__compound_proposition（复合命题与逻辑联结词（compound proposition / logical connectives））、s11__conditional_statement（条件语句（conditional statement / implication））、s11__biconditional（双条件语句（biconditional））

**★ 子目标（4 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **先找出句中的每个原子命题，并分别给它们命名** | `using the propositions p: “A student who has taken calculus can take this class” and q: “A student who has taken introductory computer science can take this class.”` |  |
| 2 | **先按句子本意判断 or 是相容或还是排斥或，再选定对应的联结词** | `We assume that this statement means that students who have taken both calculus and introductory computer science can take the class, as well as the students who have taken only one of the two subjects.` |  |
| 3 | **遇到 only if / necessary / sufficient / unless 时先定方向，再写成条件语句** | `To remember that “p only if q” expresses the same thing as “if p, then q,” note that “p only if q” says that p cannot be true when q is not true.` |  |
| 4 | **判断自然语言里是否还隐含了另一个方向，决定要不要写成双条件** | `Instead, biconditionals are often expressed using an “if, then” or an “only if” construction.` |  |

> ⚠️ **课件没交代的地方（讲解若补上，属补充解释而非课件内容）**：
> - 第 2 步「先按句子本意判断 or 是相容或还是排斥或，再选定对应的联结词」：教材只通过具体例句示范这种取舍（如 Example 9 用两个选择都要花掉全部积蓄来判定为排斥或），没有给出判断 or 是相容或还是排斥或的一般规则。

### `s11__form_converse_contrapositive_inverse` — 写出条件语句的逆命题、否命题和逆否命题

- **类型**：程序性
- **出处**：rosen-c1.1-pdf0032
- **前置**：s11__conditional_statement（条件语句（conditional statement / implication））、s11__converse_contrapositive_inverse（逆命题、否命题与逆否命题（converse, contrapositive, inverse））

**★ 子目标（4 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **先把原句改写成“如果……那么……”的标准条件句式** | `Because “q whenever p” is one of the ways to express the conditional statement p →q, the original statement can be rewritten as “If it is raining, then the home team wins.”` |  |
| 2 | **交换前件与后件，得到逆命题** | `The proposition q →p is called the converse of p →q.` |  |
| 3 | **对前件和后件分别取否，得到否命题；先交换再分别取否，得到逆否命题** | `The contrapositive of p →q is the proposition ¬q →¬p. The proposition ¬p →¬q is called the inverse of p →q.` |  |
| 4 | **需要做等价替换时只使用逆否命题，不要用逆命题或否命题替换原命题** | `Take note that one of the most common logical errors is to assume that the converse or the inverse of a conditional statement is equivalent to this conditional statement.` |  |

### `s11__apply_bitwise_operations` — 对两个位串做按位运算

- **类型**：程序性
- **出处**：rosen-c1.1-pdf0035、rosen-c1.1-pdf0036
- **前置**：s11__bit_string（位与位串（bit, Boolean variable, bit string））、s11__truth_table（真值表（truth table））

**★ 子目标（3 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **确认两个位串长度相同（按位运算只对等长位串定义）** | `bitwise XOR of two strings of the same length to be the strings that have as their bits the OR, AND, and XOR of the corresponding bits in the two strings, respectively.` |  |
| 2 | **逐位取出两个串对应位置上的位，分别按三种位运算规则求值** | `Solution: The bitwise OR, bitwise AND, and bitwise XOR of these strings are obtained by taking the OR, AND, and XOR of the corresponding bits, respectively.` |  |
| 3 | **把逐位得到的结果按原顺序拼成一个新的位串** | `01 1011 0110 11 0001 1101 11 1011 1111 bitwise OR` |  |

> ⚠️ **课件没交代的地方（讲解若补上，属补充解释而非课件内容）**：
> - 第 1 步「确认两个位串长度相同（按位运算只对等长位串定义）」：教材只定义了等长位串的按位运算，没有交代两个位串长度不同时该怎么办（例如是否要先补前导零）。

### `s12__logic_circuit` — 逻辑电路（logic circuit / digital circuit）

- **类型**：概念
- **出处**：rosen-c1.2-pdf0045
- **对比对象**：s12__logic_gate（逻辑门（gate）：反相器/非门、或门、与门）
- **易错点**：
    - 以为一个逻辑电路可以同时给出多个输出信号（本节只讨论单输出的逻辑电路，多输出是一般数字电路的情形）
    - 把逻辑电路的输入输出当成抽象命题真假值，忘了它们实际是比特 0（断开）或 1（接通）

### `s12__logic_gate` — 逻辑门（gate）：反相器/非门、或门、与门

- **类型**：概念
- **出处**：rosen-c1.2-pdf0045
- **上位**：s12__logic_circuit（逻辑电路（logic circuit / digital circuit））
- **对比对象**：s12__logic_circuit（逻辑电路（logic circuit / digital circuit））
- **易错点**：
    - 把或门理解成“两个输入只能有一个成立”（两个输入都为 1 时或门输出仍然是 1）
    - 把与门和或门的输出对调（与门输出两个输入的合取，或门输出两个输入的析取）
    - 以为反相器要用与门或或门搭出来，而它本身就是三种基本门之一

### `s12__boolean_search` — 布尔检索（Boolean search）

- **类型**：概念
- **出处**：rosen-c1.2-pdf0042、rosen-c1.2-pdf0043
- **易错点**：
    - 把 OR 当成“必须同时包含两个检索词”（OR 匹配含其中一个或两个的记录，要求同时包含的是 AND）
    - 忽略 AND 的优先级高于 OR，把 (NEW AND MEXICO OR ARIZONA) 误读成 NEW AND (MEXICO OR ARIZONA)
    - 以为检索词写得越多结果就越精确（教材指出结果里仍会混入无关页面，例如关于墨西哥的新大学的页面，需要再用 NOT 排除）

### `s12__system_specification` — 系统规格及其一致性（system specification, consistent）

- **类型**：概念
- **出处**：rosen-c1.2-pdf0041、rosen-c1.2-pdf0042
- **易错点**：
    - 只要每条规格单独看都能成立，就断定整套规格一致（一致性要求存在一个赋值让所有规格同时为真）
    - 认为往一致的规格集合里再加一条规格不会破坏一致性（加入“诊断消息没有被重传”后四条规格就变得不一致）

### `s12__logic_puzzle` — 逻辑谜题（logic puzzle）

- **类型**：概念
- **出处**：rosen-c1.2-pdf0043
- **易错点**：
    - 靠直觉逐句试猜答案，不为每个原子断言引入命题变元，也不检验哪种赋值能让全部陈述同时成立
    - 漏掉谜题里的数量条件（例如“只有一句是真的”），只逐句判断真假

### `s12__knights_and_knaves` — 骑士与无赖（knights and knaves）

- **类型**：概念
- **出处**：rosen-c1.2-pdf0044
- **上位**：s12__logic_puzzle（逻辑谜题（logic puzzle））
- **易错点**：
    - 把无赖的话当成“有时假有时真”（无赖说的每个陈述都为假，骑士说的每个陈述都为真）
    - 看到“某人说了某句话”就直接把这句话当成真的，忘了先判断说话者是骑士还是无赖

### `s12__translate_english_to_logic` — 把英语句子翻译成逻辑表达式

- **类型**：程序性
- **出处**：rosen-c1.2-pdf0040、rosen-c1.2-pdf0041
- **易错点**：
    - 把 only if 引出的部分当成充分条件，把条件句译成了相反的方向
    - 把 unless 当成又一个合取项直接接上去，而不是把它处理成前件中的否定
    - 为了省事把整句用一个命题变元表示（这样无法分析句子内部含义，也无法据此推理）

**★ 子目标（4 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **为句子的每个成分各指派一个命题变元** | `possible to represent the sentence by a single propositional variable, such as p, this would not be
useful when analyzing its meaning or reasoning with it. Instead, we will use propositional vari-
ables to represent each sentence part and determine the appropriate logical connectives between
them. In particular, we let a, c, and f represent “You can access the Internet from campus,” “You
are a computer science major,” and “You are a freshman,” respectively.` |  |
| 2 | **判断条件句哪个方向是充分条件（only if 引出的是必要条件那一边）** | `Noting that “only if” is
one way a conditional statement can be expressed, this sentence can be represented as
a →(c ∨¬f).` |  |
| 3 | **把 unless 处理成“若不满足例外条件”这一前提的否定** | `Let q, r, and s represent “You can ride the roller coaster,” “You are under 4 feet tall,”
and “You are older than 16 years old,” respectively. Then the sentence can be translated to
(r ∧¬s) →¬q.` |  |
| 4 | **按句子原意补上合理假设，并确认译法够用** | `Note that
this may involve making a set of reasonable assumptions based on the intended meaning of
the sentence.` |  |

> ⚠️ **课件没交代的地方（讲解若补上，属补充解释而非课件内容）**：
> - 第 3 步「把 unless 处理成“若不满足例外条件”这一前提的否定」：教材只直接给出了 (r ∧¬s) →¬q 这一译法，并说还可以有其他译法，没有说明为什么 unless 要处理成前件里那个被否定的条件。

### `s12__check_specification_consistency` — 判定系统规格是否一致

- **类型**：程序性
- **出处**：rosen-c1.2-pdf0041、rosen-c1.2-pdf0042
- **前置**：s12__translate_english_to_logic（把英语句子翻译成逻辑表达式）、s12__system_specification（系统规格及其一致性（system specification, consistent））
- **易错点**：
    - 只检查每条规格各自能不能被满足，不去找让全部规格同时为真的赋值
    - 找到一个满足赋值后就不再检查新加的规格是否与该赋值冲突

**★ 子目标（4 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **先把每条自然语言规格翻译成逻辑表达式** | `To determine whether these speciﬁcations are consistent, we ﬁrst express them using
logical expressions. Let p denote “The diagnostic message is stored in the buﬀer” and let q
denote “The diagnostic message is retransmitted.” The speciﬁcations can then be written as` |  |
| 2 | **逐条施加约束，找出让所有规格同时为真的赋值** | `An assignment of truth values that makes all three speciﬁcations true
must have p false to make ¬p true. Because we want p ∨q to be true but p must be false, q must
be true. Because p →q is true when p is false and q is true, we conclude that these speciﬁcations
are consistent, because they are all true when p is false and q is true.` |  |
| 3 | **用真值表穷举所有赋值作为备选判定手段** | `We could come to the same
conclusion by use of a truth table to examine the four possible assignments of truth values to p
and q.` |  |
| 4 | **新增规格后重新检查整体是否仍然可同时满足** | `By the reasoning in Example 4, the three speciﬁcations from that example are true
only in the case when p is false and q is true. However, this new speciﬁcation is ¬q, which is
false when q is true. Consequently, these four speciﬁcations are inconsistent.` |  |

### `s12__construct_boolean_search` — 构造布尔检索式

- **类型**：程序性
- **出处**：rosen-c1.2-pdf0042、rosen-c1.2-pdf0043
- **前置**：s12__boolean_search（布尔检索（Boolean search））
- **易错点**：
    - 把检索式按自然语言词序来读，忽略连接词本身的逻辑含义
    - 该同时出现的词用了 OR 连接，结果里混入大量无关页面

**★ 子目标（4 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **按 AND/OR/NOT 各自的匹配含义挑选连接词** | `In Boolean searches, the connective AND is used to match records that contain both of
two search terms, the connective OR is used to match one or both of two search terms, and the
connective NOT (sometimes written as AND NOT ) is used to exclude a particular search term.` |  |
| 2 | **用 OR 放宽匹配范围（命中其中一个或两个检索词）** | `Next, to ﬁnd pages that deal with universities in New Mexico or Arizona, we can search
for pages matching (NEW AND MEXICO OR ARIZONA) AND UNIVERSITIES.` |  |
| 3 | **用 NOT 排除会让结果混入无关页面的检索词** | `Finally, to ﬁnd
Web pages that deal with universities in Mexico (and not New Mexico), we might ﬁrst look
for pages matching MEXICO AND UNIVERSITIES, but because the results of this search will
include pages about universities in New Mexico, as well as universities in Mexico, it might be
better to search for pages matching (MEXICO AND UNIVERSITIES) NOT NEW. The results
of this search include pages that contain both the words MEXICO and UNIVERSITIES but
do not contain the word NEW.` |  |
| 4 | **把固定短语用引号锁成一个整体再与其他词连接** | `Most search engines support the use of quotation marks
to search for speciﬁc phrases. So, it may be more eﬀective to search for pages matching “NEW
MEXICO” AND UNIVERSITIES.` |  |

### `s12__solve_logic_puzzle_by_translation` — 把逻辑谜题翻译成逻辑表达式并求解

- **类型**：程序性
- **出处**：rosen-c1.2-pdf0043
- **前置**：s12__translate_english_to_logic（把英语句子翻译成逻辑表达式）、s12__logic_puzzle（逻辑谜题（logic puzzle））
- **易错点**：
    - 只把每句话各自译出来，漏掉“恰好一句为真”这类数量条件
    - 化简得出结论后不回原文核对哪句陈述为真、答案是否与全部题设相容

**★ 子目标（4 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **为每个原子断言引入命题变元，再把每句陈述写成它们的组合** | `Let pi be the proposition that the treasure is in Trunk i, for i = 1, 2, 3. To translate into
propositional logic the Queen’s statement that exactly one of the inscriptions is true, we observe
that the inscriptions on Trunk 1, Trunk 2, and Trunk 3, are ¬p1, ¬p2, and p2, respectively.` |  |
| 2 | **把“恰好一个成立”这类数量条件写成各情形的析取** | `So,
her statement can be translated to
(¬p1 ∧¬(¬p2) ∧¬p2) ∨(¬(¬p1) ∧¬p2 ∧¬p2) ∨(¬(¬p1) ∧¬(¬p2) ∧p2)).` |  |
| 3 | **用等价变形把条件化简，读出哪些情形被排除** | `Using the rules for propositional logic, we see that this is equivalent to (p1 ∧¬p2) ∨(p1 ∧p2). By
the distributive law, (p1 ∧¬p2) ∨(p1 ∧p2) is equivalent to p1 ∧(¬p2 ∨p2). But because ¬p2 ∨
p2 must be true, this is then equivalent to p1 ∧T, which is in turn equivalent to p1.` |  |
| 4 | **把结论代回原文，核对哪个陈述为真** | `So the treasure
is in Trunk 1 (that is, p1 is true), and p2 and p3 are false; and the inscription on Trunk 2 is the
only true one.` |  |

> ⚠️ **课件没交代的地方（讲解若补上，属补充解释而非课件内容）**：
> - 第 2 步「把“恰好一个成立”这类数量条件写成各情形的析取」：教材只演示了这一处“恰好一个为真”的翻译实例，没有给出 n 个陈述中恰好一个为真的一般写法（各情形合取式的析取）。

### `s12__solve_knights_and_knaves` — 求解骑士与无赖谜题

- **类型**：程序性
- **出处**：rosen-c1.2-pdf0043、rosen-c1.2-pdf0044
- **前置**：s12__knights_and_knaves（骑士与无赖（knights and knaves））、s12__solve_logic_puzzle_by_translation（把逻辑谜题翻译成逻辑表达式并求解）
- **易错点**：
    - 只试一种身份假设就下结论，不检验相反身份下是否也自洽
    - 发现某个假设与发言矛盾后就直接判定发言内容为假，而不去走完另一种身份假设

**★ 子目标（4 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **把每个人“是诚实者”设成命题变元，其身份决定发言的真假** | `Let p and q be the statements that A is a knight and B is a knight, respectively, so that
¬p and ¬q are the statements that A is a knave and B is a knave, respectively.` |  |
| 2 | **先假设某人属于诚实一方，把他的发言当真推出后果** | `We ﬁrst consider the possibility that A is a knight; this is the statement that p is true. If A is
a knight, then he is telling the truth when he says that B is a knight, so that q is true, and A and B
are the same type.` |  |
| 3 | **检验推出的后果与全部发言是否相容，不相容就否定该假设** | `would have to be true, which it is not, because A and
B are both knights. Consequently, we can conclude that A is not a knight, that is, that p is false.` |  |
| 4 | **改设相反身份再走一遍，两种身份都自洽才下结论** | `If A is a knave, then because everything a knave says is false, A’s statement that B is
a knight, that is, that q is true, is a lie. This means that q is false and B is also a knave.
Furthermore, if B is a knave, then B’s statement that A and B are opposite types is a lie,
which is consistent with both A and B being knaves. We can conclude that both A and B are
knaves.` |  |

> ⚠️ **课件没交代的地方（讲解若补上，属补充解释而非课件内容）**：
> - 第 4 步「改设相反身份再走一遍，两种身份都自洽才下结论」：教材按“先假设某人是骑士、再假设他是无赖”演示了一遍，没有说明为什么必须把两种身份都试过才能下结论。

### `s12__trace_circuit_output` — 由电路求输出：逐门追踪

- **类型**：程序性
- **出处**：rosen-c1.2-pdf0045
- **前置**：s12__logic_circuit（逻辑电路（logic circuit / digital circuit））、s12__logic_gate（逻辑门（gate）：反相器/非门、或门、与门）
- **易错点**：
    - 从输出端往回猜结果，而不是从输入侧按门的先后顺序逐个算出中间输出
    - 把某个门的输出重复接到它并没有连接的门上，凭公式形状而不是连线来读电路

**★ 子目标（2 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **从输入侧出发沿连线逐个门向前追踪** | `Given a circuit built from the basic logic gates and the inputs to the circuit, we determine
the output by tracing through the circuit, as Example 10 shows.` |  |
| 2 | **把每个门的输出写成由已求出的信号构成的表达式，供下游门使用** | `In Figure 2 we display the output of each logic gate in the circuit. We see that the
AND gate takes input of p and ¬q, the output of the inverter with input q, and produces p ∧
¬q. Next, we note that the OR gate takes input p ∧¬q and ¬r, the output of the inverter with
input r, and produces the ﬁnal output (p ∧¬q) ∨¬r.` |  |

### `s12__build_circuit_from_formula` — 由逻辑公式搭建数字电路

- **类型**：程序性
- **出处**：rosen-c1.2-pdf0046
- **前置**：s12__logic_gate（逻辑门（gate）：反相器/非门、或门、与门）、s12__trace_circuit_output（由电路求输出：逐门追踪）
- **易错点**：
    - 需要变元的否定时直接把变元本身接进门，忘了先用反相器取出否定
    - 想用一个门把整个公式一次接完，而不是按子公式逐层搭建

**★ 子目标（4 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **按顶层连接词把公式拆成子公式，分别搭建后再用顶层门合并** | `To construct the desired circuit, we build separate circuits for p ∨¬r and for ¬p ∨(q ∨
¬r) and combine them using an AND gate.` |  |
| 2 | **用反相器从输入变元取出需要的否定信号** | `To construct a circuit for p ∨¬r, we use an inverter
to produce ¬r from the input r.` |  |
| 3 | **由最内层子公式往外，逐层用或门、与门接出中间表达式** | `for ¬p ∨(q ∨¬r), we ﬁrst use an inverter to obtain ¬r. Then we use an OR gate with inputs q
and ¬r to obtain q ∨¬r. Finally, we use another inverter and an OR gate to get ¬p ∨(q ∨¬r)
from the inputs p and q ∨¬r.` |  |
| 4 | **最后用顶层连接词对应的门把各子电路接起来** | `To complete the construction, we employ a ﬁnal AND gate, with inputs p ∨¬r and ¬p ∨
(q ∨¬r). The resulting circuit is displayed in Figure 3.` |  |

### `s13__tautology_and_contradiction` — 永真式、矛盾式与偶然式

- **类型**：概念
- **出处**：rosen-c1.3-pdf0050、rosen-c1.3-pdf0053、rosen-c1.3-pdf0056
- **对比对象**：s13__satisfiability（可满足性与不可满足性（satisfiability））
- **易错点**：
    - 把「可满足」当成「永真式」：只要找到一组赋值使命题为真，就说它是永真式
    - 把偶然式（有的赋值真、有的赋值假）说成永真式或矛盾式
    - 把永真式排除在可满足之外（永真式也满足「存在一组赋值使命题为真」）
    - 记反否定关系：矛盾式的否定是永真式，永真式的否定是矛盾式

### `s13__logical_equivalence` — 逻辑等价（logically equivalent）

- **类型**：概念
- **出处**：rosen-c1.3-pdf0050、rosen-c1.3-pdf0051、rosen-c1.3-pdf0054
- **前置**：s13__tautology_and_contradiction（永真式、矛盾式与偶然式）
- **对比对象**：s13__biconditional_equivalences（双条件语句的等价式（Table 8））
- **易错点**：
    - 把两式逻辑等价当成一个复合命题，拿它去和别的式子做真值运算（它其实是「对应的双条件式是永真式」这一断言）
    - 把表示逻辑等价的符号当成 ∧、∨ 那样的逻辑联结词
    - 把逻辑等价理解成两个式子写法相同或可以互相「代入字母」
    - 把原文里表示逻辑等价的符号 ⇔ 与双条件联结词 ↔ 当成同一个符号

### `s13__conditional_disjunction_equivalence` — 条件-析取等价（conditional-disjunction equivalence）

- **类型**：概念
- **出处**：rosen-c1.3-pdf0051、rosen-c1.3-pdf0052、rosen-c1.3-pdf0054
- **前置**：s13__logical_equivalence（逻辑等价（logically equivalent））
- **对比对象**：s13__conditional_equivalences（条件语句的等价式（Table 7））
- **易错点**：
    - 把条件式改写成析取式时把否定加到后件上（写成「后件的否定或前件」）
    - 把前件与后件一起否定，得到「非前件或非后件」
    - 把条件-析取等价与它的逆否形式当成同一个式子
    - 以为改写后仍含有条件联结词

### `s13__conditional_equivalences` — 条件语句的等价式（Table 7）

- **类型**：概念
- **出处**：rosen-c1.3-pdf0052、rosen-c1.3-pdf0054
- **前置**：s13__conditional_disjunction_equivalence（条件-析取等价（conditional-disjunction equivalence））
- **对比对象**：s13__de_morgan_laws（德摩根律（De Morgan's laws））
- **易错点**：
    - 把逆命题（交换前件后件）或否命题（前件后件都取否定）当成与原条件式等价，只有逆否命题才等价
    - 把「条件式的否定」展开成「非前件蕴含非后件」或「前件蕴含非后件」（正确结果是「前件真而后件假」）
    - 把两个条件式的合取与「后件的合取作为结论」这一条写反，前件后件位置对调
    - 对条件式直接套用结合律、分配律或德摩根律来「拆括号」

### `s13__biconditional_equivalences` — 双条件语句的等价式（Table 8）

- **类型**：概念
- **出处**：rosen-c1.3-pdf0052、rosen-c1.3-pdf0054
- **前置**：s13__conditional_equivalences（条件语句的等价式（Table 7））
- **对比对象**：s13__logical_equivalence（逻辑等价（logically equivalent））
- **易错点**：
    - 把双条件式的否定写成「两个变元否定的双条件式」（Table 8 里等价的是原双条件式与「双否定后的双条件式」，否定式对应的是「其中一个变元取否定」的形式）
    - 把双条件式展开成两个条件式的析取，而不是合取
    - 把双条件联结词与表示逻辑等价的符号当成同一个符号

### `s13__de_morgan_laws` — 德摩根律（De Morgan's laws）

- **类型**：概念
- **出处**：rosen-c1.3-pdf0050、rosen-c1.3-pdf0052、rosen-c1.3-pdf0053
- **前置**：s13__logical_equivalence（逻辑等价（logically equivalent））
- **对比对象**：s13__basic_logical_identities（基本逻辑等价律（Table 6））
- **易错点**：
    - 取否定后忘记把联结词换成相反的：把「合取的否定」写成「各成分否定的合取」
    - 只否定其中一个成分，例如把「析取的否定」写成「一个成分否定后仍用析取联结」
    - 把两条律的方向用反：否定合取应该得到各成分否定的析取
    - 把德摩根律用在条件式或双条件式上，当作可以直接「把否定推进去」

### `s13__basic_logical_identities` — 基本逻辑等价律（Table 6）

- **类型**：概念
- **出处**：rosen-c1.3-pdf0052、rosen-c1.3-pdf0053
- **前置**：s13__logical_equivalence（逻辑等价（logically equivalent））
- **对比对象**：s13__conditional_equivalences（条件语句的等价式（Table 7））
- **易错点**：
    - 把结合律、分配律或德摩根律用在合取与析取混合出现的表达式上（这些律只在所有运算符都相同时才适用）
    - 把两个分配律的方向写错：析取分配到合取、合取分配到析取得到的展开式不同
    - 把同一律与支配律记混（与恒真常元合取保持原式，与恒真常元析取得到恒真常元）
    - 以为多个同种联结词串起来时结合顺序会改变真值，因而不承认可以不写括号

### `s13__satisfiability` — 可满足性与不可满足性（satisfiability）

- **类型**：概念
- **出处**：rosen-c1.3-pdf0056、rosen-c1.3-pdf0060
- **前置**：s13__tautology_and_contradiction（永真式、矛盾式与偶然式）
- **对比对象**：s13__tautology_and_contradiction（永真式、矛盾式与偶然式）
- **易错点**：
    - 找到一组使其为真的赋值后，就宣称它是永真式（可满足不等于永真）
    - 为证明不可满足只验证了几组赋值都为假，没有覆盖全部赋值
    - 把「原式不可满足」与「原式的否定不可满足」混淆（原式不可满足等价于其否定是永真式）
    - 认为永真式不算可满足

### `s13__dual` — 对偶式（dual）

- **类型**：概念
- **出处**：rosen-c1.3-pdf0062
- **前置**：s13__basic_logical_identities（基本逻辑等价律（Table 6））
- **对比对象**：s13__de_morgan_laws（德摩根律（De Morgan's laws））
- **易错点**：
    - 把对偶式当成否定式：求对偶只交换合取与析取、交换两个常元，不加否定号
    - 对含条件联结词或双条件联结词的式子也照搬交换合取与析取（定义只覆盖只含析取、合取、否定的命题）
    - 以为求两次对偶得到的是否定式，而不是原式

### `s13__functionally_complete` — 功能完备的联结词集合（functionally complete）

- **类型**：概念
- **出处**：rosen-c1.3-pdf0062、rosen-c1.3-pdf0063
- **前置**：s13__logical_equivalence（逻辑等价（logically equivalent））
- **对比对象**：s13__logical_equivalence（逻辑等价（logically equivalent））
- **易错点**：
    - 以为功能完备要求两个复合命题写法完全相同，而不是逻辑等价即可
    - 以为只有「否定、合取、析取」这一组是完备的，忽略只用否定加合取、只用否定加析取、只用 NOR、只用 NAND 也完备
    - 把 NAND 与 NOR 记反（NAND 只在两个成分都为真时为假，NOR 只在两个成分都为假时为真）
    - 以为 NAND 可以结合，把两种不同加括号方式得到的式子当成等价

### `s13__equivalence_by_truth_table` — 用真值表判定两个复合命题是否逻辑等价

- **类型**：程序性
- **出处**：rosen-c1.3-pdf0050、rosen-c1.3-pdf0051、rosen-c1.3-pdf0053
- **前置**：s13__logical_equivalence（逻辑等价（logically equivalent））、s13__tautology_and_contradiction（永真式、矛盾式与偶然式）
- **易错点**：
    - 只比较了部分行就下结论，没有覆盖全部取值组合
    - 把两个待比较的式子算在同一列里，导致无法逐列对照
    - 变元个数为 n 时行数算少（应为 2 的 n 次方行）
    - 把两式真值列恰好相同的若干行当成「处处一致」

**★ 子目标（5 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **把「两式是否逻辑等价」改判为「对应的双条件式是否永真」** | `The compound propositions p and q are called logically equivalent if p ↔q is a tautology.` |  |
| 2 | **并排算出两式的真值列，逐行比较两列是否处处一致** | `One way to determine whether two compound propositions are equivalent is to use a truth table. In particular, the compound propositions p and q are equivalent if and only if the columns giving their truth values agree.` |  |
| 3 | **按固定顺序枚举所有真值组合，避免漏行或重复行** | `These eight combinations of truth values are TTT, TTF, TFT, TFF, FTT, FTF, FFT, and FFF; we use this order when we display the rows of the truth table.` |  |
| 4 | **按变元个数确定表的规模（每多一个变元，取值组合数翻倍）** | `In general, 2n rows are required if a compound proposition involves n propositional variables.` |  |
| 5 | **变元太多使真值表不可行时，改用已知的等价律来推导** | `Because of the rapid growth of 2n, more eﬃcient ways are needed to establish logical equivalences, such as by using ones we already know.` |  |

### `s13__negation_by_de_morgan` — 用德摩根律求复合命题（含自然语言陈述）的否定

- **类型**：程序性
- **出处**：rosen-c1.3-pdf0050、rosen-c1.3-pdf0052、rosen-c1.3-pdf0053
- **前置**：s13__de_morgan_laws（德摩根律（De Morgan's laws））
- **易错点**：
    - 取否定后没有把联结词换成相反的，直接把否定号「分配」进去
    - 自然语言陈述没有先符号化就凭语感改写，导致析取/合取判断错
    - 否定的结果仍然带着原来的联结词，或只否定了其中一个成分
    - 把适用于两个成分的律直接推广时漏掉某些项的否定

**★ 子目标（5 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **先看否定作用在合取还是析取上，据此决定否定后改用哪种联结词** | `In particular, the equivalence ¬(p ∨q) ≡¬p ∧¬q tells us that the negation of a disjunction is formed by taking the conjunction of the negations of the component propositions.` |  |
| 2 | **把否定分别加到每个成分上，并把联结词换成相反的** | `Similarly, the equivalence ¬(p ∧q) ≡¬p ∨¬q tells us that the negation of a conjunction is formed by taking the disjunction of the negations of the component propositions.` |  |
| 3 | **取完否定务必改变联结词，否则写出的是不等价的式子** | `When using De Morgan’s laws, remember to change the logical connective after you negate.` |  |
| 4 | **自然语言陈述先符号化再套律，最后把结果译回自然语言** | `Let r be “Heather will go to the concert” and s be “Steve will go to the concert.” Then “Heather will go to the concert or Steve will go to the concert” can be represented by r ∨s. By the second of De Morgan’s laws, ¬(r ∨s) is equivalent to ¬r ∧¬s.` |  |
| 5 | **把两条律推广到任意有限多项的合取或析取** | `Furthermore, note that De Morgan’s laws extend to ¬(p1 ∨p2 ∨⋯∨pn) ≡(¬p1 ∧¬p2 ∧⋯∧¬pn)` |  |

> ⚠️ **课件没交代的地方（讲解若补上，属补充解释而非课件内容）**：
> - 第 5 步「把两条律推广到任意有限多项的合取或析取」：教材只给出推广形式并说明证明方法放在 5.1 节，本节没有说明该推广为什么不依赖项数的具体取值。

### `s13__derive_equivalence_chain` — 用已知等价律把待证式逐步化归，构造新的逻辑等价

- **类型**：程序性
- **出处**：rosen-c1.3-pdf0054、rosen-c1.3-pdf0055
- **前置**：s13__logical_equivalence（逻辑等价（logically equivalent））、s13__basic_logical_identities（基本逻辑等价律（Table 6））
- **易错点**：
    - 一步里同时用好几条等价式改写多处，出错后无法定位
    - 把待证结论当作已知条件使用（用结论去替换式子）
    - 改写时只变换了一边而另一边保持原样，最后两侧不同却宣布等价
    - 证永真式时化归到某个偶然式就停下，没有化成恒真常元

**★ 子目标（4 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **利用「子式可替换为等价式而不改变整体真值」这一原理** | `The reason for this is that a proposition in a compound proposition can be replaced by a compound proposition that is logically equivalent to it without changing the truth value of the original compound proposition.` |  |
| 2 | **每一步只套用一条已知等价式，并注明这一步的依据** | `So, we will establish this equivalence by developing a series of logical equivalences, using one of the equivalences in Table 6 at a time, starting with ¬(p →q) and ending with p ∧¬q.` |  |
| 3 | **要证某式为永真式时，用等价变形把它化归为恒真的常元** | `To show that this statement is a tautology, we will use logical equivalences to demon-strate that it is logically equivalent to T.` |  |
| 4 | **借助等价的传递性把多步变形串成一条链** | `This technique is illustrated in Examples 6–8, where we also use the fact that if p and q are logically equivalent and q and r are logically equivalent, then p and r are logically equivalent (see Exercise 60).` |  |

### `s13__decide_satisfiability` — 判定一个复合命题是否可满足（不依赖真值表的推理与工具方法）

- **类型**：程序性
- **出处**：rosen-c1.3-pdf0056、rosen-c1.3-pdf0060
- **前置**：s13__satisfiability（可满足性与不可满足性（satisfiability））
- **易错点**：
    - 用几组赋值试不出真就宣布不可满足
    - 把「否定式恒真」当作「原式恒真」
    - 只对合取式中的一部分子句做了推理，漏掉其余子句的约束
    - 变元稍多仍坚持手算真值表，忽略指数级增长

**★ 子目标（6 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **按定义区分「存在一组赋值使其为真」与「对所有赋值都为假」** | `A compound proposition is satisﬁable if there is an assignment of truth values to its variables that makes it true (that is, when it is a tautology or a contingency). When no such assignments exists, that is, when the compound proposition is false for all assignments of truth values to its variables, the compound proposition is unsatisﬁable.` |  |
| 2 | **通过判断否定式是否恒真来间接判定可满足性** | `Note that a compound proposition is unsatisﬁable if and only if its negation is true for all assignments of truth values to the variables, that is, if and only if its negation is a tautology.` |  |
| 3 | **证明可满足只需给出一组使其为真的赋值，并把它作为该问题的解** | `When we ﬁnd a particular assignment of truth values that makes a compound proposition true, we have shown that it is satisﬁable; such an assignment is called a solution of this particular satisﬁability problem.` |  |
| 4 | **证明不可满足必须覆盖所有赋值，不能只举几组为假的例子** | `However, to show that a compound proposition is unsatisﬁable, we need to show that every assignment of truth values to its variables makes it false.` |  |
| 5 | **把整体为真的要求拆成各部分同时为真，再看这些条件能否同时成立** | `Finally, note that for (p ∨¬q) ∧(q ∨¬r) ∧(r ∨¬p) ∧(p ∨q ∨r) ∧(¬p ∨¬q ∨¬r) to be true, (p ∨¬q) ∧(q ∨¬r) ∧(r ∨¬p) and (p ∨q ∨r) ∧(¬p ∨¬q ∨¬r) must both be true.` |  |
| 6 | **变元很多时放弃真值表，改用计算机求解程序** | `A truth table can be used to determine whether a compound proposition is satisﬁable, or equivalently, whether its negation is a tautology (see Exercise 64). This can be done by hand for a compound proposition with a small number of variables, but when the number of variables grows, this becomes impractical.` |  |

> ⚠️ **课件没交代的地方（讲解若补上，属补充解释而非课件内容）**：
> - 第 6 步「变元很多时放弃真值表，改用计算机求解程序」：教材只说明已有实用的可满足性求解程序、并指出相关算法在第 3 章讨论，本节没有给出可以照做的求解步骤。

### `s13__model_as_satisfiability` — 把约束型实际问题编码成可满足性问题并求解

- **类型**：程序性
- **出处**：rosen-c1.3-pdf0056、rosen-c1.3-pdf0057、rosen-c1.3-pdf0058、rosen-c1.3-pdf0059、rosen-c1.3-pdf0060
- **前置**：s13__satisfiability（可满足性与不可满足性（satisfiability））
- **易错点**：
    - 变元含义设计含糊，导致同一个变元被用来表示两件事
    - 只写了「至少一个」类断言，漏掉「至多一个」类断言，得到的解不满足题目约束
    - 把「至多一个」写成「所有候选都为假」，把该出现的那个也排除了
    - 取合取时漏掉某条约束，或把几条断言用析取连起来
    - 按块遍历时把下标设错，导致某些格子被漏掉或被重复断言

**★ 子目标（6 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **为「某个对象取某个值」这类断言各设一个命题变元** | `To model the n-queens problem as a satisﬁability problem, we introduce n2 variables, p(i, j) for i = 1, 2, … , n and j = 1, 2, … , n.` |  |
| 2 | **先把题目已给定的取值编码成断言** | `Given a particular Sudoku puzzle, we begin by encoding each of the given values.` |  |
| 3 | **把每条约束拆成「至少一个」与「至多一个」两类断言** | `We can show that there is one queen in each row by verifying that every row contains at least one queen and that every row contains at most one queen.` |  |
| 4 | **「至多一个」用「不能同时为真」的析取式表达** | `Observe that ¬p(i, j) ∨¬p(i, k) asserts that at least one of ¬p(i, j) and ¬p(i, k) is true, which means that at least one of p(i, j) and p(i, k) is false.` |  |
| 5 | **把所有断言取合取得到总公式，解就是使它为真的那组赋值** | `Putting all this together, we ﬁnd that the solutions of the n-queens problem are given by the assignments of truth values to the variables p(i, j), i = 1, 2, … , n and j = 1, 2, … , n that make Q = Q1 ∧Q2 ∧Q3 ∧Q4 ∧Q5 true.` |  |
| 6 | **对每条约束先写「某个位置含有某个值」，再对所有取值、所有位置逐层加合取或析取** | `We now explain how to construct the assertion that every row contains every number. First, to assert that row i contains the number n, we form ⋁9 j=1 p(i, j, n). To assert that row i contains all n numbers, we form the conjunction of these disjunctions over all nine possible values of n, giving us ⋀9 n=1 ⋁9 j=1 p(i, j, n).` |  |

### `s14__propositional_function` — 命题函数与谓词（propositional function / predicate）

- **类型**：概念
- **出处**：rosen-c1.4-pdf0064、rosen-c1.4-pdf0065
- **对比对象**：s14__domain_of_discourse（论域（domain of discourse））
- **易错点**：
    - 把带自由变量的命题函数当成命题，说它有确定的真值
    - 把“x is greater than 3”的主语 x 当成谓词（谓词是“is greater than 3”）
    - 把谓词本身当成完整命题，忘了它必须配上主语/变量赋值才有真值
    - 只给多变量谓词中的一部分变量赋值，就认为已经得到命题
    - 把 n 元谓词的实参顺序写错，认为 P(a, b) 与 P(b, a) 是一回事

### `s14__universal_quantifier` — 全称量化（universal quantification，∀）

- **类型**：概念
- **出处**：rosen-c1.4-pdf0067
- **前置**：s14__propositional_function（命题函数与谓词（propositional function / predicate））、s14__domain_of_discourse（论域（domain of discourse））
- **对比对象**：s14__existential_quantifier（存在量化（existential quantification，∃））
- **易错点**：
    - 写 ∀xP(x) 却不交代论域，以为全称量化的真假与论域无关
    - 把“for any x”当成无歧义的“for all”（教材明说 any 常歧义）
    - 以为 ∀ 可以像分配律一样分配到析取上，写出 ∀x(P(x) ∨Q(x)) ≡∀xP(x) ∨∀xQ(x)

### `s14__existential_quantifier` — 存在量化（existential quantification，∃）

- **类型**：概念
- **出处**：rosen-c1.4-pdf0068、rosen-c1.4-pdf0069
- **前置**：s14__propositional_function（命题函数与谓词（propositional function / predicate））、s14__domain_of_discourse（论域（domain of discourse））
- **对比对象**：s14__universal_quantifier（全称量化（universal quantification，∀））
- **易错点**：
    - 不交代论域就使用 ∃xP(x)，把它当成有确定真值的命题
    - 把“Some student in this class has visited Mexico”写成 ∃x(S(x) →M(x))，而不是用 ∧ 连接

### `s14__uniqueness_quantifier` — 唯一性量词（uniqueness quantifier，∃!）

- **类型**：概念
- **出处**：rosen-c1.4-pdf0069
- **前置**：s14__existential_quantifier（存在量化（existential quantification，∃））、s14__universal_quantifier（全称量化（universal quantification，∀））
- **对比对象**：s14__existential_quantifier（存在量化（existential quantification，∃））
- **易错点**：
    - 把 ∃!xP(x) 当成 ∃xP(x) 的弱化形式（其实它是更强的断言）
    - 以为 ∃!xP(x) 也保证 ∀xP(x) 成立
    - 以为必须用 ∃! 才能表达唯一性（教材说用 ∃ 和 ∀ 就能表达，而且更便于用推理规则）

### `s14__counterexample` — 量词化命题的真值判据与反例（counterexample）

- **类型**：概念
- **出处**：rosen-c1.4-pdf0067、rosen-c1.4-pdf0068
- **前置**：s14__universal_quantifier（全称量化（universal quantification，∀））、s14__existential_quantifier（存在量化（existential quantification，∃））
- **对比对象**：s14__universal_quantifier（全称量化（universal quantification，∀））
- **易错点**：
    - 为了说明 ∃xP(x) 为真去找反例（反例只能驳 ∀）
    - 举出多个反例才敢断定 ∀xP(x) 为假（其实一个就够）
    - 用反例去反驳存在量化命题 ∃xP(x)
    - 举的反例不在当前论域内，例如论域是整数却拿分数去反驳 ∀x(x2 ≥x)

### `s14__domain_of_discourse` — 论域（domain of discourse）

- **类型**：概念
- **出处**：rosen-c1.4-pdf0067、rosen-c1.4-pdf0069
- **前置**：s14__propositional_function（命题函数与谓词（propositional function / predicate））
- **对比对象**：s14__counterexample（量词化命题的真值判据与反例（counterexample））
- **易错点**：
    - 换了论域却以为量词化命题的真值不变
    - 以为论域可以是空的（教材默认论域非空），并据此乱套空论域下的真值

### `s14__finite_domain_expansion` — 有限论域下量词的合取/析取展开

- **类型**：概念
- **出处**：rosen-c1.4-pdf0070
- **前置**：s14__universal_quantifier（全称量化（universal quantification，∀））、s14__existential_quantifier（存在量化（existential quantification，∃））
- **对比对象**：s14__compute_truth_value_by_looping（用循环/搜索判定量词化命题的真值）
- **易错点**：
    - 对无穷论域也照搬这种展开写法
    - 把 ∃ 展开成合取、把 ∀ 展开成析取（两者恰好相反）
    - 以为展开时少列一个元素不影响真值

### `s14__bounded_and_free_variables` — 约束变量、自由变量与量词辖域

- **类型**：概念
- **出处**：rosen-c1.4-pdf0071、rosen-c1.4-pdf0072
- **前置**：s14__universal_quantifier（全称量化（universal quantification，∀））、s14__existential_quantifier（存在量化（existential quantification，∃））
- **对比对象**：s14__propositional_function（命题函数与谓词（propositional function / predicate））
- **易错点**：
    - 把含自由变量的式子当成命题，认为它已经有真值
    - 看不清辖域，把 ∃x(P(x) ∧Q(x)) ∨∀xR(x) 中两个量词的作用范围弄混
    - 以为辖域不重叠时也必须给两个量词换用不同字母（教材说可以重名）

### `s14__logical_equivalence_involving_quantifiers` — 含量词的逻辑等价

- **类型**：概念
- **出处**：rosen-c1.4-pdf0072
- **前置**：s14__universal_quantifier（全称量化（universal quantification，∀））、s14__existential_quantifier（存在量化（existential quantification，∃））
- **对比对象**：s14__de_morgan_laws_for_quantifiers（量词的德摩根律（量词否定的等价式））
- **易错点**：
    - 只在某一个具体论域下验证真值相同，就宣称两个量化命题逻辑等价
    - 把 ∀ 分配到析取、把 ∃ 分配到合取，当成普遍成立的等价式

### `s14__de_morgan_laws_for_quantifiers` — 量词的德摩根律（量词否定的等价式）

- **类型**：概念
- **出处**：rosen-c1.4-pdf0073、rosen-c1.4-pdf0074
- **前置**：s14__universal_quantifier（全称量化（universal quantification，∀））、s14__existential_quantifier（存在量化（existential quantification，∃））、s14__logical_equivalence_involving_quantifiers（含量词的逻辑等价）
- **对比对象**：s14__logical_equivalence_involving_quantifiers（含量词的逻辑等价）
- **易错点**：
    - 否定时只把 ¬ 写进括号里而不换量词，写出 ¬∀xP(x) ≡∀x¬P(x)
    - 把 ¬∀xP(x) ≡∃x¬P(x) 记成 ¬∀xP(x) ≡∃xP(x)
    - 把 ¬∃xP(x) ≡∀x¬P(x) 与 ¬∀xP(x) ≡∃x¬P(x) 两条律互相记反

### `s14__compute_truth_value_by_looping` — 用循环/搜索判定量词化命题的真值

- **类型**：程序性
- **出处**：rosen-c1.4-pdf0070
- **前置**：s14__universal_quantifier（全称量化（universal quantification，∀））、s14__existential_quantifier（存在量化（existential quantification，∃））、s14__counterexample（量词化命题的真值判据与反例（counterexample））
- **对比对象**：s14__finite_domain_expansion（有限论域下量词的合取/析取展开）
- **易错点**：
    - 对无穷论域也声称已经用这种枚举法判定了真值
    - 判断全称命题时只抽查几个元素为真就宣布它为真

**★ 子目标（6 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **把论域中的 n 个对象逐个代入，检查该性质是否在每一个对象上都成立** | `Suppose that there are n objects in the domain for the variable x. To determine whether ∀xP(x) is true, we can loop through all n values of x to see whether P(x) is always true. If we encounter` |  |
| 2 | **一旦遇到使性质为假的对象，立即判该全称命题为假** | `is true, we can loop through all n values of x to see whether P(x) is always true. If we encounter a value x for which P(x) is false, then we have shown that ∀xP(x) is false. Otherwise, ∀xP(x)` |  |
| 3 | **若始终没有遇到反例，则判该全称命题为真** | `a value x for which P(x) is false, then we have shown that ∀xP(x) is false. Otherwise, ∀xP(x) is true. To see whether ∃xP(x) is true, we loop through the n values of x searching for a value` |  |
| 4 | **对存在命题改为搜索，找到一个使性质成立的对象即可判真** | `is true. To see whether ∃xP(x) is true, we loop through the n values of x searching for a value for which P(x) is true. If we ﬁnd one, then ∃xP(x) is true. If we never ﬁnd such an x, then we` |  |
| 5 | **搜索完整个论域仍未找到，才判该存在命题为假** | `for which P(x) is true. If we ﬁnd one, then ∃xP(x) is true. If we never ﬁnd such an x, then we have determined that ∃xP(x) is false. (Note that this searching procedure does not apply if there` |  |
| 6 | **确认论域是否有限：无限论域不能真的枚举，只能把这种方法当思考方式** | `have determined that ∃xP(x) is false. (Note that this searching procedure does not apply if there are inﬁnitely many values in the domain. However, it is still a useful way of thinking about the truth values of quantiﬁcations.)` |  |

### `s14__evaluate_quantifier_over_listed_domain` — 把量词化命题改写成合取/析取后求值

- **类型**：程序性
- **出处**：rosen-c1.4-pdf0070
- **前置**：s14__finite_domain_expansion（有限论域下量词的合取/析取展开）、s14__propositional_function（命题函数与谓词（propositional function / predicate））
- **对比对象**：s14__compute_truth_value_by_looping（用循环/搜索判定量词化命题的真值）
- **易错点**：
    - 论域是 {1, 2, 3, 4} 却漏写或多写某一项
    - 代入时把幂写错（例如把 42 当成四十二而不是 4 的平方）
    - 以为要所有项都算成真才算全称命题真，忘了只要有一项为假整个合取即为假

**★ 子目标（5 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **确认论域有限且元素能一一列出，据元素个数定出要展开的项数** | `When the domain of a quantiﬁer is ﬁnite, that is, when all its elements can be listed, quantiﬁed statements can be expressed using propositional logic. In particular, when the elements of the domain are x1, x2, …, xn, where n is a positive integer, the universal quantiﬁcation ∀xP(x) is the same as the conjunction P(x1) ∧P(x2) ∧⋯∧P(xn), because this conjunction is true if and only if P(x1), P(x2), … , P(xn) are all true.` |  |
| 2 | **把全称量化改写成对论域每个元素的合取式** | `domain are x1, x2, …, xn, where n is a positive integer, the universal quantiﬁcation ∀xP(x) is the same as the conjunction` |  |
| 3 | **把存在量化改写成对论域每个元素的析取式** | `Similarly, when the elements of the domain are x1, x2, … , xn, where n is a positive integer, the existential quantiﬁcation ∃xP(x) is the same as the disjunction P(x1) ∨P(x2) ∨⋯∨P(xn), because this disjunction is true if and only if at least one of P(x1), P(x2), … , P(xn) is true.` |  |
| 4 | **逐项代入求值：合取式里只要有一项为假，全称命题就是假** | `because the domain consists of the integers 1, 2, 3, and 4. Because P(4), which is the statement “42 < 10,” is false, it follows that ∀xP(x) is false. ◂` |  |
| 5 | **析取式里只要有一项为真，存在命题就是真** | `Solution: Because the domain is {1, 2, 3, 4}, the proposition ∃xP(x) is the same as the disjunction P(1) ∨P(2) ∨P(3) ∨P(4). Because P(4), which is the statement “42 > 10,” is true, it follows that ∃xP(x) is true.` |  |

### `s14__negate_quantified_statement` — 否定量词化命题（把否定推进量词内部）

- **类型**：程序性
- **出处**：rosen-c1.4-pdf0073、rosen-c1.4-pdf0074
- **前置**：s14__de_morgan_laws_for_quantifiers（量词的德摩根律（量词否定的等价式））、s14__logical_equivalence_involving_quantifiers（含量词的逻辑等价）
- **对比对象**：s14__translate_english_to_quantified_expression（把英文语句翻译成带量词的逻辑表达式）
- **易错点**：
    - 只把 ¬ 搬进括号、不把 ∀ 换成 ∃（或反过来）
    - 否定后仍用“All ... are not ...”这类有歧义的英文表述，而不是改成“存在一个…不…”

**★ 子目标（5 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **按量词否定律把 ¬ 推过量词：全称换成存在、存在换成全称** | `This example illustrates the following logical equivalence: ¬∀xP(x) ≡∃x ¬P(x).` |  |
| 2 | **量词换过之后，把否定加到原谓词上** | `∀x ¬Q(x). This example illustrates the equivalence ¬∃xQ(x) ≡∀x ¬Q(x).` |  |
| 3 | **把 ¬(P(x) →Q(x)) 这类内层式子按命题逻辑等价式化简成合取形式** | `Solution: By De Morgan’s law for universal quantiﬁers, we know that ¬∀x(P(x) →Q(x)) and ∃x(¬(P(x) →Q(x))) are logically equivalent. By the ﬁfth logical equivalence in Table 7 in Sec- tion 1.3, we know that ¬(P(x) →Q(x)) and P(x) ∧¬Q(x) are logically equivalent for every x.` |  |
| 4 | **消去谓词前的否定符号，改写成相反的谓词或关系（如把 x2 > x 写成 x2 ≤x）** | `Solution: The negation of ∀x(x2 > x) is the statement ¬∀x(x2 > x), which is equivalent to ∃x¬(x2 > x). This can be rewritten as ∃x(x2 ≤x). The negation of ∃x(x2 = 2) is the statement ¬∃x(x2 = 2), which is equivalent to ∀x¬(x2 = 2). This can be rewritten as ∀x(x2 ≠2). The truth` |  |
| 5 | **改用不含歧义的英文把否定说出来，不写“All ... are not ...”** | `is ¬∃xH(x), which is equivalent to ∀x¬H(x). This negation can be expressed as “Every politician is dishonest.” (Note: In English, the statement “All politicians are not honest” is ambiguous. In common usage, this statement often means “Not all politicians are honest.” Consequently, we do not use this statement to express this negation.)` |  |

### `s14__translate_english_to_quantified_expression` — 把英文语句翻译成带量词的逻辑表达式

- **类型**：程序性
- **出处**：rosen-c1.4-pdf0075、rosen-c1.4-pdf0076
- **前置**：s14__universal_quantifier（全称量化（universal quantification，∀））、s14__existential_quantifier（存在量化（existential quantification，∃））、s14__domain_of_discourse（论域（domain of discourse））、s14__propositional_function（命题函数与谓词（propositional function / predicate））
- **对比对象**：s14__negate_quantified_statement（否定量词化命题（把否定推进量词内部））
- **易错点**：
    - 论域取全体人时，把“所有学生都学过微积分”写成 ∀x(S(x) ∧C(x))
    - 论域取全体人时，把“有的学生去过墨西哥”写成 ∃x(S(x) →M(x))
    - 不先改写句子就直接硬套量词，结果连该用全称还是存在都没确定

**★ 子目标（6 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **先把原句改写成能看清量词的说法，再确定该用全称还是存在** | `Solution: First, we rewrite the statement so that we can clearly identify the appropriate quanti- ﬁers to use. Doing so, we obtain:` |  |
| 2 | **引入变量，把句子改写成“对每个 x……”这种带变量的形式** | `“For every student x in this class, x has studied calculus.”` |  |
| 3 | **为每个性质引入一个谓词符号，并写明它表示什么** | `Continuing, we introduce C(x), which is the statement “x has studied calculus.” Consequently,` |  |
| 4 | **选定论域；若把论域放大到全体对象，全称句要改用条件式表达** | `If we change the domain to consist of all people, we will need to express our statement as “For every person x, if person x is a student in this class, then x has studied calculus.” If S(x) represents the statement that person x is in this class, we see that our statement can` |  |
| 5 | **存在句在放大论域后要用合取把限定条件与性质连起来** | `In this case, the domain for the variable x consists of all people. We introduce S(x) to represent “x is a student in this class.” Our solution becomes ∃x(S(x) ∧M(x)) because the statement is that there is a person x who is a student in this class and who has visited Mexico. [Caution! Our` |  |
| 6 | **翻译完回头检查连接词：全称句误用 ∧、存在句误用 → 都会把原意改掉** | `be expressed as ∀x(S(x) →C(x)). [Caution! Our statement cannot be expressed as ∀x(S(x) ∧ C(x)) because this statement says that all people are students in this class and have studied calculus!]` |  |

### `s14__prolog_facts_rules_queries` — 用 Prolog 事实、规则与查询做逻辑编程

- **类型**：程序性
- **出处**：rosen-c1.4-pdf0078、rosen-c1.4-pdf0079
- **前置**：s14__propositional_function（命题函数与谓词（propositional function / predicate））、s14__existential_quantifier（存在量化（existential quantification，∃））、s14__universal_quantifier（全称量化（universal quantification，∀））
- **易错点**：
    - 把 Prolog 里的逗号当成分隔符，忘了它表示谓词的合取
    - 把大写开头的名字当成常量（Prolog 把大写开头视为变量）
    - 以为事实本身表达了“存在”，却把规则体部里暗含的存在量化当成全称条件

**★ 子目标（4 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **先把已知对象间的关系写成事实，用事实定义基本谓词** | `rules. Prolog facts deﬁne predicates by specifying the elements that satisfy these predicates.` |  |
| 2 | **用已有事实定义新谓词时写出规则：头部是待定义谓词，体部把已定义的条件并列列出** | `rules. Prolog facts deﬁne predicates by specifying the elements that satisfy these predicates. Prolog rules are used to deﬁne new predicates using those already deﬁned by Prolog facts.` |  |
| 3 | **对具体对象提问时，用查询检查该事实是否已被给出，直接得到是/否** | `Prolog answers queries using the facts and rules it is given. For example, using the facts and rules listed, the query ?enrolled(kevin,math273) produces the response yes` |  |
| 4 | **查询里带变量提问时，把该变量在所有匹配事实中的取值全部列出来** | `To produce this response, Prolog determines all possible values of X for which enrolled(X, math273) has been included as a Prolog fact. Similarly, to ﬁnd all the professors` |  |

### `s15__nested_quantifiers` — 嵌套量词（nested quantifiers）

- **类型**：概念
- **出处**：rosen-c1.5-pdf0084、rosen-c1.5-pdf0085
- **对比对象**：s15__order_of_quantifiers（量词顺序（order of quantifiers））
- **易错点**：
    - 把嵌套量词命题当成分开的几个单量词命题，忽略内层量词还依赖外层变量
    - 读 ∀x∃y(x + y = 0) 时，把内层 ∃y 当成与外层 x 无关的独立命题

### `s15__order_of_quantifiers` — 量词顺序（order of quantifiers）

- **类型**：概念
- **出处**：rosen-c1.5-pdf0085、rosen-c1.5-pdf0086
- **前置**：s15__nested_quantifiers（嵌套量词（nested quantifiers））
- **上位**：s15__nested_quantifiers（嵌套量词（nested quantifiers））
- **对比对象**：s15__same_type_quantifier_order（同类量词的顺序可交换）
- **易错点**：
    - 因为两个命题只差量词的书写顺序，就断定 ∃y∀xP(x, y) 与 ∀x∃yP(x, y) 逻辑等价
    - 由一种顺序的命题为真推出另一种顺序的命题为真，把单向蕴含当成双向等价
    - 把外层存在量词选出的对象当成可以随内层变量的取值变化

### `s15__same_type_quantifier_order` — 同类量词的顺序可交换

- **类型**：概念
- **出处**：rosen-c1.5-pdf0085、rosen-c1.5-pdf0086
- **前置**：s15__order_of_quantifiers（量词顺序（order of quantifiers））
- **上位**：s15__order_of_quantifiers（量词顺序（order of quantifiers））
- **对比对象**：s15__order_of_quantifiers（量词顺序（order of quantifiers））
- **易错点**：
    - 把“全为全称或全为存在时可以交换顺序”推广到全称与存在混用的情形
    - 把仅含同类量词的式子交换顺序后，又当作新命题重新判断真假

### `s15__two_variable_quantification_truth_conditions` — 二元量化命题的真值条件（Table 1）

- **类型**：概念
- **出处**：rosen-c1.5-pdf0086
- **前置**：s15__nested_quantifiers（嵌套量词（nested quantifiers））
- **上位**：s15__nested_quantifiers（嵌套量词（nested quantifiers））
- **对比对象**：s15__order_of_quantifiers（量词顺序（order of quantifiers））
- **易错点**：
    - 把外层全称、内层存在的命题为假说成“存在一对取值使谓词为假”（正确条件是存在一个外层取值，使内层对每个取值都为假）
    - 把两种异类量词顺序的真假条件互换
    - 判断外层与内层都是存在的命题为假时，只找到一个反例就下结论

### `s15__prenex_normal_form` — 前束范式（prenex normal form, PNF）

- **类型**：概念
- **出处**：rosen-c1.5-pdf0095
- **前置**：s15__nested_quantifiers（嵌套量词（nested quantifiers））、s15__negate_nested_quantifiers（否定嵌套量词命题（把否定推进到谓词前））
- **对比对象**：s15__negate_nested_quantifiers（否定嵌套量词命题（把否定推进到谓词前））
- **易错点**：
    - 把 ∃xP(x) ∨∀xQ(x) 当成前束范式（量词没有全部出现在最前面）
    - 以为只有一部分语句能化成前束范式（教材说每个这样的语句都能）

### `s15__evaluate_nested_quantification_truth` — 用嵌套循环判定嵌套量化命题的真值

- **类型**：程序性
- **出处**：rosen-c1.5-pdf0084、rosen-c1.5-pdf0085
- **前置**：s15__nested_quantifiers（嵌套量词（nested quantifiers））
- **对比对象**：s15__two_variable_quantification_truth_conditions（二元量化命题的真值条件（Table 1））
- **易错点**：
    - 对无限论域也声称已经用循环法遍历完了所有取值
    - 判断外层全称的命题为真时，只检查了一部分外层取值就下结论
    - 以为外层存在的命题也要把全部取值都检查完才能判定为真

**★ 子目标（5 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **把多变量量化想成嵌套循环：外层每取一个值，内层就把全部取值走一遍** | `In working with quantiﬁcations of more
than one variable, it is sometimes helpful to think in terms of nested loops. (If there are inﬁnitely
many elements in the domain of some variable, we cannot actually loop through all values.
Nevertheless, this way of thinking is helpful in understanding nested quantiﬁers.)` |  |
| 2 | **外层与内层都是全称：任取一对取值一旦使谓词为假，整个命题即为假** | `For example, to see whether ∀x∀yP(x, y) is true, we loop through the values for x, and for each x we loop through the values for y.` |  |
| 3 | **外层全称、内层存在：每个外层取值都要找到一个内层取值使命题为真，某一个外层取值找不到即为假** | `Similarly, to determine whether ∀x∃yP(x, y) is true, we loop through the values for x. For
each x we loop through the values for y until we ﬁnd a y for which P(x, y) is true. If for every x we
hit such a y, then ∀x∃yP(x, y) is true; if for some x we never hit such a y, then ∀x∃yP(x, y) is false.` |  |
| 4 | **外层存在、内层全称：找到一个外层取值使内层全部为真即为真，从未找到即为假** | `To see whether ∃x∀yP(x, y) is true, we loop through the values for x until we ﬁnd an x for
which P(x, y) is always true when we loop through all values for y. Once we ﬁnd such an x, we
know that ∃x∀yP(x, y) is true. If we never hit such an x, then we know that ∃x∀yP(x, y) is false.` |  |
| 5 | **外层与内层都是存在：找到一对使谓词为真的取值即为真，一对都找不到才为假** | `Finally, to see whether ∃x∃yP(x, y) is true, we loop through the values for x, where for each
x we loop through the values for y until we hit an x for which we hit a y for which P(x, y) is true.
The statement ∃x∃yP(x, y) is false only if we never hit an x for which we hit a y such that P(x, y)
is true.` |  |

> ⚠️ **课件没交代的地方（讲解若补上，属补充解释而非课件内容）**：
> - 第 1 步「把多变量量化想成嵌套循环：外层每取一个值，内层就把全部取值走一遍」：教材只说这种想法“有帮助”并提醒无限论域无法真的遍历，没有交代循环视角为什么与量词的真值条件一致。

### `s15__read_nested_quantification_in_english` — 把嵌套量化表达式逐层读成自然语言

- **类型**：程序性
- **出处**：rosen-c1.5-pdf0084、rosen-c1.5-pdf0088
- **前置**：s15__nested_quantifiers（嵌套量词（nested quantifiers））
- **对比对象**：s15__translate_english_sentence_to_nested_quantifiers（把英文语句翻译成嵌套量化表达式）
- **易错点**：
    - 跳过“先写出量词和谓词的含义”，直接凭印象猜整句意思
    - 只把量词翻成“对每个/存在”，不翻译谓词，得到读不通的句子
    - 把主联结词是析取的式子读成合取，得出比原句更强的意思

**★ 子目标（3 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **把量词辖域内的整块式子当作一个命题函数，先分层再逐层读** | `Note that everything within the scope of a quantiﬁer can be thought of as a propositional func-
tion. For example,
∀x∃y(x + y = 0)
is the same thing as ∀xQ(x), where Q(x) is ∃yP(x, y), where P(x, y) is x + y = 0.` |  |
| 2 | **逐个弄清式中每个量词和谓词各自的含义，再合成整句** | `To understand statements involving nested quantiﬁers, we need to unravel what the quantiﬁers
and predicates that appear mean. This is illustrated in Examples 1 and 2.` |  |
| 3 | **先把量词与谓词的含义写全，再把它压缩成一句更简洁的自然语言** | `Expressions with nested quantiﬁers expressing statements in English can be quite complicated.
The ﬁrst step in translating such an expression is to write out what the quantiﬁers and predicates
in the expression mean. The next step is to express this meaning in a simpler sentence. This
process is illustrated in Examples 9 and 10.` |  |

### `s15__compare_quantifier_order` — 比较不同量词顺序的命题（等价性与蕴含方向）

- **类型**：程序性
- **出处**：rosen-c1.5-pdf0085、rosen-c1.5-pdf0086
- **前置**：s15__nested_quantifiers（嵌套量词（nested quantifiers））、s15__order_of_quantifiers（量词顺序（order of quantifiers））
- **对比对象**：s15__same_type_quantifier_order（同类量词的顺序可交换）
- **易错点**：
    - 只比较谓词是否相同就断定两个量词顺序不同的命题等价
    - 以外层存在量词开头的命题为真时，以为内层对象可以随外层取值变化
    - 把“同类量词可交换”当成“任何量词都可交换”来用

**★ 子目标（6 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **先看量词种类是否一致：全称与存在混用时，顺序不能随意调换** | `Many mathematical statements involve multiple quantiﬁcations of propositional functions in-
volving more than one variable. It is important to note that the order of the quantiﬁers is impor-
tant, unless all the quantiﬁers are universal quantiﬁers or all are existential quantiﬁers.
These remarks are illustrated by Examples 3–5.` |  |
| 2 | **同类量词（全为全称或全为存在）可以直接交换顺序而不改变意义** | `This illustrates the principle that the order of nested universal quantiﬁers in a statement without
other quantiﬁers can be changed without changing the meaning of the quantiﬁed statement.` |  |
| 3 | **确认两种顺序的命题是否逻辑等价：异类量词互换顺序后不等价** | `Example 4 illustrates that the order in which quantiﬁers appear makes a diﬀerence. The
statements ∃y∀xP(x, y) and ∀x∃yP(x, y) are not logically equivalent.` |  |
| 4 | **外层存在、内层全称：要求存在一个与外层取值无关的固定对象，使谓词对每个取值都成立** | `The statement ∃y∀xP(x, y)
is true if and only if there is a y that makes P(x, y) true for every x. So, for this statement to
be true, there must be a particular value of y for which P(x, y) is true regardless of the choice
of x.` |  |
| 5 | **外层全称、内层存在：内层对象允许随外层取值变化（可以依赖外层取值）** | `On the other hand, ∀x∃yP(x, y) is true if and only if for every value of x there is a value
of y for which P(x, y) is true. So, for this statement to be true, no matter which x you choose,
there must be a value of y (possibly depending on the x you choose) for which P(x, y) is true.
In other words, in the second case, y can depend on x, whereas in the ﬁrst case, y is a constant
independent of x.` |  |
| 6 | **定出蕴含方向：前者为真可推出后者为真，反之不成立** | `From these observations, it follows that if ∃y∀xP(x, y) is true, then ∀x∃yP(x, y) must also
be true. However, if ∀x∃yP(x, y) is true, it is not necessary for ∃y∀xP(x, y) to be true. (See
Supplementary Exercises 30 and 31.)` |  |

> ⚠️ **课件没交代的地方（讲解若补上，属补充解释而非课件内容）**：
> - 第 6 步「定出蕴含方向：前者为真可推出后者为真，反之不成立」：教材只写“从这些观察可得”并把证明指向 Supplementary Exercises 30 和 31，本节没有给出该单向蕴含的证明。

### `s15__translate_math_statement_to_nested_quantifiers` — 把数学命题翻译成嵌套量化表达式

- **类型**：程序性
- **出处**：rosen-c1.5-pdf0087、rosen-c1.5-pdf0088
- **前置**：s15__nested_quantifiers（嵌套量词（nested quantifiers））
- **对比对象**：s15__translate_english_sentence_to_nested_quantifiers（把英文语句翻译成嵌套量化表达式）
- **易错点**：
    - 论域已经取正整数，还在表达式里重复加上大于零的条件
    - 论域取全体整数时漏掉“都是正数”这类条件，使命题比原句更宽
    - 把“当…时”“只要…就…”这层条件漏掉，不写成蕴含

**★ 子目标（4 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **先把隐含的量词和论域显式写出来，再引入变量** | `To translate this statement into a logical expression, we ﬁrst rewrite it so that the
implied quantiﬁers and a domain are shown: “For every two integers, if these integers are both
positive, then the sum of these integers is positive.” Next, we introduce the variables x and y to
obtain “For all positive integers x and y, x + y is positive.` |  |
| 2 | **也可以用缩小论域代替在表达式里加条件，使式子更简洁** | `Note that we could also translate
this using the positive integers as the domain. Then the statement “The sum of two positive
integers is always positive” becomes “For every two positive integers, the sum of these integers
is positive.” We can express this as
∀x∀y(x + y > 0),
where the domain for both variables consists of all positive integers.` |  |
| 3 | **把“除某个值以外”的限制改写成条件式，放在蕴含的前件** | `We ﬁrst rewrite this as “For every real number x except zero, x has a multiplicative
inverse.” We can rewrite this as “For every real number x, if x ≠0, then there exists a real
number y such that xy = 1.” This can be rewritten as
∀x((x ≠0) →∃y(xy = 1)).` |  |
| 4 | **按“对每个…存在…”的先后把定义逐层写成量词串，把“只要…就…”写成蕴含** | `Recall that the deﬁnition of the statement
lim
x→a f(x) = L
is: For every real number 𝜖> 0 there exists a real number 𝛿> 0 such that |f(x) −L| < 𝜖
whenever 0 < |x −a| < 𝛿. This deﬁnition of a limit can be phrased in terms of quantiﬁers by
∀𝜖∃𝛿∀x(0 < |x −a| < 𝛿→|f(x) −L| < 𝜖),
where the domain for the variables 𝛿and 𝜖consists of all positive real numbers and for x consists
of all real numbers.` |  |

> ⚠️ **课件没交代的地方（讲解若补上，属补充解释而非课件内容）**：
> - 第 1 步「先把隐含的量词和论域显式写出来，再引入变量」：教材只示范“先把隐含的量词和论域写出来”，没有说明为什么必须先做这一步。

### `s15__translate_english_sentence_to_nested_quantifiers` — 把英文语句翻译成嵌套量化表达式

- **类型**：程序性
- **出处**：rosen-c1.5-pdf0089、rosen-c1.5-pdf0090
- **前置**：s15__nested_quantifiers（嵌套量词（nested quantifiers））
- **对比对象**：s15__read_nested_quantification_in_english（把嵌套量化表达式逐层读成自然语言）
- **易错点**：
    - 把“如果某对象满足条件，则存在另一对象…”写成合取而不是蕴含
    - 用一个笼统的关系谓词代替分层谓词，掩盖各层变量之间的关系
    - 把可以左移的量词留在原处，导致辖域与题意不一致

**★ 子目标（3 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **把“如果某对象满足条件，则存在另一对象与之有关系”写成全称量词加蕴含** | `The statement “If a person is female and is a parent, then this person is someone’s
mother” can be expressed as “For every person x, if person x is female and person x is a parent,
then there exists a person y such that person x is the mother of person y.” We introduce the
propositional functions F(x) to represent “x is female,” P(x) to represent “x is a parent,” and
M(x, y) to represent “x is the mother of y.” The original statement can be represented as
∀x((F(x) ∧P(x)) →∃yM(x, y)).` |  |
| 2 | **把不依赖某变量的量词左移到合适位置，得到辖域正确的等价式** | `Using the null quantiﬁcation rule in part (b) of Exercise 49 in Section 1.4, we can move ∃y to
the left so that it appears just after ∀x, because y does not appear in F(x) ∧P(x). We obtain the
logically equivalent expression
∀x∃y((F(x) ∧P(x)) →M(x, y)).` |  |
| 3 | **为每一层对象分别引入关系谓词，避免一个笼统谓词掩盖变量之间的关系** | `The statement could also be expressed as
∃w∀a∃fR(w, f, a),
where R(w, f, a) is “w has taken f on a.” Although this is more compact, it somewhat
obscures the relationships among the variables. Consequently, the ﬁrst solution is usually
preferable.` |  |

### `s15__express_exactly_one_quantification` — 用嵌套量词表达“恰好一个”

- **类型**：程序性
- **出处**：rosen-c1.5-pdf0089
- **前置**：s15__nested_quantifiers（嵌套量词（nested quantifiers））、s15__translate_english_sentence_to_nested_quantifiers（把英文语句翻译成嵌套量化表达式）
- **对比对象**：s15__translate_english_sentence_to_nested_quantifiers（把英文语句翻译成嵌套量化表达式）
- **易错点**：
    - 把“恰好一个”只写成存在量词，丢掉“其余对象都不满足”这一支，退化成“至少一个”
    - 把唯一性约束写成“还存在另一个对象满足关系”，方向写反

**★ 子目标（3 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **先把句子改写成“对每个对象，该对象恰好有一个…”的形式，再引入全称量词** | `The statement “Everyone has exactly one best friend” can be expressed as “For every
person x, person x has exactly one best friend.” Introducing the universal quantiﬁer, we see
that this statement is the same as “∀x(person x has exactly one best friend),” where the domain
consists of all people.` |  |
| 2 | **把“恰好一个”拆成“存在一个满足关系的对象”与“其余任何对象都不满足”，并用合取连接、用内层全称量词写成条件式** | `To say that x has exactly one best friend means that there is a person y who is the best friend
of x, and furthermore, that for every person z, if person z is not person y, then z is not the best
friend of x. When we introduce the predicate B(x, y) to be the statement “y is the best friend of
x,” the statement that x has exactly one best friend can be represented as
∃y(B(x, y) ∧∀z((z ≠y) →¬B(x, z))).` |  |
| 3 | **也可以改用唯一性量词把整个表达式简写** | `[Note that we can write this statement as ∀x∃!yB(x, y), where ∃! is the “uniqueness quantiﬁer”
deﬁned in Section 1.4.]` |  |

### `s15__negate_nested_quantifiers` — 否定嵌套量词命题（把否定推进到谓词前）

- **类型**：程序性
- **出处**：rosen-c1.5-pdf0090、rosen-c1.5-pdf0091
- **前置**：s15__nested_quantifiers（嵌套量词（nested quantifiers））
- **对比对象**：s15__prenex_normal_form（前束范式（prenex normal form, PNF））
- **易错点**：
    - 只把最外层量词取反就停下，没有把否定一路推到谓词前
    - 把否定整句的嵌套量化写成量词不变、只给谓词加否定
    - 否定落到蕴含上时对前件和后件分别取反，而不是用蕴含的否定等价式

**★ 子目标（5 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **先把整句识别成某个已知命题的否定，写出最外层的否定号** | `This statement is the negation of the statement “There is a woman who has taken
a ﬂight on every airline in the world” from Example 13. By Example 13, our statement can
be expressed as ¬∃w∀a∃f(P(w, f) ∧Q( f, a)), where P(w, f) is “w has taken f” and Q( f, a) is
“f is a ﬂight on a.` |  |
| 2 | **从最外层量词开始，逐次应用量词德摩根律把否定推到所有量词的内侧** | `By successively applying De Morgan’s laws for quantiﬁers in Table 2 of
Section 1.4, we can move the negation in ¬∀x∃y(xy = 1) inside all the quantiﬁers.` |  |
| 3 | **否定落到合取（或析取）上时，改用联结词的德摩根律处理最后一步** | `By successively applying De Morgan’s laws for quantiﬁers in Table 2 of
Section 1.4 to move the negation inside successive quantiﬁers and by applying De Morgan’s
law for negating a conjunction in the last step, we ﬁnd that our statement is equivalent to each
of this sequence of statements:` |  |
| 4 | **否定落到蕴含上时，改用蕴含的否定等价式把它拆成合取** | `In the last step we used the equivalence ¬(p →q) ≡p ∧¬q, which follows from the ﬁfth
equivalence in Table 7 of Section 1.3.` |  |
| 5 | **把谓词里的否定化简成更自然的写法** | `Because
¬(xy = 1) can be expressed more simply as xy ≠1, we conclude that our negated statement can
be expressed as ∃x∀y(xy ≠1).` |  |

### `s16__valid_argument_form` — 有效论证与论证形式（valid argument / argument form）

- **类型**：概念
- **出处**：rosen-c1.6-pdf0096、rosen-c1.6-pdf0097
- **对比对象**：s16__argument_construction（由前提构造有效论证（build an argument））
- **易错点**：
    - 把“前提全真则结论必真”的形式有效性，说成“结论事实上为真”——前提为假时论证照样有效，但结论不能保证为真
    - 只检验某一次代入后结论的真假，而不检验“所有代入下前提真是否都逼出结论真”
    - 把论证形式有效误认为是在断言前提本身为真

### `s16__rules_of_inference` — 推理规则（rules of inference）

- **类型**：概念
- **出处**：rosen-c1.6-pdf0096、rosen-c1.6-pdf0098
- **前置**：s16__valid_argument_form（有效论证与论证形式（valid argument / argument form））
- **对比对象**：s16__fallacies（谬误：肯定结论与否定假设（fallacies））
- **易错点**：
    - 把“规则”当成待证明的结论而不是可反复套用的模板，每遇到一个论证都从真值表重新算一遍
    - 把与真值表判定并列的推理规则当成“更弱的近似方法”，以为规则推出的结论只是可能真

### `s16__tautology_validity_check` — 用真值表判定论证形式有效（truth table method）

- **类型**：程序性
- **出处**：rosen-c1.6-pdf0097、rosen-c1.6-pdf0098、rosen-c1.6-pdf0099
- **前置**：s16__valid_argument_form（有效论证与论证形式（valid argument / argument form））
- **对比对象**：s16__fallacies（谬误：肯定结论与否定假设（fallacies））、s16__rule_identification（判定一个论证用了哪条推理规则）
- **易错点**：
    - 以为只要找出“使结论为真”的一行就证明了有效
    - 变量稍多就硬列真值表，忽略 2^n 行的代价与用推理规则替代的必要性

**★ 子目标（3 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **按重言式判据写出待检验的蕴含式** | `Remark: From the deﬁnition of a valid argument form we see that the argument form with premises p1, p2, … , pn and conclusion q is valid exactly when (p1 ∧p2 ∧⋯∧pn) →q is a tautology.` |  |
| 2 | **穷举赋值，找前提全真而结论为假的行** | `We can always use a truth table to show that an argument form is valid. We do this by showing that whenever the premises are true, the conclusion must also be true. However, this can be a tedious approach.` |  |
| 3 | **从已证重言式读出规则，替代逐行穷举** | `The tautology (p ∧(p →q)) →q is the basis of the rule of inference called modus ponens, or the law of detachment.` |  |

### `s16__modus_ponens` — 假言推理 / 肯定前件（modus ponens）

- **类型**：概念
- **出处**：rosen-c1.6-pdf0098、rosen-c1.6-pdf0099
- **前置**：s16__valid_argument_form（有效论证与论证形式（valid argument / argument form））
- **上位**：s16__rules_of_inference（推理规则（rules of inference））
- **对比对象**：s16__fallacies（谬误：肯定结论与否定假设（fallacies））
- **易错点**：
    - 把肯定后件当成肯定前件使用：已知 p →q 与 q 就断言 p
    - 条件句方向被读反，由 p →q 与 p 去推出前件不成立

### `s16__disjunctive_syllogism` — 析取三段论（disjunctive syllogism）

- **类型**：概念
- **出处**：rosen-c1.6-pdf0099、rosen-c1.6-pdf0100
- **前置**：s16__valid_argument_form（有效论证与论证形式（valid argument / argument form））
- **上位**：s16__rules_of_inference（推理规则（rules of inference））
- **对比对象**：s16__resolution_proof（归结证明（resolution））
- **易错点**：
    - 在二选一里误用否定去消去“结论的那一支”而不是被否定的那一支
    - 忽略析取是相容的，未排除两支同真的情形就下断言

### `s16__rule_identification` — 判定一个论证用了哪条推理规则

- **类型**：程序性
- **出处**：rosen-c1.6-pdf0098、rosen-c1.6-pdf0099、rosen-c1.6-pdf0100
- **前置**：s16__rules_of_inference（推理规则（rules of inference））
- **对比对象**：s16__argument_construction（由前提构造有效论证（build an argument））
- **易错点**：
    - 直接凭生活语义给论证贴规则标签，而不先把命题符号化再逐符号比对形式
    - 把内容相近但形式不同的论证（如含传递的两步条件句）当成同一条规则

**★ 子目标（3 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **把论证的每个命题符号化** | `In each argument, we ﬁrst use propositional variables to express the propositions in the argument.` |  |
| 2 | **写出论证形式** | `We then show that the resulting argument form is a rule of inference from Table 1.` |  |
| 3 | **与已列出的规则模板逐一比对，指出所用规则** | `State which rule of inference is the basis of the following argument: “It is below freezing now. Therefore, it is below freezing or raining now.”` |  |

### `s16__argument_construction` — 由前提构造有效论证（build an argument）

- **类型**：程序性
- **出处**：rosen-c1.6-pdf0096、rosen-c1.6-pdf0100、rosen-c1.6-pdf0101
- **前置**：s16__rules_of_inference（推理规则（rules of inference））、s16__modus_ponens（假言推理 / 肯定前件（modus ponens））、s16__rule_identification（判定一个论证用了哪条推理规则）
- **对比对象**：s16__valid_argument_form（有效论证与论证形式（valid argument / argument form））
- **易错点**：
    - 只写结论不给每步理由，或理由写成“显然”
    - 把结论的前提直接当成已获得的前提，中途引入没给出的假设
    - 前提很多时仍拒绝分步，试图一步跳到结论

**★ 子目标（4 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **把英文论证符号化并写出前提与结论** | `Then the premises are p →q, ¬p →r, and r →s. The desired conclusion is ¬q →s. We need to give a valid argument with premises p →q, ¬p →r, and r →s and conclusion ¬q →s.` |  |
| 2 | **逐步列出每行并标注依据** | `This is illustrated by Examples 6 and 7, where the steps of arguments are displayed on separate lines, with the reason for each step explicitly stated.` |  |
| 3 | **把每一步归约到已确立的规则** | `These examples also show how arguments in English can be analyzed using rules of inference.` |  |
| 4 | **把已证等价式（如逆否）当作中间步骤来用** | `This argument form shows that the premises lead to the desired conclusion.` |  |

> ⚠️ **课件没交代的地方（讲解若补上，属补充解释而非课件内容）**：
> - 第 4 步「把已证等价式（如逆否）当作中间步骤来用」：教材给出了 Example 7 的完整步骤表（其中把 (1) 换成其逆否命题再作假言三段论），但没有单列“何时该用逆否式替换条件句”的选步规则，需要在例题里自行归纳。

### `s16__fallacies` — 谬误：肯定结论与否定假设（fallacies）

- **类型**：概念
- **出处**：rosen-c1.6-pdf0102
- **前置**：s16__valid_argument_form（有效论证与论证形式（valid argument / argument form））、s16__modus_ponens（假言推理 / 肯定前件（modus ponens））
- **对比对象**：s16__modus_ponens（假言推理 / 肯定前件（modus ponens））
- **易错点**：
    - 由 p →q 与 q 推出 p（肯定结论）
    - 由 p →q 与 ¬p 推出 ¬q（否定假设）
    - 把“前提假”当成论证无效的理由，或反过来把“结论假”当成形式无效的证据

### `s16__invalid_argument_detection` — 识别并命名无效论证形式

- **类型**：程序性
- **出处**：rosen-c1.6-pdf0102
- **前置**：s16__valid_argument_form（有效论证与论证形式（valid argument / argument form））、s16__fallacies（谬误：肯定结论与否定假设（fallacies））
- **对比对象**：s16__tautology_validity_check（用真值表判定论证形式有效（truth table method））
- **易错点**：
    - 举出一个“结论碰巧为假”的实例当作形式无效的证明，而不是给出让前提全真结论为假的赋值
    - 看出论证不对却说不出所用形式的名称与错因

**★ 子目标（2 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **给出前提全真而结论为假的一组赋值，说明它不是重言式** | `The proposition ((p →q) ∧q) →p is not a tautology, because it is false when p is false and q is true.` |  |
| 2 | **把该形式归入已知谬误并指出错在哪一步** | `This type of incorrect reasoning is called the fallacy of aﬃrming the conclusion.` |  |

### `s16__resolution_proof` — 归结证明（resolution）

- **类型**：程序性
- **出处**：rosen-c1.6-pdf0101、rosen-c1.6-pdf0102
- **前置**：s16__disjunctive_syllogism（析取三段论（disjunctive syllogism））、s16__valid_argument_form（有效论证与论证形式（valid argument / argument form））
- **对比对象**：s16__disjunctive_syllogism（析取三段论（disjunctive syllogism））
- **易错点**：
    - 把归结当成能直接作用于任意原句的规则，忘记必须先化子句
    - 把 x ∨(y ∧z) 这样的合取误当成一个子句，不拆成两条
    - 只用一条前提去归结，忽略两条前提各出一个互补文字才产生归结式

**★ 子目标（4 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **先把所有前提与结论化为子句** | `To construct proofs in propositional logic using resolution as the only rule of inference, the hypotheses and the conclusion must be expressed as clauses, where a clause is a disjunction of variables or negations of these variables.` |  |
| 2 | **把非子句语句改写成等价子句** | `We can replace a statement in propositional logic that is not a clause by one or more equivalent statements that are clauses.` |  |
| 3 | **消去互补文字，取其余文字的析取得归结式** | `The ﬁnal disjunction in the resolution rule, q ∨r, is called the resolvent.` |  |
| 4 | **取两条子句归结，直到得到目标子句** | `Using the two clauses p ∨r and ¬r ∨s, we can use resolution to conclude p ∨s.` |  |

### `s16__universal_instantiation` — 全称例示（universal instantiation）

- **类型**：概念
- **出处**：rosen-c1.6-pdf0102、rosen-c1.6-pdf0103
- **前置**：s16__valid_argument_form（有效论证与论证形式（valid argument / argument form））
- **对比对象**：s16__existential_instantiation（存在例示（existential instantiation））
- **易错点**：
    - 例示出的个体自带了原语句没说的性质（例如由“所有女性都睿智”推出 Lisa 还额外满足别的条件）
    - 把全称例示与存在例示混用，以为 ∀xP(x) 可以给出一个“满足某个额外条件的 c”

### `s16__existential_instantiation` — 存在例示（existential instantiation）

- **类型**：概念
- **出处**：rosen-c1.6-pdf0103
- **前置**：s16__valid_argument_form（有效论证与论证形式（valid argument / argument form））
- **对比对象**：s16__universal_instantiation（全称例示（universal instantiation））、s16__existential_generalization（存在推广（existential generalization））
- **易错点**：
    - 把存在例示出的见证元当成任意元素，对 c 附加额外假设
    - 同一个见证元符号被两次存在例示复用，或把由存在例示得到的 c 再拿去作全称推广

### `s16__universal_generalization` — 全称推广（universal generalization）

- **类型**：概念
- **出处**：rosen-c1.6-pdf0102、rosen-c1.6-pdf0103
- **前置**：s16__valid_argument_form（有效论证与论证形式（valid argument / argument form））
- **对比对象**：s16__universal_instantiation（全称例示（universal instantiation））、s16__existential_instantiation（存在例示（existential instantiation））
- **易错点**：
    - 所用的 c 是特殊的（某个具体个体或额外假设下的个体），却据此断言 ∀xP(x)
    - 对元素 c 偷偷加上论证中未获授权的前提后再作全称推广

### `s16__existential_generalization` — 存在推广（existential generalization）

- **类型**：概念
- **出处**：rosen-c1.6-pdf0103
- **前置**：s16__valid_argument_form（有效论证与论证形式（valid argument / argument form））
- **对比对象**：s16__existential_instantiation（存在例示（existential instantiation））
- **易错点**：
    - 把只对某个特定个体成立的性质直接推广成对全体的断言
    - 误以为存在推广要求掌握满足条件的具体是哪一个元素

### `s16__combined_quantifier_propositional_rules` — 量词规则与命题规则的组合（universal modus ponens / universal modus tollens）

- **类型**：程序性
- **出处**：rosen-c1.6-pdf0104、rosen-c1.6-pdf0105
- **前置**：s16__universal_instantiation（全称例示（universal instantiation））、s16__modus_ponens（假言推理 / 肯定前件（modus ponens））、s16__argument_construction（由前提构造有效论证（build an argument））
- **对比对象**：s16__fallacies（谬误：肯定结论与否定假设（fallacies））
- **易错点**：
    - 把 a 当成被全称量词覆盖的任意元素，而不是域中一个确定的个体
    - 拿一个不满足前件 P(a) 的 a 去使用该组合规则
    - 看到 ∀x(P(x) →Q(x)) 与 ¬Q(a) 时误用肯定式去推 Q(a)

**★ 子目标（3 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **先做全称例示，得到该个体的条件句** | `To see this, note that by universal instantiation, P(a) →Q(a) is true.` |  |
| 2 | **确认该个体满足全称条件句的前件** | `This rule tells us that if ∀x(P(x) →Q(x)) is true, and if P(a) is true for a particular element a in the domain of the universal quantiﬁer, then Q(a) must also be true.` |  |
| 3 | **用肯定式得到该个体的结论** | `It follows by universal modus ponens that Q(100) is true, namely, that 1002 < 2100.` |  |

### `s17__theorem` — 定理（theorem）

- **类型**：概念
- **出处**：rosen-c1.7-pdf0108
- **对比对象**：s17__lemma_corollary_conjecture（引理、推论与猜想（lemma, corollary, conjecture））
- **易错点**：
    - 把 1.1 里的命题（proposition，有真值的陈述句）与本节的命题（proposition，指不太重要的定理）当成同一回事
    - 以为定理必须写成条件语句（教材指出定理也可以是完全不同形式的逻辑陈述）
    - 把猜想当定理引用（猜想只是被提出为真的陈述，只有找到证明之后才成为定理）

### `s17__proof` — 证明（proof）

- **类型**：概念
- **出处**：rosen-c1.7-pdf0108、rosen-c1.7-pdf0109
- **前置**：s17__theorem（定理（theorem））
- **对比对象**：s17__mistakes_in_proofs（证明中的常见错误（mistakes in proofs））
- **易错点**：
    - 把公理也当成需要证明的命题（公理是被假定为真、无须证明的陈述）
    - 随手引用没有证明过的结论或凭直觉跳步（构造证明时只能用公理、定义和已证结果这些事实）
    - 以为每一步都必须显式写出所用规则（面向人类读者的证明几乎都是非形式证明：一步里可以用多条规则、可以跳步、不显式声明公理与推理规则）
    - 以为证明不写全就会被判错（教材明确说若把每一步都写出来，证明会长得无法阅读）

### `s17__lemma_corollary_conjecture` — 引理、推论与猜想（lemma, corollary, conjecture）

- **类型**：概念
- **出处**：rosen-c1.7-pdf0108
- **前置**：s17__theorem（定理（theorem））
- **对比对象**：s17__theorem（定理（theorem））
- **易错点**：
    - 以为引理本身就是不值钱的小结论（引理是为证明其他结果服务的辅助定理，复杂证明常先拆成一系列引理逐个证明）
    - 把推论当成需要从头独立证明的新定理（推论是可以直接从已证定理得到的）
    - 把猜想当成定理来引用（猜想在被证明之前不是定理，而且很多猜想最后被证明是假的）

### `s17__even_odd_parity` — 偶数、奇数与奇偶性（even, odd, parity）

- **类型**：概念
- **出处**：rosen-c1.7-pdf0109
- **易错点**：
    - 以为一个整数可以既是偶数又是奇数（定义明确说每个整数非偶即奇，且不会既偶又奇）
    - 只把“是奇数”当成一个性质而不展开成可代入运算的形式（必须写成比某个整数大一倍的样子才能继续计算）
    - 在逆否证明里把“不是奇数”当成不好用的否定式（在整数范围内它就是偶数，可以直接展开继续推导）

### `s17__rational_irrational` — 有理数与无理数（rational, irrational）

- **类型**：概念
- **出处**：rosen-c1.7-pdf0112
- **易错点**：
    - 忽略分母不能为零这一条（定义要求存在整数之比且分母非零）
    - 把“不是有理数”当成一种正面描述，而不是“不存在满足条件的整数之比”这一否定（证明无理数要从假设能写成整数之比出发导出矛盾）
    - 证明根号 2 无理时忘记把那个分数先约到最低项，于是最后得不到“分子分母同为偶数”与“互素”的对撞

### `s17__mistakes_in_proofs` — 证明中的常见错误（mistakes in proofs）

- **类型**：概念
- **出处**：rosen-c1.7-pdf0116、rosen-c1.7-pdf0117
- **前置**：s17__proof（证明（proof））
- **对比对象**：s17__proof_by_contraposition（逆否证明（proof by contraposition））
- **易错点**：
    - 由“若前件成立则后件成立”加上后件成立，反推前件成立（肯定结论的谬误）
    - 由“若前件成立则后件成立”加上前件不成立，推出后件不成立（否定假设的谬误；正确的方向是逆否命题）
    - 把要证的结论直接当前提用（循环论证：在证明过程中直接假设结论的等价说法成立，却不给任何理由）
    - 在等式两边除以一个可能为零的式子（经典假证明里正是除以了一个等于零的差）
    - 把算术与代数上的粗心错误当成逻辑错误，或反过来只查逻辑不查每一处计算

### `s17__prove_for_all_conditional` — 证明全称量化的条件语句

- **类型**：程序性
- **出处**：rosen-c1.7-pdf0108、rosen-c1.7-pdf0109
- **前置**：s17__theorem（定理（theorem））

**★ 子目标（3 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **看清定理省略了全称量词，按“对论域中所有元素都成立”来读** | `Many theorems assert that a property holds for all elements in a domain, such as the integers or the real numbers. Although the precise statement of such theo-rems needs to include a universal quantiﬁer, the standard convention in mathematics is to omit it.` |  |
| 2 | **取论域中一个任意元素，把目标降为该元素上的条件语句** | `To prove a theorem of the form ∀x(P(x) →Q(x)), our goal is to show that P(c) →Q(c) is true, where c is an arbitrary element of the domain, and then apply universal generalization.` |  |
| 3 | **证完任意元素后引用全称推广，把结论提升到整个论域** | `Finally, universal generalization implies that the theorem holds for all members of the domain.` |  |

### `s17__direct_proof` — 直接证明（direct proof）

- **类型**：程序性
- **出处**：rosen-c1.7-pdf0108、rosen-c1.7-pdf0109
- **前置**：s17__proof（证明（proof））、s17__prove_for_all_conditional（证明全称量化的条件语句）

**★ 子目标（3 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **假设前件为真，再用公理、定义、已证定理和推理规则推向结论** | `In a direct proof, we assume that p is true and use axioms, deﬁnitions, and previously proven theorems, together with rules of inference, to show that q must also be true.` |  |
| 2 | **后续各步由推理规则接续，最后一步落到后件为真** | `subsequent steps are constructed using rules of inference, with the ﬁnal step showing that q must also be true.` |  |
| 3 | **收尾时最后一步直接写出定理的结论** | `In practice, the ﬁnal step of a proof is usually just the conclusion of the theorem.` |  |

### `s17__proof_by_contraposition` — 逆否证明（proof by contraposition）

- **类型**：程序性
- **出处**：rosen-c1.7-pdf0110、rosen-c1.7-pdf0111
- **前置**：s17__proof（证明（proof））、s17__prove_for_all_conditional（证明全称量化的条件语句）、s17__direct_proof（直接证明（direct proof））

**★ 子目标（4 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **确认可以改用逆否命题：原条件语句与逆否命题等价** | `Proofs by contraposition make use of the fact that the conditional statement p →q is equivalent to its contrapositive, ¬q →¬p.` |  |
| 2 | **把结论的否定取为前提，用公理、定义、已证定理推出前提的否定** | `In a proof by contraposition of p →q, we take ¬q as a premise, and using axioms, deﬁnitions, and previously proven theorems, together with rules of inference, we show that ¬p must follow.` |  |
| 3 | **先把“结论为假”翻译成正面说法，变成可以展开计算的形式** | `The ﬁrst step in a proof by contraposition is to assume that the conclusion of the conditional statement “If 3n + 2 is odd, then n is odd” is false; namely, assume that n is even.` |  |
| 4 | **推出前提为假后，据此断定原条件语句为真** | `Because the negation of the conclusion of the conditional statement implies that the hypothesis is false, the original conditional statement is true.` |  |

### `s17__vacuous_proof` — 空证明（vacuous proof）

- **类型**：程序性
- **出处**：rosen-c1.7-pdf0111
- **前置**：s17__proof（证明（proof））、s17__prove_for_all_conditional（证明全称量化的条件语句）

**★ 子目标（3 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **先确认假设本身是假的（假设为假时条件语句必真）** | `We can quickly prove that a conditional statement p →q is true when we know that p is false, because p →q must be true when p is false.` |  |
| 2 | **证出假设为假即完成整条证明** | `Con-sequently, if we can show that p is false, then we have a proof, called a vacuous proof, of the conditional statement p →q.` |  |
| 3 | **不去讨论结论的真假，它不影响条件语句的真值** | `The fact that the conclusion of this conditional statement, 02 > 0, is false is irrelevant to the truth value of the conditional statement, because a conditional statement with a false hypothesis is guaranteed to be true.` |  |

### `s17__trivial_proof` — 平凡证明（trivial proof）

- **类型**：程序性
- **出处**：rosen-c1.7-pdf0112
- **前置**：s17__proof（证明（proof））、s17__prove_for_all_conditional（证明全称量化的条件语句）

**★ 子目标（3 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **先确认结论已经为真** | `We can also quickly prove a conditional statement p →q if we know that the conclusion q is true.` |  |
| 2 | **证明结论为真即完成整条证明** | `By showing that q is true, it follows that p →q must also be true. A proof of p →q that uses the fact that q is true is called a trivial proof.` |  |
| 3 | **整个证明中不需要用到假设** | `Note that the hypothesis, which is the statement “a ≥b,” was not needed in this proof.` |  |

### `s17__proof_by_contradiction` — 反证法（proof by contradiction）

- **类型**：程序性
- **出处**：rosen-c1.7-pdf0113、rosen-c1.7-pdf0114
- **前置**：s17__proof（证明（proof））、s17__prove_for_all_conditional（证明全称量化的条件语句）

**★ 子目标（4 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **把待证命题的否定设为假设，目标是导出某个自相矛盾的结论** | `Because the statement r ∧¬r is a contradiction whenever r is a proposition, we can prove that p is true if we can show that ¬p →(r ∧¬r) is true for some proposition r.` |  |
| 2 | **待证的是条件语句时，改为假设“前提与结论的否定”同时为真，由它们推出矛盾** | `Proof by contradiction can be used to prove conditional statements. In such proofs, we ﬁrst assume the negation of the conclusion. We then use the premises of the theorem and the negation of the conclusion to arrive at a contradiction.` |  |
| 3 | **手上已有一条逆否证明时，补上原前提作为额外假设即可改写成反证** | `To rewrite a proof by contraposition of p →q as a proof by contradiction, we suppose that both p and ¬q are true.` |  |
| 4 | **导出矛盾后据此断定原命题成立** | `Because q is false, but ¬p →q is true, we can conclude that ¬p is false, which means that p is true.` |  |

### `s17__proof_of_equivalence` — 证明等价（双条件与多命题等价）

- **类型**：程序性
- **出处**：rosen-c1.7-pdf0115
- **前置**：s17__proof（证明（proof））、s17__direct_proof（直接证明（direct proof））、s17__proof_by_contraposition（逆否证明（proof by contraposition））

**★ 子目标（3 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **把双条件拆成两个方向，分别证明两个条件语句** | `To prove a theorem that is a biconditional statement, that is, a statement of the form p ↔q, we show that p →q and q →p are both true.` |  |
| 2 | **命题多于两个时，只需证出一圈首尾相接的蕴含链** | `This shows that if the n conditional statements p1 →p2, p2 →p3, … , pn →p1 can be shown to be true, then the propositions p1, p2, … , pn are all equivalent.` |  |
| 3 | **链条的顺序和起点可以自选，只要沿链能从任一命题走到任何另一命题** | `When we prove that a group of statements are equivalent, we can establish any chain of conditional statements we choose as long as it is possible to work through the chain to go from any one of these statements to any other statement.` |  |

### `s17__choose_proof_method` — 选择证明方法的策略

- **类型**：程序性
- **出处**：rosen-c1.7-pdf0112
- **前置**：s17__direct_proof（直接证明（direct proof））、s17__proof_by_contraposition（逆否证明（proof by contraposition））

**★ 子目标（4 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **拿到全称条件语句先评估直接证明是否可行** | `When you want to prove a statement of the form ∀x(P(x) →Q(x)), ﬁrst evaluate whether a direct proof looks promising.` |  |
| 2 | **先展开假设里的定义，再用公理与手头定理往下推** | `Begin by expanding the deﬁnitions in the hypotheses. Start to reason using these hypotheses, together with axioms and available theorems.` |  |
| 3 | **直接证明走不通时，换成逆否证明再试一遍** | `If a direct proof does not seem to go anywhere, for instance when there is no clear way to use hypotheses as in Examples 3 and 4 to reach the conclusion, try the same thing with a proof by contraposition.` |  |
| 4 | **假设本身难以利用时（否定式、非零之类的条件），提示该走间接证明** | `(Hypotheses such as x is irrational or x ≠0 that are diﬃcult to reason from are a clue that an indirect proof might be your best best.)` |  |

### `s17__find_counterexample` — 用反例反驳全称命题

- **类型**：程序性
- **出处**：rosen-c1.7-pdf0116
- **前置**：s17__theorem（定理（theorem））

**★ 子目标（3 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **要驳倒全称命题，只需给出一个使它为假的具体例子** | `to show that a statement of the form ∀xP(x) is false, we need only ﬁnd a counterexample, that is, an example x for which P(x) is false.` |  |
| 2 | **命题看似为假或反复证不出来时，转为去找反例** | `When presented with a statement of the form ∀xP(x), which we believe to be false or which has resisted all proof attempts, we look for a counterexample.` |  |
| 3 | **验证候选反例：穷举相关取值，说明它确实不满足该性质** | `note that the only perfect squares not exceeding 3 are 02 = 0 and 12 = 1. Furthermore, there is no way to get 3 as the sum of two terms each of which is 0 or 1.` |  |

### `s18__proof_by_cases` — 分情形证明（proof by cases）

- **类型**：程序性
- **出处**：rosen-c1.8-pdf0120、rosen-c1.8-pdf0121、rosen-c1.8-pdf0122
- **对比对象**：s18__exhaustive_proof（穷举证明（exhaustive proof / proof by exhaustion））
- **易错点**：
    - 漏掉某个情形就宣布证完：讨论正负时漏掉等于零的那种情况（Example 9 的假证明就败在这里）
    - 只验证了若干例子就当成覆盖了所有情形，把没证全的命题当定理用

**★ 子目标（3 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **把前提改写成覆盖全部可能的若干情形，再逐个情形证明同一个结论** | `[(p1 ∨p2 ∨⋯∨pn) →q] ↔[(p1 →q) ∧(p2 →q) ∧⋯∧(pn →q)] can be used as a rule of inference. This shows that the original conditional statement with a hypothesis made up of a disjunction of the propositions p1, p2, … , pn can be proved by proving each of the n conditional statements pi →q, i = 1, 2, … , n, individually.` |  |
| 2 | **确认所分情形合起来覆盖所有可能（漏掉一个情形，证明就作废）** | `A proof by cases must cover all possible cases that arise in a theorem.` |  |
| 3 | **判断值不值得分情形：没有明显入手点、而分情形能带来额外信息时才用** | `Generally, look for a proof by cases when there is no obvious way to begin a proof, but when extra information in each case helps move the proof forward.` |  |

### `s18__exhaustive_proof` — 穷举证明（exhaustive proof / proof by exhaustion）

- **类型**：程序性
- **出处**：rosen-c1.8-pdf0120、rosen-c1.8-pdf0121、rosen-c1.8-pdf0122
- **前置**：s18__proof_by_cases（分情形证明（proof by cases））
- **上位**：s18__proof_by_cases（分情形证明（proof by cases））
- **对比对象**：s18__proof_by_cases（分情形证明（proof by cases））
- **易错点**：
    - 把所有想得到的例子都验证过就当成证明了（正整数写成 18 个四次方之和，79 就是反例）

**★ 子目标（4 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **先确认要检查的实例数目足够少、真的能一个个列完** | `People can carry out exhaustive proofs when it is necessary to check only a relatively small number of instances of a statement.` |  |
| 2 | **把每个允许的取值当成一个情形，逐个验证结论都成立** | `An exhaustive proof is a special type of proof by cases where each case involves checking a single example.` |  |
| 3 | **先缩小候选范围、排除不可能的取值，再对剩下的少数情形逐一检查** | `We can quickly reduce a proof to checking just a few simple cases because x2 > 8 when |x| ≥3 and 3y2 > 8 when |y| ≥2. This leaves the cases when x equals −2, −1, 0, 1, or 2 and y equals −1, 0, or 1.` |  |
| 4 | **判断能不能穷举：无法列出全部实例时，再多计算机验证也算不上证明** | `Note that not even a computer can check all instances when it is impossible to list all instances to check.` |  |

### `s18__without_loss_of_generality` — 不失一般性（without loss of generality, WLOG）

- **类型**：程序性
- **出处**：rosen-c1.8-pdf0123
- **前置**：s18__proof_by_cases（分情形证明（proof by cases））
- **对比对象**：s18__proof_by_cases（分情形证明（proof by cases））
- **易错点**：
    - 对并不对称的情形也写「不失一般性」，把没证的情形当成「同理」，结果证明不完整
    - 把「不失一般性」理解成「只要证随便挑的一个特例」，说不出其余情形为什么能照样推出

**★ 子目标（3 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **只详细证一个情形，并说明其余情形做同样的改动就能得到** | `Implicit in this statement is that we can complete the case with x < 0 and y ≥0 using the same argument as we used for the case with x ≥0 and y < 0, but with the obvious changes.` |  |
| 2 | **写「不失一般性」时要能指出各情形之间靠什么互换互推，把理由交代清楚** | `(Note that our use of without loss of generality within the proof is justiﬁed because the proof when y is odd can be obtained by simply interchanging the roles of x and y in the proof we have given.)` |  |
| 3 | **检查情形之间是否真对称：某个情形差别很大时就不能略过它** | `Sometimes assumptions are made that lead to a loss in generality. Such assumptions can be made that do not take into account that one case may be substantially diﬀerent from others. This can lead to an incomplete, and possibly unsalvageable, proof.` |  |

### `s18__existence_proof` — 存在性证明（existence proof）

- **类型**：概念
- **出处**：rosen-c1.8-pdf0124
- **对比对象**：s18__uniqueness_proof（唯一性证明（uniqueness proof））
- **易错点**：
    - 认为没把那个元素具体算出来的证明不算证明（其实非构造性的存在性证明同样成立）

### `s18__constructive_existence_proof` — 构造性存在性证明（constructive existence proof）

- **类型**：程序性
- **出处**：rosen-c1.8-pdf0124、rosen-c1.8-pdf0131
- **前置**：s18__existence_proof（存在性证明（existence proof））
- **上位**：s18__existence_proof（存在性证明（existence proof））
- **对比对象**：s18__nonconstructive_existence_proof（非构造性存在性证明（nonconstructive existence proof））
- **易错点**：
    - 只算出或猜到某个候选对象，却不验证它满足所要求的性质，就宣布证明结束

**★ 子目标（2 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **找出一个具体的元素（见证元），并验证它满足所要求的性质** | `Sometimes an existence proof of ∃xP(x) can be given by ﬁnding an element a, called a witness, such that P(a) is true. This type of existence proof is called constructive.` |  |
| 2 | **把找到的对象摆出来并说明它符合要求，存在性就算证完** | `The existence of one such tiling completes a constructive existence proof.` |  |

### `s18__nonconstructive_existence_proof` — 非构造性存在性证明（nonconstructive existence proof）

- **类型**：程序性
- **出处**：rosen-c1.8-pdf0124、rosen-c1.8-pdf0125、rosen-c1.8-pdf0126
- **前置**：s18__existence_proof（存在性证明（existence proof））
- **上位**：s18__existence_proof（存在性证明（existence proof））
- **对比对象**：s18__constructive_existence_proof（构造性存在性证明（constructive existence proof））
- **易错点**：
    - 在非构造性证明里以为自己已经找到了那个元素（其实只证了必有一个）

**★ 子目标（3 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **不去找具体元素，改用别的方式证明存在性** | `It is also possible to give an existence proof that is nonconstructive; that is, we do not ﬁnd an element a such that P(a) is true, but rather prove that ∃xP(x) is true in some other way.` |  |
| 2 | **常用手段是用反证法：否定存在量化，推出矛盾** | `One common method of giving a nonconstructive existence proof is to use proof by contradiction and show that the negation of the existential quantiﬁcation implies a contradiction.` |  |
| 3 | **确认「只证存在、不指出是哪一个」也算完成证明** | `Note that we showed that a winning strategy exists, but we did not specify an actual winning strategy. Consequently, the proof is a nonconstructive existence proof.` |  |

### `s18__uniqueness_proof` — 唯一性证明（uniqueness proof）

- **类型**：程序性
- **出处**：rosen-c1.8-pdf0126、rosen-c1.8-pdf0127
- **前置**：s18__existence_proof（存在性证明（existence proof））
- **对比对象**：s18__existence_proof（存在性证明（existence proof））
- **易错点**：
    - 只证了唯一性（任意两个满足条件的对象相等）就宣布「存在唯一」，漏掉存在性这一半
    - 把「我找到了一个解」当成唯一性证明，没说明不会有第二个

**★ 子目标（3 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **存在性部分：先证明确实有一个元素满足所要求的性质** | `Existence: We show that an element x with the desired property exists.` |  |
| 2 | **唯一性部分：假设两个元素都满足性质，推出它们相等** | `Uniqueness: We show that if x and y both have the desired property, then x = y.` |  |
| 3 | **必要时把目标写成量词形式：存在一个满足性质、其余都不满足** | `Remark: Showing that there is a unique element x such that P(x) is the same as proving the statement ∃x(P(x) ∧∀y(y ≠x →¬P(y))).` |  |

### `s18__forward_reasoning` — 前向推理（forward reasoning）

- **类型**：程序性
- **出处**：rosen-c1.8-pdf0128
- **对比对象**：s18__backward_reasoning（逆向推理（backward reasoning））
- **易错点**：
    - 结论很复杂时硬着头皮从头往前推，写了很多步也到不了结论（这时应换逆向推理）

**★ 子目标（3 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **从前提出发，配合公理和已知定理一步步推向结论** | `To begin a direct proof of a conditional statement, you start with the premises. Using these premises, together with axioms and known theorems, you can construct a proof using a sequence of steps that leads to the conclusion. This type of reasoning, called forward reasoning, is the most common type of reasoning used to prove relatively simple results.` |  |
| 2 | **间接证明时换起点：从结论的否定出发，一步步推出前提的否定** | `Similarly, with indirect reasoning you can start with the negation of the conclusion and, using a sequence of steps, obtain the negation of the premises.` |  |
| 3 | **判断前向推理够不够用：结论复杂、路径看不出来时就要换方法** | `Unfortunately, forward reasoning is often diﬃcult to use to prove more complicated results, because the reasoning needed to reach the desired conclusion may be far from obvious.` |  |

### `s18__backward_reasoning` — 逆向推理（backward reasoning）

- **类型**：程序性
- **出处**：rosen-c1.8-pdf0128、rosen-c1.8-pdf0129
- **前置**：s18__forward_reasoning（前向推理（forward reasoning））
- **对比对象**：s18__forward_reasoning（前向推理（forward reasoning））
- **易错点**：
    - 从结论出发时把方向用反：拿「结论能推出的东西」成立来说明结论成立（循环论证/乞题）
    - 把逆向推理的草稿直接当正式证明交上去，没有倒过来写成前向证明

**★ 子目标（4 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **从要证的结论往回找：找一个已经能证明、且能推出结论的命题** | `In such cases it may be helpful to use backward reasoning. To reason backward to prove a statement q, we ﬁnd a statement p that we can prove with the property that p →q.` |  |
| 2 | **别把推出方向搞反：不能由结论推出来的东西成立反过来断定结论成立** | `(Note that it is not helpful to ﬁnd a statement r that you can prove such that q →r, because it is the fallacy of begging the question to conclude from q →r and r that q is true.)` |  |
| 3 | **把结论改写成一串彼此等价的式子，一直化到已知为真的式子** | `To prove that (x + y)∕2 > √xy when x and y are distinct positive real numbers, we can work backward. We construct a sequence of equivalent inequalities.` |  |
| 4 | **逆推只是找路：最后把步骤倒过来，用前向推理写出正式证明** | `Once we have carried out this backward reasoning, we can build a proof based on reversing the steps.` |  |

### `s18__adapting_existing_proofs` — 改造已有证明（adapting existing proofs）

- **类型**：程序性
- **出处**：rosen-c1.8-pdf0129
- **易错点**：
    - 碰到新定理完全从零开始，不去找结构相近的老定理和它的证明

**★ 子目标（3 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **先找结构相似的老结论，看它的证明能不能直接搬过来用** | `An excellent way to look for possible approaches that can be used to prove a statement is to take advantage of existing proofs of similar results.` |  |
| 2 | **整段搬不动时，至少借用老证明里的想法** | `Often an existing proof can be adapted to prove other facts. Even when this is not the case, some of the ideas used in existing proofs may be helpful.` |  |
| 3 | **照搬之后标出哪些步骤在新定理里还缺依据、需要另补工具** | `In turns out that we can, but we need some ammunition from number theory, which we will develop in Chapter 4. We sketch out the remainder of the proof, but leave the justiﬁcation of these steps until Chapter 4.` |  |

### `s18__counterexample_search` — 寻找反例（looking for counterexamples）

- **类型**：程序性
- **出处**：rosen-c1.8-pdf0130
- **对比对象**：s18__exhaustive_proof（穷举证明（exhaustive proof / proof by exhaustion））
- **易错点**：
    - 试了很多个小例子都成立就断言命题为真（正整数写成 18 个四次方之和，79 处就失败）

**★ 子目标（3 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **先尝试证明；证不出来就从最小的例子开始找反例；还找不到就回头继续证** | `When confronted with a conjecture, you might ﬁrst try to prove this conjecture, and if your attempts are unsuccessful, you might try to ﬁnd a counterexample, ﬁrst by looking at the simplest, smallest examples. If you cannot ﬁnd a counterexample, you might again try to prove the statement.` |  |
| 2 | **找反例的具体打法：把正整数按从小到大逐个代进去试** | `To look for a counterexample, we try to write successive positive integers as a sum of three squares.` |  |
| 3 | **找到可疑的对象后，把可能的取值限制住，证明它确实不满足命题** | `To show that there are not three squares that add up to 7, we note that the only possible squares we can use are those not exceeding 7, namely, 0, 1, and 4. Because no three terms where each term is 0, 1, or 4 add up to 7, it follows that 7 is a counterexample.` |  |

### `s18__checkerboard_tiling` — 棋盘与铺砌（checkerboard / board / domino / tiling）

- **类型**：概念
- **出处**：rosen-c1.8-pdf0131、rosen-c1.8-pdf0133
- **易错点**：
    - 只比较棋子数或格子数的奇偶就下结论：格子数是偶数只是必要条件，62 格的棋盘照样可能铺不出来

### `s18__coloring_argument` — 染色计数论证（coloring argument）

- **类型**：程序性
- **出处**：rosen-c1.8-pdf0132、rosen-c1.8-pdf0133
- **前置**：s18__checkerboard_tiling（棋盘与铺砌（checkerboard / board / domino / tiling））
- **易错点**：
    - 只数格子总数，忘了按颜色分别计数，于是看不出「每种颜色各需多少格」这个矛盾

**★ 子目标（6 步）**——依据 Morrison 等 2020：无反馈条件下**给标签**优于让学生自己生成；按 Catrambone 1995/1998，标签写**功能/目的**、不绑符号。

| # | 子目标标签 | 课件原文对应 | 这一步在做什么 |
|---|---|---|---|
| 1 | **把棋盘交替染色，并观察每块骨牌覆盖各种颜色各几个** | `We color the squares of this checkerboard using alternating white and black squares, as in Figure 2. Observe that a domino in a tiling of such a board covers one white square and one black square.` |  |
| 2 | **由「每块骨牌覆盖一黑一白」算出整块棋盘要铺满必须有多少黑格、多少白格** | `Note that each domino in this tiling covers one white and one black square. Consequently, the tiling covers 31 white squares and 31 black squares.` |  |
| 3 | **假设铺砌存在，推出它与染色计数矛盾，从而否定存在性** | `We can use these observations to prove by contradiction that a standard checkerboard with opposite corners removed cannot be tiled using dominoes.` |  |
| 4 | **换骨牌类型就换颜色数：用三格骨牌时改成三色染色** | `Because we are using straight triominoes rather than dominoes, we color the squares using three colors rather than two colors` |  |
| 5 | **观察每块三格骨牌覆盖三种颜色各一个** | `Next, we make the crucial observation that when a straight triomino covers three squares of the checkerboard, it covers one blue square, one black square, and one white square.` |  |
| 6 | **用旋转对称把缺格统一成同一种颜色，减少要讨论的情形** | `Thus, without loss of generality, we may assume that we have rotated the coloring so that the missing square is colored blue.` |  |

### `s18__open_problems` — 未解决问题与猜想（open problems）

- **类型**：概念
- **出处**：rosen-c1.8-pdf0134、rosen-c1.8-pdf0135
- **易错点**：
    - 把「已经被计算机验证到很大范围」当成「已经证明」（3x + 1 猜想验到 5.48 ⋅1018 仍未证明）
