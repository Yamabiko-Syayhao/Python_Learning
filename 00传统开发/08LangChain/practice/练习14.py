from langchain_community.document_loaders import TextLoader
from pathlib import Path
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from utils.llm import chat_utils
from langchain_text_splitters import (CharacterTextSplitter,
                                      RecursiveCharacterTextSplitter,
                                      TokenTextSplitter)

text_path = Path("智能客服平台知识库.txt")
loader = TextLoader(text_path,encoding="utf-8")
txt = loader.load()

splitter_CT = CharacterTextSplitter(
    separator='\n\n',
    chunk_size=150,
    chunk_overlap=30
)
splitter_RC = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=30
)
splitter_TT = TokenTextSplitter(
    chunk_size=60,
    chunk_overlap=15,
    encoding_name='cl100k_base'
)

chunks_char = splitter_CT.split_documents(
    txt
)
chunks_recursive = splitter_RC.split_documents(
    txt
)
chunks_token = splitter_TT.split_documents(
    txt
)

# 三种切分器的对比打印
def report(name,chunks):
    print(f"\n===== {name} =====")
    print(f"chunk 数量：{len(chunks)}")
    if chunks:
        first = chunks[0].page_content
        print(f"第一个 chunk 文本长度:{len(first)}")
        print(f"前 80 个字符：{first[:80]}")
report("CharacterTextSplitter",chunks_char)
report("RecursiveCharacterTextSplitter",chunks_recursive)
report("TokenTextSplitter",chunks_token)

# 创建知识库
knowledge = []
for doc in chunks_recursive:
    knowledge.append(doc.page_content)

# 构建提示词模板
prompt = ChatPromptTemplate.from_messages([
    ("system",
    "你是智能客服平台的知识库助手。"
    "请只根据下面的知识库内容回答；"
    "如果知识库中没有答案，就明确说没有查到，不要编造。\n\n"
    "知识库内容：\n{context}"),
    MessagesPlaceholder(variable_name="history"),
    ("user","{question}"),
]).partial(context=knowledge) # 提前把知识库内容的 context 固定填进去，后面每次只需要传 question

# 创建 llm 执行流水线
llm = chat_utils()
chain = prompt | llm

# 创建历史存储和记忆包装器
store = {}
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]
chat = RunnableWithMessageHistory(
    chain,
    get_session_history=get_session_history,
    history_messages_key="history",
    input_messages_key="question",
)

# 三轮对话
def talk(session_id: str,question:str):
    res = chat.invoke(
        {"question":question,},
        config={"configurable":{"session_id":session_id}},
    )
    print(f"\n用户：{question}")
    print(f"\n助手：{res.content}")

if __name__ == "__main__":
    session_id = "user_001"
    talk(session_id,"会员等级有哪些？分别有什么权益？")
    talk(session_id,"支付失败有哪些可能的原因")
    talk(session_id,"你刚才说的这些问题，哪些是我作为普通会员可能遇到的")


