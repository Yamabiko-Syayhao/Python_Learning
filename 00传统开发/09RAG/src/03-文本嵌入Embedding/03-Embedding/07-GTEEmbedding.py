"""
GTE 是 General Text Embedding
阿里巴巴达摩院推出的
专门用于语义检索 RAG 向量检索
代表模型:  gte‑small  gte‑base gte‑large gte‑qwen2
"""
# 从sentence_transformers导入SentenceTransformer，用来加载本地开源语义向量模型
from sentence_transformers import SentenceTransformer
from modelscope import snapshot_download
# --------------------------1.加载GTE本地向量化模型--------------------------
# snapshot_download 是魔搭社区提供下载模型函数
model_dir = snapshot_download('AI-ModelScope/gte-base-zh')
# 加载gte‑base‑zh中文向量模型；AI‑ModelScope代表魔搭社区模型仓库
# 第一次运行程序会自动下载模型文件(约1GB+)，网速慢需要等待
model = SentenceTransformer(model_dir)
# 控制台打印提示信息，确认模型已经加载完毕
print('模型加载成功')

# huggingface下载
# model = SentenceTransformer('thenlper/gte-base-zh')

# --------------------------2.单条文本生成Embedding向量--------------------------
# 准备测试文本：用户的咨询提问
text = '如何申请退款'
# 使用本地模型encode直接把中文文本转为语义向量；GTE不需要额外添加指令前缀
embedding = model.encode(text)
# 打印生成后的向量数组
print(f'Embedding生成成功 {embedding}')
# 打印向量维度；gte‑base‑zh输出维度是768
print(f'维度 {len(embedding)}')

"""
BGE 和 GTE的区别
BGE 用户提问  知识库段落
用户问题 必须加指令前缀   不加前缀会导致召回效果大幅降低
举例:   为这个句子生成表示以用于检索相关文章: 如何申请退款
一般的知识库段落不需要加指令前缀
擅长场景:RAG知识库检索,FAQ问答/长段落匹配

GTE 不需要指令前缀的,用户问题和知识库文档,直接编码
擅长场景:文本聚类/语义相似度/电商搜索/复杂中文理解
"""

# --------------------------3.封装获取向量的函数--------------------------
def get_embedding(text):
    # GTE直接encode，不用额外拼接检索指令
    return model.encode(text)

# --------------------------4.余弦相似度函数--------------------------
import numpy as np
def cosine_similarity(vec1, vec2):
    # 将list转为numpy数组用于向量运算
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    # 余弦相似度公式：点积除以两个向量模的乘积；越靠近1语义越相似
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# --------------------------5.构建内存版向量库 + 检索（模仿前面RAG案例补全）--------------------------
# FAQ知识库，模拟商城客服知识库
faq_docs = [
    '退款流程说明',
    '订单取消流程',
    '售后服务规范',
    '物流查询方式'
]

vector_db = []
# 循环知识库文本生成向量存入内存向量库
for faq_doc in faq_docs:
    emb = get_embedding(faq_doc)
    vector_db.append({
        'text': faq_doc,
        'embedding': emb
    })

# --------------------------6.检索函数search--------------------------
def search(query, top_k=3):
    """
    :param query: 用户提问
    :param top_k: 返回相似度最高的前N条
    :return: 排序后的召回结果列表
    """
    query_emb = get_embedding(query)   # GTE直接对原始提问编码，不需要加检索指令！
    results = []
    for item in vector_db:
        score = cosine_similarity(query_emb, item['embedding'])
        results.append({
            'text': item['text'],
            'score': score
        })
    # 相似度降序排序，分数高排在前面
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:top_k]

# --------------------------7.测试检索效果--------------------------
query = '订单怎么退款？'
res_list = search(query)
print("--------------------------------")
for r in res_list:
    print(r['text'], "相似度得分：", r['score'])

def retrieve(query):
    """知识召回，拼接上下文文本，供给后面大模型做RAG"""
    docs = search(query, top_k=3)
    context = '\n'.join([doc['text'] for doc in docs])
    return context

context = retrieve(query)
print("\n====召回上下文====")
print(context)