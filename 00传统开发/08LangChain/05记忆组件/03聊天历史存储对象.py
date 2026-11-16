"""
MessagesPlaceholder 动态历史消息占位组件 负责在提示词模板中预留位置 把结构化的历史消息列表填充在prompt
InMemoryChatMessageHistory：
1.对话历史存储类
2.专门用来存取，管理整轮对话的历史消息
3.管理整轮对话的历史消息存在内存中
4.把整轮对话的的消息列表存在内存中
5.程序关闭数据消失，不持久化
"""

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory # 专门用来存取管理整轮对话的历史消息
from utils.llm import chat_prompt

# 构建了一个带着历史消息占位符的对话模板
prompt = ChatPromptTemplate.from_messages([
    ("system","你是一个淘宝闪购平台的外卖客服人员，请结合历史对话，回答客户消息"),
    # 消息占位符 变量名叫history 用来插入多条结构化历史对话记录
    MessagesPlaceholder(variable_name="history"),
    # 当前用户的最新提问
    ("user","{current_question}")
])

if __name__ == "__main__":
    # 创建一个内存对话历史对象 用来保存本次会话的全部问答
    history = InMemoryChatMessageHistory()
    # 往对话历史列表当中追加一条"用户消息"
    history.add_user_message("我刚才点的喷射套餐为何还没到？")
    # 往对话历史列表当中追加一条"AI回答"
    history.add_ai_message("请稍等，正在帮您查看送餐进度？")

    # 往对话历史列表当中追加一条"用户回答"
    history.add_user_message("刚才骑手给我致电说自己迷路了")
    # 往对话历史列表当中追加一条"AI回答"
    history.add_ai_message("不好意思已经联系了骑手，告诉了他正确的路线")

    print(history.messages,type(history))
    # 填充完整的prompt
    final_prompt = prompt.invoke({
        # 报错 因为InMemoryChatMessageHistory对象本身不能直接塞到占位符中，要.messages拿到对话列表
        "history":history.messages,
        "current_question":"我现在已经饿死了，退款吧"
    })
for item in final_prompt.to_messages():
    print(f"{item.type}---{item.content}")

    """
    
    
    """

