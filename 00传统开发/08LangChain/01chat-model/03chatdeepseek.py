# uv add langchain langchain-openai

from langchain_deepseek import ChatDeepSeek
from config import DASHSCOPE_API_KEY, DASHSCOPE_BASE_URL, DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

# ChatOpenAI走的是openAI兼容协议 一个模型只有有对应的openai兼容接口的时候才能使用


# 初始化客户端
llm = ChatDeepSeek(
    # qwen3.8-flash
    model = "deepseek-flash",
    api_key = DEEPSEEK_API_KEY,
    base_url = DEEPSEEK_BASE_URL,
)

# 调用
res = llm.invoke("写调用你的标准格式py代码")
print(res.content) # 直接查看大模型的输出的内容，如果只输出res就会有所有的字段