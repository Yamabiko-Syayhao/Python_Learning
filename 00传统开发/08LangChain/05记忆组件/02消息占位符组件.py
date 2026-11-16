"""
# MessagesPlaceholder 动态历史消息占位符组件
# 作用：在ChatPromptTemplate提示词模板中预留一块专属空位 专门用来存放完整对话历史消息列表
普通占位符{} 只能填一段文本字符串
MessagesPlaceholder 接收的是结构化的消息列表[HumanMessage,AIMessage,HumanMessage]
"""
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import HumanMessage,AIMessage
from utils.llm import chat_prompt

# 构建了一个带着历史消息占位符的对话模板
prompt = ChatPromptTemplate.from_messages([
    ("system","你是贴心的情感顾问，回答简短精炼"),
    MessagesPlaceholder(variable_name="history"),
    ("user","{current_question}")
])
# 模拟一段历史会话（结构化消息列表）
chat_history = [
    # 用户提问
    HumanMessage(content="我女朋友叫光，最近在和我冷战，我该如何？"),
    # AI回答
    AIMessage(content="你可以主动找她沟通了解一下矛盾产生的原因")
]

# 填充模板 把历史消息直接插入到占位的位置
fill_prompt = prompt.invoke({
    # 历史消息
    "history":chat_history,
    # 当前问题
    "current_question":"我女朋友叫什么",
})

res = chat_prompt(fill_prompt)
print(res.content)

