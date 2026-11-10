# uv add langchain langchain-openai
from langchain_classic.chains.question_answering.map_reduce_prompt import messages

from config import DASHSCOPE_API_KEY,DASHSCOPE_BASE_URL
from langchain.chat_models import init_chat_model

# ChatOpenAI走的是openAI兼容协议 一个模型只有有对应的openai兼容接口的时候才能使用


# 初始化客户端
llm = init_chat_model(
    # qwen3.8-flash
    model = "qwen3.8-flash",
    api_key = DASHSCOPE_API_KEY,
    base_url = DASHSCOPE_BASE_URL,
    model_provider="openai",
)

# 第一种 纯字符串
# res1 = llm.invoke("你是谁")
# print(res1.content) # 直接查看大模型的输出的内容，如果只输出res就会有所有的字段

# 第二种 传统写法 消息列表
# messages = [
#     {"role":"system","content":"你好"},
#     {"role":"user","content":"你好"},
#     {"role":"assistant","content":"你好,我是wwww"},
#
# ]
# re2 = llm.invoke(messages)
# print(re2.content)

# 第三种 消息对象
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
# SystemMessage 系统提示词
# HumanMessage 用户输入
# AIMessage 大模型的回复
messages = [
    SystemMessage("你是江户时期的诗人，很会写俳句"),
    HumanMessage("写一首关于春天的俳句"),
    AIMessage("这里输出你写的春天的俳句,用日语原文")
]

res3 = llm.invoke(messages)
print(res3.content)
# 查看token使用情况
print(res3.usage_metadata)
# 包含模型名称，模型供应商，结束原因等等
print(res3.response_metadata)