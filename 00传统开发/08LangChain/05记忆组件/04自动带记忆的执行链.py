from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# 内存聊天历史类 用来保存单论会话消息
from langchain_core.chat_history import InMemoryChatMessageHistory  # 专门用来存取管理整轮对话的历史消息
# RunnableWithMessageHistory 自动记忆包装器 Runnable基类 自定义组件继承它
from langchain_core.runnables import RunnableWithMessageHistory ,Runnable
# 标准AI消息对象 写回历史的时需要
from langchain_core.messages import AIMessage
from utils.llm import chat_prompt
from typing import Any
# LangChainDeprecationWarning专属的弃用警告类 精准的忽略弃用警告
from langchain_core._api.deprecation import  LangChainDeprecationWarning

# 自定义一个模拟类 继承Runnable 成为可管道符执行的组件
# 不真正调大模型 模拟模型
class MockLLM(Runnable):
    def invoke(self,prompt_value,config=None):
        # 必须返回AIMessage() 不是字符串
        # RunnableWithMessageHistory 要把ai的回复写回history，需要用到标准的消息对象，字符串会导致解析失败
        return AIMessage("推荐招牌珍珠奶茶，烫嘴最好喝")
# 构建对话提示词模板
prompt = ChatPromptTemplate.from_messages([
    ("system","你是奶茶店导购，记住用户对话"),
    # 消息占位符 变量名叫history 用来插入多条结构化历史对话记录
    MessagesPlaceholder(variable_name="history"),
    # 当前用户的最新提问
    ("user","{current_question}")
])

# 拼接一个LCEL执行链 此时chain是无记忆的普通链 prompt渲染--->MockLLM返回
chain = prompt | MockLLM()

# 全局字典仓库 将来可以存放所有的用户会话 多会话隔离靠这个字典
# key = session_id # 会话id
# value = 该会话的历史消息对象
store = {}
# 回调函数 根据会话id获取对话历史
def get_hist(sid):
    if sid not in store:
        # 如果用户是第一次会话，肯定没有聊天记录 那么就创建一个新的聊天记录存储对象
        store[sid] = InMemoryChatMessageHistory()
    return store[sid]

# 给基础链包装自动读写记忆的能力
# RunnableWithMessageHistory内部就是去 config["configurable"]["session_id"]读值
chat = RunnableWithMessageHistory(
    chain, # 原始的不带记忆的执行链
    history_messages_key="history", # 模板当中历史消息占位符的变量名
    input_messages_key="current_question", # 用户提问的占位符变量名
    get_session_history=get_hist # 回调函数 获取/创建会话存储器
)
# 封装对话调用函数
def talk(sid,msg):
    # 触发一次带记忆的对话调用 把用户问题 和 这是哪个会话 一起交给包装器
    # 两个参数 第一个输入msg填充{current_question}占位符
     # 第二个config configurable.session_id 告诉包装器这是哪个会话
    res = chat.invoke({"current_question":msg},config={"configurable":{"session_id":sid}})
    print(f"[{sid}用户：{msg} | AI:{res.content}")

if __name__ == '__main__':
    talk("uu1","给我推荐一份套餐")
    talk("uu1","什么甜度最好喝")
    talk("uu2","有没有果茶")
    print("\nuu1完整会话")
    for m in store["uu1"].messages:
        print(f"{m.type}:{m.content}")
    print("\nuu2完整会话")
    for m in store["uu2"].messages:
        print(f"{m.type}:{m.content}")




