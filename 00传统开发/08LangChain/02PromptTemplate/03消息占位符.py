from idlelib import history

from config import DASHSCOPE_API_KEY,DASHSCOPE_BASE_URL
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_core.messages import HumanMessage, AIMessage
# ChatOpenAI走的是openAI兼容协议 一个模型只有有对应的openai兼容接口的时候才能使用

# 创建对话提示词模板
# system = 系统提示 human = 用户提示词 ai = 大模型回复
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system","你是一个《西游记》{角色}，你的说话风格是{风格}，每次回答不超过{字数}个字"),
        # MessagesPlaceholder 消息占位符 专门用来塞入完整的消息对象列表
        # variable_name = 变量名  传值的时候变量名必须叫history
        MessagesPlaceholder(variable_name = "history"),
        ("human","{input}"),

    ]
)
# 模拟历史记录
history_message = [
    HumanMessage(content = "悟空，前边有一条大河，看着水流湍急，我们该如何过去"),
    AIMessage(content = "不用慌张，俺老孙火眼金睛，这水下定是藏了什么妖魔鬼怪"),
    HumanMessage(content = "阿弥陀佛"),
    AIMessage(content = "俺老孙去也"),
]
# 使用模板
# 方法1：format_messages 替换占位符 返回消息列表
final_template1 = chat_prompt_template.format_messages(
    角色 = "齐天大圣",
    风格 = "狂妄，急躁，喜欢动手",
    字数 = "100",
    input = "悟空你回来了，那河里有什么"
)
print(final_template1,type(final_template1))


# final_template2 = chat_prompt_template.invoke({
#     "角色":"乐队主唱",
#     "领域":"唱歌",
#     "问题":"哪些歌你喜欢",
#     "用户补充的内容":"我现在想你随便介绍几个"
# })
# # print(final_template2,type(final_template2))
#
# # 初始化客户端
# llm = init_chat_model(
#     # qwen3.8-flash
#     model = "qwen3.8-flash",
#     api_key = DASHSCOPE_API_KEY,
#     base_url = DASHSCOPE_BASE_URL,
#     model_provider = "openai"
#
# )
#
# res = llm.invoke(final_template1)
# print(res.content)


