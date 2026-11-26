"""
============================================================
Embedding 评测平台
============================================================
用途：给 Embedding 模型"打分"，回答"这个模型在我的业务上好不好用"
结构：配置 → 数据 → 检索链路 → 效果指标 → 工程指标 → 汇总报告
============================================================

"""

# ==================== 一、环境与配置 ====================
# 导入操作系统模块，读取环境变量
import os
# 导入时间模块
import time
# 导入numpy，用于向量运算、相似度计算
import numpy as np
# 导入openai客户端，用于兼容方式调用dashscope向量接口
from openai import OpenAI
# dotenv用于加载.env环境配置文件
from dotenv import load_dotenv
# 加载环境变量；override=True覆盖系统已有同名环境变量；verbose=True打印加载详情
load_dotenv(override=True, verbose=True)


# --- 模型配置（改这里就能换模型）---
EMBEDDING_MODEL = "qwen3.7-text-embedding-flash"   # 可换 text-embedding-v3 / BGE 等

# --- API 客户端（OpenAI 兼容协议对接 DashScope）---
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://ws-lb7fb82qnmqlboi9.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)


# ==================== 二、评测数据 ====================
# query：用户问句；answer：该问句对应的"标准正确文档"（可多条）
evaluation_data = [
    {"query": "订单怎么退款",   "answer": ["退款申请流程", "售后服务规范"]},
    {"query": "如何取消订单",   "answer": ["订单取消流程"]},
    {"query": "发票如何申请",   "answer": ["发票申请指南"]},
    {"query": "物流在哪里查看", "answer": ["物流查询方式"]},
    {"query": "售后怎么办",     "answer": ["售后服务规范"]},
]

# 知识库：所有候选文档，检索结果只能从这里出
documents = [
    "退款申请流程",
    "订单取消流程",
    "发票申请指南",
    "物流查询方式",
    "售后服务规范",
]


# ==================== 三、检索链路（先跑通） ====================

def get_embedding(text):
    """文本 → 向量"""
    resp = client.embeddings.create(input=text, model=EMBEDDING_MODEL)
    return resp.data[0].embedding


def cosine_similarity(vec1, vec2):
    """余弦相似度：值越接近 1，语义越像"""
    v1, v2 = np.array(vec1), np.array(vec2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


# --- 建库：把所有候选文档向量化，存进内存 ---
vector_db = [
    {"text": doc, "embedding": get_embedding(doc)}
    for doc in documents
]


def retriever(query, top_k=3):
    """
    检索：query 向量化 → 和库里每条算相似度 → 排序 → 取 Top-K
    返回：[{"text": 文档, "score": 相似度}, ...]
    """
    query_emb = get_embedding(query)
    results = [
        {"text": item["text"], "score": cosine_similarity(query_emb, item["embedding"])}
        for item in vector_db
    ]
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


# ==================== 四、效果指标（从粗到细） ====================

def hit_rate(dataset, k=3):
    """
    HitRate@K —— 有没有命中？
    每个 query 看 Top-K 里有没有至少 1 条正确文档：有=1，没有=0
    最终 = 命中样本数 / 总样本数
    """
    hits = 0
    for sample in dataset:  # 遍历每个测试样本
        gold = set(sample["answer"])  # 标准答案（可能多条），转成集合 集合才能做交集运算
        got = {r["text"] for r in retriever(sample["query"], k)}  #检索返回的Top-K文档文本，转成集合
        if gold & got:  # 集合交集非空 → 命中
            hits += 1
    return hits / len(dataset)  # 命中数 / 总数


def recall_at_k(dataset, k=3):
    """
    Recall@K —— 该找的找到多少？（漏没漏）
    单样本 = 命中的正确文档数 / 该 query 全部正确文档数
    最终 = 所有样本取平均
    """
    recalls = []
    for sample in dataset:
        gold = set(sample["answer"])
        got = {r["text"] for r in retriever(sample["query"], k)}
        recalls.append(len(gold & got) / len(gold)) # 命中了几个 / 应该命中几个
    return sum(recalls) / len(recalls)


def precision_at_k(dataset, k=3):
    """
    Precision@K —— 返回的 K 条里，几条是对的？（混没混噪声）
    单样本 = 命中的正确文档数 / K
    最终 = 所有样本取平均
    """
    precisions = []
    for sample in dataset:
        gold = set(sample["answer"])
        got = {r["text"] for r in retriever(sample["query"], k)}
        precisions.append(len(gold & got) / k)
    return sum(precisions) / len(precisions)


def mrr_score(dataset, k=3):
    """
    MRR —— 第一个正确文档排第几？
    排第 1 得 1 分，排第 2 得 1/2，排第 3 得 1/3，没命中得 0
    最终 = 所有样本取平均
    """
    scores = []
    for sample in dataset:
        gold = set(sample["answer"])
        rank = None
        for i, r in enumerate(retriever(sample["query"], k), start=1):
            if r["text"] in gold: # 找到第一个正确的就记下名次并立即跳出（只关心第一个）；
                rank = i
                break
        scores.append(1 / rank if rank else 0)
    return sum(scores) / len(scores)


def ndcg_at_k(dataset, k=3):
    """
    NDCG@K —— 整体排序合不合理？（对的越靠前分越高）
    DCG  = Σ (1 / log2(位置+1))，只对命中的位置累加
    IDCG = 理想排序（正确的全排最前）下的 DCG
    NDCG = DCG / IDCG，值域 [0,1]
    """
    ndcgs = []
    for sample in dataset:
        gold = set(sample["answer"])
        results = retriever(sample["query"], k)

        # 实际 DCG：命中位置加权 排第 1 得满分 1，排第 2 只拿 0.63，排第 3 拿 0.5——越靠前越值钱。
        dcg = sum(
            1 / np.log2(i + 1)
            for i, r in enumerate(results, start=1)
            if r["text"] in gold
        )
        # 理想 DCG：假设正确的都排最前
        ideal_hits = min(len(gold), k)
        idcg = sum(1 / np.log2(i + 1) for i in range(1, ideal_hits + 1))

        ndcgs.append(dcg / idcg if idcg > 0 else 0)
    return sum(ndcgs) / len(ndcgs)


# ==================== 五、工程指标 ====================

def benchmark_latency(query="订单怎么退款", runs=5):
    """
    Latency —— 检索快不快？（跑多次取平均，避免单次抖动）
    返回平均耗时（毫秒）
    """
    times = []
    for _ in range(runs):
        start = time.time()
        retriever(query, top_k=3)
        times.append((time.time() - start) * 1000)
    return sum(times) / len(times)


# ==================== 六、统一评测入口 ====================

def evaluate_all(dataset, k=3):
    """一键跑全部指标，返回字典"""
    return {
        f"HitRate@{k}":   hit_rate(dataset, k),
        f"Recall@{k}":    recall_at_k(dataset, k),
        f"Precision@{k}": precision_at_k(dataset, k),
        f"MRR@{k}":       mrr_score(dataset, k),
        f"NDCG@{k}":      ndcg_at_k(dataset, k),
        "Latency(ms)":    benchmark_latency(),
    }


def print_report(report, title="Embedding 评测报告"):
    """把字典打印成一张表"""
    print(f"\n{'='*40}")
    print(f"  {title}")
    print(f"{'='*40}")
    for name, val in report.items():
        print(f"  {name:15s}: {val:.4f}")
    print(f"{'='*40}\n")


# ==================== 七、运行 ====================

if __name__ == "__main__":
    report = evaluate_all(evaluation_data, k=3)
    print_report(report, title=f"模型：{EMBEDDING_MODEL}")