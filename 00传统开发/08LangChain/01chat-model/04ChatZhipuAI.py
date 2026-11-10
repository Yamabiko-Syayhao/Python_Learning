# uv add langchain langchain-openai

from langchain_community.chat_models import ChatZhipuAI
from langchain_openai import ChatOpenAI
from config import DASHSCOPE_API_KEY, DASHSCOPE_BASE_URL, DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, ZHIPU_API_KEY, ZHIPU_BASE_URL

# ChatOpenAI走的是openAI兼容协议 一个模型只有有对应的openai兼容接口的时候才能使用


# 初始化客户端
llm = ChatZhipuAI(
    model = "glm-5.3",
    api_key = "be3eff06e37f4a5cbdbaf19e62db34a4.YXdLC3J6bfaR4kwG",
    api_base = "https://open.bigmodel.cn/api/paas/v4/chat/completions",
)

# 调用
res = llm.invoke("你是？")
print(res.content) # 直接查看大模型的输出的内容，如果只输出res就会有所有的字段
