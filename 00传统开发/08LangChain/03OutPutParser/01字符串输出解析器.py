"""
大模型输出的特点：
    输出的内容又随机性
    输出格式不稳定 一般输出的都是 非常自由的 自然语言

当模型结果能被后边的程序所需要的时候，要根据需求去设置具体的格式，json字符串，列表，字典。。。
langchain提供了输出解析器组件

StrOutputParser 字符串输出解析器
"""
from langchain_core.output_parsers import StrOutputParser

from config import DASHSCOPE_API_KEY,DASHSCOPE_BASE_URL

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

# 创建一个提示词模板
prompt_template = PromptTemplate.from_template("快速回答下面的问题：{question}")
final_template = prompt_template.format(question="汉堡好吃吗")


# 初始化客户端
# 设置初始化 后续调大模型
llm = init_chat_model(
    # qwen3.8-flash
    model = "qwen3.8-flash",
    api_key = DASHSCOPE_API_KEY,
    base_url = DASHSCOPE_BASE_URL,
    model_provider = "openai"

)

res = llm.invoke(final_template)
str_parse = StrOutputParser()
res_str = str_parse.invoke(res)
print(res_str)


