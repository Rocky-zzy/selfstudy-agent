# -*- coding: utf-8 -*-
r"""生成一轮 MQI 盲评样本：对同一批问题生成 A/B 两段讲解并存盘。

为什么要这个脚本（而不是手工点界面）：
    界面一次只出一个知识点，而 MQI 判分要的是**一批**样本。
    这里复用应用的 `/api/ask` 通路（test client），保证与界面走的是同一套逻辑。

产物（给评判者看的时候**必须抹掉 condition**，见 `--export`）：
    data/mqi/batches/<batch>/samples.json   含 condition（自己存档用）
    data/mqi/batches/<batch>/blind.json     抹掉 condition，给评判者

用法：
    python scripts/make_mqi_batch.py --batch r3                 # 生成
    python scripts/make_mqi_batch.py --batch r3 --export        # 导出盲评输入
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))

from demo_app import ROOT as APP_ROOT, flask_app, load_dotenv  # noqa: E402

# 问题集：跨讲、跨知识类型（概念 / 算法 / 公式），每种讲法各若干
QUESTIONS: list[tuple[str, str, str]] = [
    # (lecture, teaching, question)
    ("L01", "brief",    "L01 这一讲整体在讲什么？各部分是什么关系"),
    ("L01", "detailed", "向量空间的定义是什么？为什么需要它？"),
    ("L01", "detailed", "线性映射是什么？为什么说它保持向量空间的结构？"),
    ("L01", "detailed", "基变换的矩阵 T^{-1}A_φS 是怎么推出来的？"),
    ("L01", "detailed", "核（kernel）和像（image）分别是什么？为什么核是子空间？"),
    ("L01", "followup", "追问：仿射空间为什么一般不是向量空间？"),
    ("L01", "detailed", "仿射空间是什么？它和向量空间差在哪？"),
    ("L02", "brief",    "L02 范数、内积、正定性这一块主要讲了什么"),
    ("L04", "brief",    "L04 特征分解与 SVD 这一块主要讲了什么"),
    ("L04", "detailed", "特征分解和 SVD 的区别是什么？各自什么时候用？"),
    ("L05", "detailed", "梯度和方向导数是什么？为什么梯度指向最陡上升方向？"),
    ("L06", "brief",    "L06 反向传播与自动微分主要讲了什么"),
    ("L07", "detailed", "梯度下降是怎么工作的？为什么用学习率？"),
    ("L07", "detailed", "约束优化里的拉格朗日乘子为什么有效？"),
    ("L08", "brief",    "L08 概率与分布这一块主要讲了什么"),
    ("L09", "brief",    "L09 信息论这一讲主要讲了什么"),
    ("L09", "detailed", "熵和条件熵的定义是什么？为什么需要它们？"),
    ("L09", "detailed", "KL 散度是什么？它和交叉熵是什么关系？"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True, help="批次名，如 r3")
    ap.add_argument("--export", action="store_true", help="只从已有 samples 导出盲评输入")
    ap.add_argument("--sleep", type=float, default=0.3)
    args = ap.parse_args()

    out_dir = ROOT / "data" / "mqi" / "batches" / args.batch
    out_dir.mkdir(parents=True, exist_ok=True)
    samples_path = out_dir / "samples.json"
    blind_path = out_dir / "blind.json"

    if args.export:
        rows = json.loads(samples_path.read_text(encoding="utf-8"))
        # 过滤掉任一槽位为空的样本：生成时会有 API 失败的问（连接错误），
        # 那些问的两段都是空字符串。空文本没有可判的内容，混进去会让评判者
        # 判出 4 个"编码 3/4 = 0"的假样本，污染组间统计。（第一版漏了这一步。）
        usable = [r for r in rows
                  if all((r["answers"][s]["text"] or "").strip() for s in r["answers"])]
        dropped = len(rows) - len(usable)
        if dropped:
            print(f"⚠️ 跳过 {dropped} 个空答案样本（生成时失败）：")
            for r in rows:
                if not all((r["answers"][s]["text"] or "").strip() for s in r["answers"]):
                    print(f"     {r.get('lecture')} {r['question'][:44]}")
        rows = usable

        items, key = [], []
        for i, r in enumerate(rows):
            # answers 按**槽位**（A/B）存；conditions 是槽位→真实条件的映射
            # （生成时用 /api/reveal 取回的）。导出时把两个槽位随机重标为 X/Y，
            # 让评判者拿不到任何顺序线索。
            cond_of = r["conditions"]
            slots = list(cond_of)
            random.shuffle(slots)
            for j, slot in enumerate(slots):
                new_slot = "X" if j == 0 else "Y"
                iid = f"q{i:02d}{new_slot}"
                items.append({
                    "id": iid,
                    "question": r["question"],
                    "teaching": r["teaching"],
                    "text": r["answers"][slot]["text"],
                    # 存文本哈希：跨轮复用判定时用它校验"是同一段文本"。
                    # 只对 (question, condition) 不足以复用——两轮生成是不同文本。
                    "sha": hashlib.sha256(
                        (r["answers"][slot]["text"] or "").encode("utf-8")).hexdigest()[:16],
                })
                key.append({"id": iid, "condition": cond_of[slot], "sha": items[-1]["sha"],
                            "question": r["question"], "teaching": r["teaching"]})
        blind_path.write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
        (out_dir / "_key.json").write_text(
            json.dumps(key, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"导出 {len(items)} 条盲评输入（{len(rows)} 问 × 2）-> {blind_path}")
        print("字段只有 id/question/teaching/text：**无 condition、无 user_score**")
        return 0

    load_dotenv(ROOT / ".env")
    cli = flask_app.test_client()
    rows = []
    t0 = time.time()
    for i, (lec, teach, q) in enumerate(QUESTIONS, 1):
        r = cli.post("/api/ask", json={
            "question": q, "material": "kb", "lecture": lec,
            "whole_lecture": True, "teaching": teach, "top_k": 4,
        })
        d = r.get_json() or {}
        if d.get("error") or not d.get("answers"):
            print(f"[{i}/{len(QUESTIONS)}] FAIL {lec} {q[:30]} -> {d.get('error')}")
            continue
        rows.append({
            "lecture": lec, "teaching": teach, "question": q,
            "mode": d.get("mode"), "ctx_chars": d.get("ctx_chars"),
            # 槽位→条件的映射**不在 /api/ask 的响应里**（盲测要求），
            # 生成完这一轮后调 /api/reveal 取回来。这一轮到此结束，不影响盲测。
            "conditions": {
                slot: lab["condition"]
                for slot, lab in (cli.post("/api/reveal",
                                           json={"trace_id": d["trace_id"]}).get_json() or {}
                                  ).get("labels", {}).items()
            },
            "answers": {
                s: {"text": a["text"], "chars": a["chars"],
                    "finish": a.get("finish_reason"), "truncated": a.get("truncated")}
                for s, a in d["answers"].items()
            },
        })
        # 注意：这一问在**两轮生成里都失败**过（空答案）。空答案的判定没有意义，
        # 而且会被跨轮合并脚本误配到别的文本上（已经踩过）。
        # 所以这里显式标出来，导出时会跳过。
        row = rows[-1]
        row["empty"] = [s for s, a in row["answers"].items() if not (a["text"] or "").strip()]
        a, b = d["answers"]["A"], d["answers"]["B"]
        print(f"[{i}/{len(QUESTIONS)}] {lec} {teach:<8} {q[:26]:<28} "
              f"A={a['chars']:>5}字 B={b['chars']:>5}字 finish={a.get('finish_reason')}/"
              f"{b.get('finish_reason')}")
        time.sleep(args.sleep)

    samples_path.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print()
    print(f"写入 {samples_path}（{len(rows)} 问，耗时 {time.time()-t0:.0f}s）")
    tr = [r for r in rows for s in ("A", "B") if r["answers"][s].get("truncated")]
    if tr:
        print(f"⚠️ {len(tr)} 段被截断，读判定时要排除")
    print(f"下一步：python scripts/make_mqi_batch.py --batch {args.batch} --export")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
