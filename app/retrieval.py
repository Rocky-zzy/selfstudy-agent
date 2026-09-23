# -*- coding: utf-8 -*-
"""关键词检索层（最小实现）。

性质（见 docs/00_错题本.md §四）：**通用技术实现，不是评估构念**。
它不主张任何"教学有效性"；基线与优化两个条件共用同一个检索器，
因此检索质量不构成两组之间的差异来源。

设计约束来自 knowledge_base/README.md：一页一个 chunk，来源可追溯到「哪个文件第几页」。
本模块不做语义分块、不引入向量模型——那是后续再议的话题。
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KB_PATH = ROOT / "knowledge_base" / "chunks.jsonl"

# 英文停用词（只列常见功能词；数学术语一律保留）
_STOP = {
    "the", "a", "an", "of", "is", "are", "was", "were", "be", "been", "to", "in", "on",
    "at", "for", "and", "or", "not", "with", "as", "by", "from", "that", "this", "these",
    "those", "it", "its", "we", "you", "i", "he", "she", "they", "them", "his", "her",
    "do", "does", "did", "can", "could", "should", "would", "will", "shall", "may",
    "might", "must", "have", "has", "had", "but", "if", "then", "than", "so", "such",
    "what", "which", "who", "whom", "how", "why", "when", "where", "there", "here",
    "please", "explain", "tell", "me", "about", "want", "know", "help", "understand",
    "请问", "什么", "怎么", "如何", "为什么", "讲解", "解释", "一下", "这个", "那个",
    "我", "你", "的", "是", "了", "吗", "呢", "和", "与", "或", "在", "有", "不",
}

# 中文技术词 -> 课件里的英文等价词（课件是英文的，用户可能用中文提问）
_ZH2EN = {
    "向量空间": ["vector", "space"],
    "线性空间": ["vector", "space"],
    "线性组合": ["linear", "combination"],
    "线性相关": ["linearly", "dependent"],
    "线性无关": ["linearly", "independent"],
    "线性映射": ["linear", "mapping"],
    "线性变换": ["linear", "transformation"],
    "仿射空间": ["affine", "space"],
    "仿射映射": ["affine", "mapping"],
    "仿射子空间": ["affine", "subspace"],
    "张成": ["span", "spanning"],
    "生成集": ["spanning", "generating"],
    "基": ["basis"],
    "基变换": ["basis", "change"],
    "秩": ["rank"],
    "核": ["kernel", "null", "space"],
    "零空间": ["null", "space"],
    "像": ["image", "column", "space"],
    "列空间": ["column", "space"],
    "子空间": ["subspace"],
    "维数": ["dimension", "dimensional"],
    "降维": ["dimensionality", "reduction", "downsampling"],
    "升维": ["upsampling", "higher", "dimensional"],
    "交换图": ["diagram"],
    "变换矩阵": ["transformation", "matrix"],
    "矩阵": ["matrix", "matrices"],
    "等价": ["equivalent"],
    "相似": ["similar"],
    "平移": ["translation"],
    "支撑点": ["support", "point"],
    "方向空间": ["direction", "space"],
    "阿贝尔群": ["abelian", "group"],
    "群": ["group"],
    "分配律": ["distributivity"],
    "例题": ["exercise", "example"],
    "习题": ["exercise"],
    "定义": ["definition", "def"],
    "证明": ["prove", "proof"],
    "反例": ["counterexample", "example"],
}

_TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z\-']*|\d+")
_CJK_RE = re.compile(r"[\u4e00-\u9fff]+")

# 中文功能字：单独出现或构成 bigram 时都算噪声（「什么是仿射空间」→ 不应切出「么是／它和」）
_CJK_STOP_CHARS = set("的了吗呢和与或在是有不我你他她它们个这那些什么怎如何为对给把被从到就也都很更最")


@dataclass
class Chunk:
    chunk_id: str
    lecture: str | None
    lecture_title: str
    page: int
    text: str
    extraction: str
    source_file: str
    score: float = 0.0
    matched: tuple[str, ...] = ()

    def to_dict(self) -> dict:
        return {
            "chunk_id": self.chunk_id,
            "lecture": self.lecture,
            "lecture_title": self.lecture_title,
            "page": self.page,
            "extraction": self.extraction,
            "source_file": self.source_file,
            "score": round(self.score, 3),
            "matched": list(self.matched),
        }


def list_lectures(chunks: list[Chunk]) -> list[dict]:
    """列出可选的"讲"（不同素材范围不同），供 UI 动态填充下拉框。

    避免把某份课件的讲次写死在模板里——换素材时 UI 要跟着变。
    """
    agg: dict[str, dict] = {}
    for c in chunks:
        key = c.lecture or ""
        a = agg.setdefault(
            key,
            {"lecture": c.lecture, "lecture_title": c.lecture_title, "pages": 0, "chars": 0},
        )
        a["pages"] += 1
        a["chars"] += len(c.text or "")
    return sorted(agg.values(), key=lambda x: (x["lecture"] is None, x["lecture"] or ""))


def load_chunks(kb_path: Path | None = None) -> list[Chunk]:
    """读取一行一个 chunk 的 jsonl。

    kb_path 为 None 时读 `knowledge_base/chunks.jsonl`。
    临时素材（如 `temp_material/ml1/chunks.jsonl`）走同一套读取逻辑，
    但**物理隔离在 knowledge_base 之外**——用户明确要求临时样本不进知识库。
    """
    kb_path = Path(kb_path) if kb_path else KB_PATH
    if not kb_path.exists():
        raise FileNotFoundError(f"知识库不存在：{kb_path}")
    out: list[Chunk] = []
    with kb_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            out.append(
                Chunk(
                    chunk_id=r["chunk_id"],
                    lecture=r.get("lecture"),
                    lecture_title=r.get("lecture_title") or "",
                    page=int(r["page"]),
                    text=r.get("text") or "",
                    extraction=r.get("extraction") or "",
                    source_file=r.get("source_file") or "",
                )
            )
    return out


def tokenize(query: str) -> list[str]:
    """查询 -> 检索词。英文取词、中文先查术语表再降级为单字/双字。"""
    tokens: list[str] = []
    # 1) 中文技术词优先映射（长词优先，避免"空间"覆盖"仿射空间"）
    for zh in sorted(_ZH2EN, key=len, reverse=True):
        if zh in query:
            tokens.extend(_ZH2EN[zh])
    # 2) 英文与数字
    tokens.extend(t.lower() for t in _TOKEN_RE.findall(query))
    # 3) 未被术语表覆盖的汉字串：切成 2-gram（对中文提问的兜底）
    for run in _CJK_RE.findall(query):
        rest = run
        for zh in sorted(_ZH2EN, key=len, reverse=True):
            rest = rest.replace(zh, " ")
        for piece in rest.split():
            if len(piece) == 1:
                if piece not in _CJK_STOP_CHARS:
                    tokens.append(piece)
            else:
                # 只保留"整段都是实词"的 bigram：含中文功能字的碎片一律丢弃，
                # 否则「什么是仿射空间」会被切出「么是／它和／差在」这类噪声词，
                # 污染"命中依据"的展示。
                for i in range(len(piece) - 1):
                    bg = piece[i : i + 2]
                    if any(ch in _CJK_STOP_CHARS for ch in bg):
                        continue
                    tokens.append(bg)
    out: list[str] = []
    for t in tokens:
        if not t or t in _STOP:
            continue
        if t not in out:
            out.append(t)
    return out


def score_chunks(chunks: list[Chunk], terms: list[str], page_texts: dict[str, str]) -> None:
    """就地写入 score / matched。经典 tf-idf 加权，外加原词命中加成。

    通用检索技术，不涉及教学主张。为了让"哪一页被召回"可解释，
    同时记录命中的检索词，UI 会显示出来。
    """
    n_docs = max(len(chunks), 1)
    df = {t: 0 for t in terms}
    for t in terms:
        for c in chunks:
            if t in page_texts[c.chunk_id]:
                df[t] += 1
    for c in chunks:
        low = page_texts[c.chunk_id]
        s = 0.0
        matched: list[str] = []
        for t in terms:
            tf = low.count(t)
            if tf <= 0:
                continue
            idf = math.log((n_docs + 1) / (df[t] + 1)) + 1.0
            s += (1.0 + math.log(tf)) * idf
            matched.append(t)
        c.score = s
        c.matched = tuple(matched)


def search(
    query: str,
    chunks: list[Chunk],
    lecture: str | None = "L01",
    top_k: int = 3,
    bridge: bool = True,
    max_pages: int | None = None,
    whole_lecture: bool = False,
    whole_lecture_char_limit: int | None = 20000,
    page_range: tuple[int, int] | None = None,
) -> list[Chunk]:
    """检索与 query 最相关的 chunk。

    参数
    ----
    lecture      : 只在该讲内检索（None = 全库）。起步按 HANDOFF 定调先做 Lecture 1。
    top_k        : 直接命中的页数上限。
    bridge       : 是否补"桥接页"——只有当命中页之间**真的断开**（如 p1 与 p4 之间缺 p2、p3）时才补，
                   保证前置定义不被切断；命中页本来相邻则一页都不多补。
    max_pages    : 最终喂给模型的页数上限（None → top_k + 2）。防止一个宽泛问题
                   把整讲捞回来，使"检索"名存实亡、prompt 成本无声膨胀。
    whole_lecture: 直接给整讲。**起步阶段的默认**。

    为什么起步要默认给整讲（实测理由，不是偏好）：
    对「什么是仿射空间」这个问题，纯词面检索命中的是 p2/p3/p4/p5/p7，**漏掉 p8**。
    而 p8 是全讲唯一给出「仿射映射」定义的一页——它只有 282 字符、且不含
    "affine space" 字样，所以词面匹配不到。结果是：**问了某个概念，恰好漏掉讲这个概念的那一页**。
    Lecture 1 全讲仅 8 页 / 13,008 字符，整讲直灌成本可控；
    且两条件共用同一份原文，对比仍然成立。若将来要单独研究"检索"这个变量，
    再打开命中页模式（`whole_lecture=False`）单独评估。

    返回按页码排序的 chunk 列表（便于按讲解顺序喂给模型）。
    """
    pool = [c for c in chunks if lecture is None or c.lecture == lecture]
    if page_range:
        # 分区（如 Machine Learning I 的 "NumPy / SciPy / Pandas …"）本质就是页区间。
        # 不为此另造一套切分逻辑——只是在既有检索之前先按页收窄。
        lo, hi = page_range
        pool = [c for c in pool if lo <= c.page <= hi]
    if not pool:
        raise ValueError(f"知识库里没有 lecture={lecture!r} page_range={page_range} 的 chunk")

    total_chars = sum(len(c.text or "") for c in pool)
    whole = whole_lecture
    if whole and whole_lecture_char_limit and total_chars > whole_lecture_char_limit:
        # 「整讲」在 AIAA 2711 上只要 13k 字符，但课件这种东西可能只有"一整讲"，
        # 比如 Machine Learning I.pptx 共 83 页 / 23.8k 字符——整份直灌会
        # 把上下文和成本一起撑大。超过上限就退回命中页 + 桥接，
        # 并且**必须把这件事报出去**，不能静默降级。
        whole = False

    if max_pages is None:
        max_pages = top_k + 2
    max_pages = max(1, min(max_pages, len(pool)))

    # 先算分：即使整讲直灌，"哪几页跟这个问题对上了"也是用户读的时候最需要的信息
    page_texts = {c.chunk_id: c.text.lower() for c in pool}
    terms = tokenize(query)
    score_chunks(pool, terms, page_texts)

    if whole:
        return sorted(pool, key=lambda c: c.page)

    ranked = sorted(pool, key=lambda c: (-c.score, c.page))
    # 命中页不得超过 max_pages（否则一个宽泛问题会把整讲都标成"命中"，
    # 弱命中挤占桥接位，检索就名存实亡了）
    hits = [c for c in ranked[:top_k] if c.score > 0][:max_pages]
    if not hits:
        # 一个检索词都没命中：退化为给该讲最前面的若干页，避免返回空
        hits = ranked[: min(top_k, max_pages)]

    # 按**位置**索引而不是按页码：page_range 收窄后页码可能不连续
    idx_of = {id(c): i for i, c in enumerate(pool)}
    hit_idx = [idx_of[id(c)] for c in hits]
    keep: set[int] = set(hit_idx)

    if bridge:
        # 桥接补的是"命中之间"的缺页（按 pool 内部位置），且总量受 max_pages 约束
        for lo, hi in zip(sorted(hit_idx), sorted(hit_idx)[1:]):
            for i in range(lo + 1, hi):
                if len(keep) >= max_pages:
                    break
                keep.add(i)
            if len(keep) >= max_pages:
                break

    selected = [pool[i] for i in sorted(keep)]
    if len(selected) > max_pages:
        # 命中页按得分优先保留，其余丢弃
        rank_of = {id(c): i for i, c in enumerate(ranked)}
        selected = sorted(
            sorted(selected, key=lambda c: rank_of.get(id(c), 10**6))[:max_pages],
            key=lambda c: c.page,
        )
    # 命中页保留得分用于展示；桥接页得分保持 0，UI 上可区分
    return selected


def build_context(selected: list[Chunk]) -> str:
    """把选中的页拼成给模型的课件原文（整页，不删改内容）。

    这个函数是「基线 = 纯 LLM + 整页课件原文直灌」里"直灌"的实现：
    **不做摘要、不做改写、不挑句子**，只加来源标记。
    """
    parts = []
    for c in selected:
        parts.append(
            f"<<<PAGE {c.chunk_id} | {c.lecture_title} | page {c.page}>>>\n{c.text.strip()}"
        )
    return "\n\n".join(parts)
