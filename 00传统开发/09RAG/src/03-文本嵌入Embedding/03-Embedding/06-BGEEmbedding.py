"""
开源 Embedding 模型, 对于很多企业的实际情况:
    不能使用 OpenAI
    不能数据出境
    需要私有化部署
    需要离线部署
所以国内 最常见的选择之一就是 BGE

什么是 BGE
BGE 与 OpenAI Embedding 区别
SentenceTransformer 使用
本地Embedding生成
BGE‑M3了解

------
uv add sentence-transformers==5.5.1
uv add torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
uv add numpy

sentence-transformers：加载和调用 Embedding 模型的封装库
torch：底层深度学习框架（这里装的是 CPU 版）
numpy：向量运算、余弦相似度计算
"""
# 从sentence_transformers导入SentenceTransformer，用来加载本地开源语义向量模型
from sentence_transformers import SentenceTransformer
# 导入numpy，用于向量运算、计算余弦相似度
import numpy as np

import os
# 设置 Hugging Face 的缓存根目录
os.environ["HF_HOME"] = r"./huggingface"
# 国内镜像
os.environ['HF_ENDPOINT'] = r"https://hf-mirror.com"
# 代码本质就是一个最小的 RAG 召回系统   步骤逻辑 加载模型 → 单条向量化 → 封装函数 → 批量向量化→ 定义相似度 → 构建内存向量库 → 检索函数 → 召回上下文 → 测试

# --------------------------1.加载BGE本地向量化模型--------------------------
# 加载bge‑large‑zh‑v1.5中文向量模型 它是北京智元的中文 BGE 大模型 输出1024维；
# 第一次执行会自动从huggingface下载模型文件(约1G多)之后就从本地缓存加载，完全离线，
# 这一步是整个方案"私有化"的关键：模型在本地，不调外网 API
model = SentenceTransformer('BAAI/bge-large-zh-v1.5')
# 在控制台打印提示，确认模型已经加载完成
print('模型加载成功')

# --------------------------2.单条文本生成Embedding--------------------------
# 准备测试文本：用户提问
text = '如何申请退款'
# 使用本地模型encode方法，把文本转为向量，不需要调用外网api
embedding = model.encode(text)
# 打印生成出来的向量
print(f'Embedding生成成功 {embedding}')
# len查看向量的维度，bge‑large‑zh‑v1.5输出维度是1024
print(f'维度 {len(embedding)}')

# --------------------------3.封装获取向量的函数--------------------------
# 封装函数：输入一段文本，返回本地模型生成的embedding向量
def get_embedding(text):
    return model.encode(text)

# --------------------------4.批量测试多条知识库文本向量化--------------------------
# 模拟FAQ知识库文本列表
texts = [
    '退款流程说明',
    '订单取消流程',
    '售后服务规范'
]
# 循环遍历每一条知识库文本，调用函数生成向量并打印
for t in texts:
    embedding = get_embedding(t)
    print(t, embedding)

# --------------------------5.定义余弦相似度计算函数--------------------------
def cosine_similarity(vec1, vec2):
    # 将输入向量转为numpy数组，方便后续矩阵运算
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    # 余弦相似度公式：向量点积除以两个向量模长的乘积
    # 值越靠近1代表语义越相似；越靠近‑1语义差距越大
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


# --------------------------6.构造FAQ知识库，构建内存版本地向量库（参考前面openai版本RAG）--------------------------
# 模拟企业FAQ知识库
faq_docs = [
    '退款流程说明',
    '订单取消流程',
    '售后服务规范',
    '物流查询方式'
]

# 初始化内存向量数据库，使用python列表模拟
vector_db = []
# 循环遍历知识库，逐条生成向量存入内存库
for faq_doc in faq_docs:
    emb = get_embedding(faq_doc)    # 使用本地BGE模型生成知识库文本向量
    vector_db.append({
        'text': faq_doc,
        'embedding': emb
    })

# --------------------------7.实现检索函数search：根据用户query检索知识库--------------------------
def search(query, top_k=3):
    """
    :param query: 用户输入查询问题
    :param top_k: 返回相似度最高前k条
    :return: 排序之后的召回结果列表
    """
    # 用户提问先通过本地模型转为向量
    query_emb = get_embedding(query)
    results = []
    # 遍历内存向量库，逐条计算和用户query之间的余弦相似度
    for item in vector_db:
        score = cosine_similarity(query_emb, item['embedding'])
        results.append({
            'text': item['text'],
            'score': score
        })
    # 按照相似度分数降序排序，分数高排在前面
    results.sort(key=lambda x: x['score'], reverse=True)
    # 返回top_k条召回结果
    return results[:top_k]

# --------------------------8.retrieve召回知识上下文函数--------------------------
def retrieve(query):
    """根据用户问题检索知识库，拼接多条召回文本作为上下文"""
    docs = search(query, top_k=3)
    context = '\n'.join([doc['text'] for doc in docs])
    return context

# --------------------------9.测试检索效果（私有化本地Embedding完成召回；后面可对接开源大模型完成RAG生成）--------------------------
query = '订单怎么退款？'
# 执行知识召回
context = retrieve(query)
# 打印召回出来的上下文
print("====召回的知识库上下文====")
print(context)

# 打印检索返回每一条知识以及相似度得分
res_list = search(query)
print("====检索得分结果====")
for r in res_list:
    print(r['text'], " 相似度得分：", r['score'])

"""
后续RAG流程说明：
当前只用BGE完成【本地离线召回】；
如果要完整私有化RAG，还需要接入本地开源大模型(如Qwen‑7B等)，组装prompt，完成答案生成；
对比OpenAI版本RAG区别：
✅全部离线运行；✅数据不会出境；适合内网企业部署；
⚠️缺点：本地需要GPU/较好CPU资源；首次下载模型占用磁盘空间。
"""