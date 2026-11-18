import sys
from datetime import datetime
from pathlib import Path
from typing import Literal

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import (
    RunnableBranch,
    RunnableLambda,
    RunnableWithMessageHistory,
)
from pydantic import BaseModel, Field

from utils.llm import chat_utils


class SupportTicket(BaseModel):
    ticket_id: str = Field(description="工单编号，格式如 TK-20260520-001")
    priority: Literal["low", "medium", "high"] = Field(description="优先级")
    category: Literal["refund", "technical", "general"] = Field(description="问题类别")
    summary: str = Field(description="问题摘要，不少于10个字", min_length=10)
    contact: str = Field(description="用户联系方式")


llm = chat_utils()

ticket_parser = PydanticOutputParser(pydantic_object=SupportTicket)

ticket_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是客服工单信息提取助手，请从用户问题描述中提取结构化工单信息。"
            "ticket_id 必须原样使用 {ticket_id}。\n{format_instructions}",
        ),
        ("user", "用户问题描述：{text}"),
    ]
).partial(format_instructions=ticket_parser.get_format_instructions())

ticket_chain = ticket_prompt | llm | StrOutputParser() | ticket_parser


def normalize(text: str) -> dict:
    return {"content": text.strip().lower(), "text": text}


def contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in text for keyword in keywords)


def is_refund(payload: dict) -> bool:
    return contains_any(payload["content"], ("退款", "退货", "重复扣款"))


def is_technical(payload: dict) -> bool:
    return contains_any(payload["content"], ("报错", "无法登陆", "闪退", "bug"))


def refund_handler(payload: dict) -> dict:
    return {"queue": "REFUND_QUEUE", "wait": "2h", "text": payload["text"]}


def technical_handler(payload: dict) -> dict:
    return {"queue": "TECHNICAL_QUEUE", "wait": "4h", "text": payload["text"]}


def general_handler(payload: dict) -> dict:
    return {"queue": "GENERAL_QUEUE", "wait": "24h", "text": payload["text"]}


classify_chain = RunnableLambda(normalize) | RunnableBranch(
    (is_refund, RunnableLambda(refund_handler)),
    (is_technical, RunnableLambda(technical_handler)),
    RunnableLambda(general_handler),
)

support_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是电商平台的智能客服。请结合历史对话理解用户意图，"
            "用礼貌、简洁的中文回复，并说明后续处理方式。",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{question}"),
    ]
)

chat_chain = support_prompt | llm

store: dict[str, InMemoryChatMessageHistory] = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


chat = RunnableWithMessageHistory(
    chat_chain,
    get_session_history=get_session_history,
    history_messages_key="history",
    input_messages_key="question",
)


def new_ticket_id(sequence: int = 1) -> str:
    return f"TK-{datetime.now().strftime('%Y%m%d')}-{sequence:03d}"


def build_ticket(description: str, ticket_id: str) -> SupportTicket:
    try:
        return ticket_chain.invoke({"text": description, "ticket_id": ticket_id})
    except OutputParserException as error:
        print(f"[工单解析失败，使用兜底数据] {error}")
        summary = description[:20] if len(description) >= 10 else "用户问题描述待补充"
        return SupportTicket(
            ticket_id=ticket_id,
            priority="medium",
            category="general",
            summary=summary,
            contact="未提供",
        )


def talk(session_id: str, question: str, ticket: SupportTicket | None = None) -> dict:
    route = classify_chain.invoke(question)
    reply = chat.invoke(
        {"question": question},
        config={"configurable": {"session_id": session_id}},
    )
    print(f"\n[用户] {question}")
    print(f"[客服] {reply.content}")
    print(f"[分流] {route['queue']}，预计等待 {route['wait']}")
    if ticket is not None:
        print(f"[工单] {ticket.model_dump_json()}")
    return route


if __name__ == "__main__":
    session_id = "customer-001"

    first_question = (
        "我上周买的蓝牙耳机出现了重复扣款，订单号 A20260520，"
        "我想申请退款，我的邮箱是 alice@example.com"
    )
    ticket = build_ticket(first_question, new_ticket_id(1))
    talk(session_id, first_question, ticket)

    talk(session_id, "退款进度怎么样了？大概多久能退回来？")
    talk(session_id, "好的，我确认，请尽快帮我处理。")

    print("\n===== 完整会话历史 =====")
    for message in store[session_id].messages:
        print(f"{message.type}: {message.content}")
