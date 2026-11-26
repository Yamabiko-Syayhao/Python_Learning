# 从dotenv导入环境变量加载工具，读取.env配置文件
from dotenv import load_dotenv
# 导入OpenAI SDK，这里用来做兼容调用通义千问接口（openai兼容模式）
from openai import OpenAI
import os
# 加载.env环境变量；override=True：如果系统已有同名环境变量，使用文件里面的值覆盖
load_dotenv(override=True)
# 导入numpy，用于向量运算以及计算余弦相似度
import numpy as np
# -------------------1.初始化客户端-------------------
# openai兼容模式访问dashscope；不用dashscope原生sdk，复用openai调用格式
client = OpenAI(
    base_url="https://ws-lb7fb82qnmqlboi9.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",   # 指定阿里云通义千问兼容接口地址
    api_key=os.getenv("DASHSCOPE_API_KEY"),
)
# 指定使用的向量模型名称：通义的text‑embedding‑v3
MODEL_NAME = "text-embedding-v1"
# 准备一条测试文本
text = "如何申请退款"

# -------------------1.1 原生dashscope客户端演示（仅做对比，本段后面代码没有使用resp1）-------------------
# 导入dashscope原生sdk
import dashscope
# 使用dashscope原生方式调用向量接口，和上面openai兼容模式是两种不同调用写法
resp1 = dashscope.TextEmbedding.call(
    model=MODEL_NAME,
    input=text
)

# -------------------2.向大模型提交文本（openai兼容方式调用向量接口）-------------------
# 通过openai风格的接口请求embedding，把文本转为向量
resp = client.embeddings.create(
    model=MODEL_NAME,    # 指定通义的向量模型
    input=text,          # 需要向量化的输入文本
)

# -------------------3.拿到向量化之后的数据-------------------
# 从返回结果提取向量数组（浮点数列表）
embedding = resp.data[0].embedding

# -------------------4.定义余弦相似度计算函数-------------------
def cosine_similarity(vec1, vec2):
    # 余弦相似度公式：两个向量点积 ÷ (vec1模长 * vec2模长)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


"""
企业场景:
    客服企业知识库
    FAQ
    帮助中心
"""
# 模拟FAQ知识库，商城客服的几条问答知识点
faq_docs = [
    '退款申请流程',
    '订单取消流程',
    '售后服务说明',
    '物流查询方式'
]

# 封装获取embedding向量的函数；使用openai兼容客户端请求dashscope向量服务
def get_embedding(text):
    resp = client.embeddings.create(
        model=MODEL_NAME,
        input=text,
    )
    return resp.data[0].embedding


# -------------------1.构建简易内存向量库（python列表模拟向量数据库）-------------------
vector_db = []    # 初始化空列表充当内存向量库
# 遍历每一条知识库文档，生成向量存入内存库
for faq_doc in faq_docs:
    emb = get_embedding(faq_doc)                # 知识库文本转为向量
    vector_db.append({                          # 保存原文和对应的向量
        'text': faq_doc,
        'embedding': emb
    })


# -------------------2.实现检索器search，完成相似度召回-------------------
def search(query, top_k=3):
    """
    :param query: 用户问题
    :param top_k: 返回的数量
    :return: 返回排序后的top_k相似度结果
    """
    # 用户提问先调用接口生成查询向量
    query_emb = get_embedding(query)
    results = []   # 保存每一条知识和相似度得分

    # 循环遍历内存向量库，逐条计算用户query向量和知识库向量的余弦相似度
    for vec in vector_db:
        score = cosine_similarity(query_emb, vec['embedding'])
        results.append({
            'text': vec['text'],
            'score': score
        })
    # 将结果按照相似度得分降序，分数越高排越前面
    results.sort(key=lambda x: x['score'], reverse=True)
    # 返回相似度最高的top_k条记录
    return results[:top_k]


# -------------------3.测试检索逻辑，模拟用户提问-------------------
# query = '订单怎么退款'
# query = '订单则么退款'
# query = '发的什么快递'
# query = '快递信息怎么查'
query = '快递信息怎么获取'
results = search(query)    # 调用检索函数执行查询
print('--------------------------------')
# 循环打印召回的知识库文本和相似度得分
for res in results:
    print(res['text'], res['score'])


# -------------------4.构建mini版RAG，知识召回函数-------------------
"""
用户问题 -> Embedding -> 检索 -> 知识库/上下文 -> LLM
"""
def retrieve(query):
    # 调用search函数召回top3相关知识库片段
    docs = search(query=query, top_k=3)
    # 使用换行符把多条召回的知识库文本拼接，形成上下文context
    context = '\n'.join([doc['text'] for doc in docs])
    return context

# 用户实际提问
query = '订单怎么退款?'
# 执行知识召回，拿到检索出来的知识库上下文
context = retrieve(query)


# -------------------5.组装提示词prompt；把检索出来的知识给到LLM，约束基于知识库回答-------------------
prompt = f"""
你是商城客服助手.
已知知识:  {context}
用户问题: {query}
请给予知识回答.
"""

# -------------------6.调用大模型（openai兼容模式访问dashscope聊天接口，补全代码并加注释）-------------------
# 使用兼容接口调用通义千问聊天大模型，传入组装好的RAG提示词
chat_resp = client.chat.completions.create(
    model="qwen3.8-flash",                     # 指定通义千问聊天模型
    messages=[
        {"role": "user", "content": prompt}
    ]
)
# 取出大模型生成的客服回答
answer = chat_resp.choices[0].message.content
# 打印RAG最终输出答案
print("\n====RAG客服回答====")
print(answer)