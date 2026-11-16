"""
==================== 数据库分类与选型速查 ====================

【一、关系型数据库（Relational Database / RDBMS）】
代表：MySQL、PostgreSQL、Oracle、SQL Server、MariaDB、SQLite
特点：
  - 数据以固定二维表（行/列）保存，schema 先定义后写入；
  - 支持 SQL、事务（ACID）、表间关联；
  - 适合结构化数据、强一致性场景（订单、用户、财务）。
外键（Foreign Key）：
  - 物理外键：在数据库层建 FOREIGN KEY 约束，由 DB 保证引用完整性；
  - 逻辑外键：只在应用层维护关联，不建 DB 约束（互联网高并发场景常用，
    避免外键带来的锁与性能开销）。

【二、非关系型数据库（NoSQL），按数据模型分类】
  - KV 键值型：Redis —— 缓存、会话、排行榜，内存为主，极快；
  - 文档型：MongoDB —— JSON/BSON 文档，schema 灵活，适合内容、日志；
  - 搜索引擎：Elasticsearch —— 全文检索、日志分析（ELK）；
  - 时序型：InfluxDB、ClickHouse —— 监控指标、日志等海量时序数据；
  - 列式/OLAP：ClickHouse —— 大数据分析、报表；
  - 图数据库：Neo4j —— 社交关系、知识图谱。
特点：schema 灵活、易水平扩展，但通常牺牲强事务/强一致，按场景选用。

【三、SQLite 是什么】
  - 轻量级嵌入式关系型数据库，整个库就是一个 .db 文件；
  - 零配置、无需单独安装服务进程，程序内直接读写文件；
  - 支持标准 SQL 与事务，适合本地开发、调试、桌面/移动端、小规模单机；
  - 并发写入能力弱（写锁全库），不适合高并发生产服务。

【四、本文为什么用 SQLite + SQLChatMessageHistory】
  - SQLChatMessageHistory 是 LangChain 提供的 SQL 持久化对话存储，
    底层基于 SQLAlchemy，聊天记录写入 SQL 数据库，程序重启不丢；
  - 选 SQLite 是因为零配置、自动建库建表（chat_history.db），最适合演示；
  - 生产环境可把 connection 换成 MySQL / PostgreSQL，接口不变。

【五、选型速查】
  强事务/结构化业务      → MySQL / PostgreSQL
  本地开发/嵌入式/演示    → SQLite
  缓存/会话/排行榜        → Redis
  灵活文档/内容管理       → MongoDB
  全文搜索/日志分析       → Elasticsearch
  监控指标/海量时序       → InfluxDB / ClickHouse
  大数据 OLAP 分析        → ClickHouse
  关系图谱                → Neo4j
============================================================
"""
# 用来生成唯一的会话id
import uuid
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# SQL持久化聊天历史组件 对话存入sqlite数据库文件
from langchain_community.chat_message_histories import SQLChatMessageHistory
# RunnableWithMessageHistory 自动记忆包装器 Runnable基类 自定义组件继承它
from langchain_core.runnables import RunnableWithMessageHistory
# 封装好的大模型调用工具
from utils.llm import chat_prompt

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是奶茶店导购，请结合历史对话去回答用户问题"),
    # 预留了历史对话占位符
    MessagesPlaceholder("history"),
    # 当前用户的最新提问
    ("user", "{question}")
])
llm = chat_prompt
# 拼接一个LCEL执行链 此时chain是无记忆的普通链 prompt渲染--->真实的大模型
# 根据传进来的用户名user_key 生成一个名字不变 可重复的id 并且转为字符串
# uuid.uuid5(命名空间,名字) 基于名字 生成uuid 同样的名字永远生成同样的字符串id
chain = prompt | llm
def gen_session_id(user_key):
    return str(uuid.uuid5(uuid.NAMESPACE_URL,f"demo:{user_key}"))
# 基于SQL数据库的聊天记录存储器
def get_session_history(session_id: str):
    # SQLChatMessageHistory 是langchain中的持久化存储 聊天记录会存到数据库中 数据不会丢失 自动创建数据库 自动读写数据
    # session_id 会话唯一标识 不同session_id的历史相互隔离
    # connection=f"sqlite:///chat-history.db"  sqlite:///表示用的sqlite数据库   chat-history.db表示当前目录下的数据库文件
    return SQLChatMessageHistory(session_id=session_id, connection=f"sqlite:///chat-history.db")


# 给基础链增加自动读写数据库会话的记忆能力
# RunnableWithMessageHistory 内部就是去 config["configurable"]["session_id"]读值
chat = RunnableWithMessageHistory(
    chain,  # 原始的不带记忆的执行链
    history_messages_key="history",  # 模板当中历史消息占位符的变量名
    input_messages_key="question",  # 用户提问的占位符变量名
    get_session_history=get_session_history  # 读写聊天历史的方法
)
# 封装对话调用函数
def talk(user_key: str, question: str):
    """
    :param user_key: 用户名
    :param question: 用户输入的问题
    """
    res = chat.invoke({"question": question}, config={
        "configurable": {
            "session_id": gen_session_id(user_key)
        }
    })
    print(f"问题:{question}-----{user_key}")
    print(f"回答:{res.content}")


if __name__ == '__main__':
    # 每一次talk 都是先读后填会话历史，调大模型，最后再写
    talk("arl", "我是乐队主唱，想喝奶茶，我的乐队键盘手是myk，她想喝奶茶，有没有合适推荐的")
    talk("arl", "她说要三分糖")
    talk("arl", "键盘手叫什么？")

    # print("查看uu23的历史消息")
    # history = get_session_history(gen_session_id("uu23"))
    # print(history.messages)
