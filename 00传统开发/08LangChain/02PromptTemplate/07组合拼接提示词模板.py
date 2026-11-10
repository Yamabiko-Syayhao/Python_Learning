# uv add langchain langchain-openai
from typing import final

from langchain_classic.chains.summarize.map_reduce_prompt import prompt_template

from config import DASHSCOPE_API_KEY,DASHSCOPE_BASE_URL
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
# ChatOpenAI走的是openAI兼容协议 一个模型只有有对应的openai兼容接口的时候才能使用

frist = PromptTemplate.from_template("亲亲你好，我是{name}")
second = PromptTemplate.from_template("只要你{GiveMe}")
third = PromptTemplate.from_template("我就{end}")

# 将多个提示词+
full_prompt = frist + second + third

final_prompt = full_prompt.invoke({
    "name":"孙洒",
    "GiveMe":"给我五百万",
    "end":"带你上天",

})


# 初始化客户端
# 设置初始化 后续调大模型
llm = init_chat_model(
    # qwen3.8-flash
    model = "qwen3.8-flash",
    api_key = DASHSCOPE_API_KEY,
    base_url = DASHSCOPE_BASE_URL,
    model_provider = "openai"

)
res = llm.invoke(final_prompt)
print(res.content)