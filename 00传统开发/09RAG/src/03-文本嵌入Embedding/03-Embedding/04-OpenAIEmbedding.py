# 导入openai sdk客户端，用于访问openai的接口（embedding、chat大模型）
from openai import OpenAI
# 从dotenv导入环境变量加载工具，读取本地.env里面保存的OPENAI_API_KEY密钥
from dotenv import load_dotenv
# 加载环境变量；override=True 如果本机系统已有同名环境变量，则用.env文件的值覆盖
load_dotenv(override=True)
# 导入numpy数值计算库，后面用来计算余弦相似度
import numpy as np
import os
# ------------------- 1.初始化客户端 -------------------
# 创建OpenAI客户端实例，会自动读取环境变量里面的api‑key
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，各地域的URL不同。调用时请将{WorkspaceId}替换为真实的业务空间ID。
    base_url="https://ws-lb7fb82qnmqlboi9.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
# 可选向量模型：text‑embedding‑ada‑002、text‑embedding‑3‑small、text‑embedding‑3‑large
# 准备一段测试文本
text = "如何申请退款"

# ------------------- 2.向大模型提交文本 (这一步可以封装成一个函数,实现多次调用) -------------------
# 请求embedding接口，把文本变成向量
resp = client.embeddings.create(
    model="text-embedding-v1",   # 指定使用的向量模型
    input=text,                       # 需要向量化的输入文本
)

# -------------------3.拿到向量化之后的数据 -------------------
# 取出返回结果里面第一条的embedding向量（浮点数数组）
embedding = resp.data[0].embedding
# print(f"向量化：{embedding}")
# -------------------4.计算相似度：余弦相似度函数 -------------------
def cosine_similarity(vec1, vec2):
    # np.dot：求两个向量的点积；np.linalg.norm：求向量的模长；余弦相似度=点积除以两个向量模的乘积
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


"""
企业场景:
    客服企业知识库
    FAQ （Frequently Asked Questions）中文通常译为“常见问题解答”或“常见问题”
    帮助中心
"""
# FAQ知识库文本列表，模拟企业知识库的几条知识
faq_docs = [
    '退款申请流程',
    '订单取消流程',
    '售后服务说明',
    '物流查询方式'
]

# 封装获取embedding向量的函数；输入文本，返回对应的embedding向量
def get_embedding(text):
    # 调用openai向量接口
    resp = client.embeddings.create(
        model="text-embedding-v1",
        input=text,
    )
    # 返回向量数组
    return resp.data[0].embedding


# -------------------1.构建简易内存向量库（没有用向量数据库，直接python列表模拟） -------------------
vector_db = []   # 初始化空列表，充当内存版向量库
# 循环遍历每一条faq知识库文本
for faq_doc in faq_docs:
    emb = get_embedding(faq_doc)               # 将知识库文本转为向量
    vector_db.append({                         # 保存原始文本+对应的向量到列表
        'text': faq_doc,
        'embedding': emb
    })


# -------------------2.实现检索器：根据用户query从内存知识库检索相似知识 -------------------
def search(query, top_k=3):
    """
    :param query: 用户问题
    :param top_k: 返回的数量
    :return: 返回相似度排序之后的top_k结果列表
    """
    # 先把用户提问转成向量
    query_emb = get_embedding(query)
    results = []   # 用来存放每条知识和对应的相似度得分

    # 循环遍历内存向量库里面每一条知识库记录
    for vec in vector_db:
        # 计算用户问题向量 和知识库向量之间的余弦相似度得分
        score = cosine_similarity(query_emb, vec['embedding'])
        # 将知识库原文以及相似度得分存入结果列表
        results.append({
            'text': vec['text'],
            'score': score
        })
    # 按照相似度得分降序排序，分数越高越靠前
    results.sort(key=lambda x: x['score'], reverse=True)
    # 返回相似度最高前top_k条结果
    return results[:top_k]


# -------------------3.测试检索，模拟用户提问 -------------------
# query = '订单怎么退款'
# query = '发的什么快递'
# query = '快递信息怎么查'
query = '快递信息怎么获取'
results = search(query)    #调用检索函数执行查询
print('--------------------------------')
# 遍历打印检索返回的知识文本以及相似度分数
for res in results:
    print(f"相似度分数：{res['text'], res['score']}")


# -------------------4.构建 mini 版的RAG -------------------
"""
用户问题 -> Embedding -> 检索 -> 知识库/上下文 -> LLM
"""
def retrieve(query):
    # 召回知识：调用search检索知识库，取出top3相关知识
    docs = search(query=query, top_k=3)
    # 使用换行符\n，把多条召回出来的知识库文本拼接成一段上下文context
    context = '\n'.join([doc['text'] for doc in docs])
    # 返回拼接完成的知识库上下文
    return context

# 用户的提问
query = '订单怎么退款?'
# 执行知识召回，拿到检索之后的知识库上下文
context = retrieve(query)
# print(context,"context")

# -------------------5.构建提示词prompt（把检索出来的知识塞给prompt，约束大模型基于知识库回答） -------------------
# f-string组装提示词，传入知识库上下文context和用户问题query

prompt = f"""
你是商城客服助手.
已知知识:  {context}
用户问题: {query}
请给予知识回答.
"""

# -------------------6.调用大模型chat接口（补充剩余代码 +注释） -------------------
# 使用chat.completions.create调用聊天模型，传入上面组装好的prompt，获取RAG生成答案
chat_resp = client.chat.completions.create(
    model="qwen3.8-flash",    # 指定聊天大模型
    messages=[
        {"role": "user", "content": prompt}
    ]
)
# 获取大模型输出回答
answer = chat_resp.choices[0].message.content
# 打印RAG最终生成的客服回答
print("RAG回答：\n", answer)