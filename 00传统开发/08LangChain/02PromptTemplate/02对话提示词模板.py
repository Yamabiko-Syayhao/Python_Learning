# uv add langchain langchain-openai
from typing import final

from langchain_classic.chains.summarize.map_reduce_prompt import prompt_template

from config import DASHSCOPE_API_KEY,DASHSCOPE_BASE_URL
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from utils.llm import chat_prompt

# ChatOpenAI走的是openAI兼容协议 一个模型只有有对应的openai兼容接口的时候才能使用

# 创建对话提示词模板
# system = 系统提示 human = 用户提示词 ai = 大模型回复
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system","你是一个{角色}，你擅长{领域}"),
        ("human","你是一个{角色}，你擅长{领域}"),
        ("ai","你好，很高兴回答你的{问题}"),
        ("human","{用户补充的内容}"),

    ]
)
# 使用模板
# 方法1：format_messages 替换占位符 返回消息列表
final_template1 = chat_prompt_template.format_messages(
    角色 = "美食家",
    领域 = "美食评价",
    问题 = "川菜有什么经典",
    用户补充的内容 = "介绍三道就行"
)
# print(final_template1,type(final_template1))


final_template2 = chat_prompt_template.invoke({
    "角色":"乐队主唱",
    "领域":"唱歌",
    "问题":"哪些歌你喜欢",
    "用户补充的内容":"我现在想你随便介绍几个"
})
# print(final_template2,type(final_template2))

# 初始化客户端
llm = init_chat_model(
    # qwen3.8-flash
    model = "qwen3.8-flash",
    api_key = DASHSCOPE_API_KEY,
    base_url = DASHSCOPE_BASE_URL,
    model_provider = "openai"

)

res = llm.invoke(final_template1)
print(res.content)


