# # 每个模型都有自己的方法，有一种方法是通用方法---语法限定
# # from openai import max_retries
#
# from config import DASHSCOPE_API_KEY, DASHSCOPE_BASE_URL, DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL
# # 引入langchain初始化函数 方便快速切换其他模型 业务改动相对较少
# from langchain.chat_models import init_chat_model
#
# openai = init_chat_model(
#     # 指定模型名称
#     model = "deepseek-v4-flash",
#     # 密钥
#     api_key = DEEPSEEK_API_KEY,
#     # 请求地址
#     base_url = DEEPSEEK_BASE_URL,
#     # 指定厂商
#     model_provider = "openai",
#     # 温度 文本多样性0-2，数值越大越多样
#     temperature = 0.7,
#     # 请求超时时间
#     timeout = 30,
#     # 最大token输出数量
#     max_tokens = 1000,
#     # 禁止流式输出
#     streaming = False,
#     # 网络失败自动重试参数
#     max_retries = 3,
#
# )
#
# res = openai.invoke("你是？")
# print(res.content)
#

# 使用封装好的大模型
# 1.引入封装好的大模型
from utils.llm import chat_prompt
# 调用封装好的
res = chat_prompt("你是什么模型？")
print(res.content)