# 导入大模型提示词模板 用来组装系统提示词+用户提问
from langchain_core.prompts import ChatPromptTemplate
# 封装好的大模型工具类（自定义工具）
from utils.llm import chat_prompt

template = ChatPromptTemplate.from_messages([
    ("system", "你是一个乐于助人的情感分析专家，尽你所能回答用户的问题，回答要简洁明了，控制字数在50个字以内"),
    ("user", "{question}")
])

# 获取大模型对话实例
llm = chat_prompt
# LCEL 执行链 提示词模板 | 大模型
chain = template | llm
# 第一次调用链 传入第一个用户问题
resp = chain.invoke({"question": "我的女朋友叫小光，她最近一直在跟我冷战，我应该怎么解决这个问题"})
print(resp.content)
# 第二次调用链 传入第二个用户问题
resp2 = chain.invoke({"question": "我的女朋友名字是什么"})
print(resp2.content)


# 两次invoke相互独立 没有会话记忆功能 ，所以大模型在第二次回答的时候不会记住上一轮 女朋友叫小光的信息
