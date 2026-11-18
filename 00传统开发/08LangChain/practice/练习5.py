import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain.chat_models import init_chat_model
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import (
    ConfigurableField,
    RunnableBranch,
    RunnableLambda,
    RunnableSerializable,
    RunnableWithMessageHistory,
)

from config import DASHSCOPE_API_KEY, DASHSCOPE_BASE_URL, DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL


MODEL_REGISTRY = {
    "qwen": init_chat_model(
        model="qwen3.8-flash",
        api_key=DASHSCOPE_API_KEY,
        base_url=DASHSCOPE_BASE_URL,
        model_provider="openai",
    ),
    "deepseek": init_chat_model(
        model="deepseek-chat",
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL,
        model_provider="openai",
    ),
}

ACTIVE_MODEL = os.environ.get("LLM_MODEL", "qwen")
active_llm = MODEL_REGISTRY[ACTIVE_MODEL]


class LLMServiceError(Exception):
    pass


_request_count = 0


def flaky_llm(prompt_value, config=None):
    global _request_count
    _request_count += 1
    if _request_count == 1:
        print("[重试机制] 第 1 次请求抛出 LLMServiceError，开始指数退避重试...")
        raise LLMServiceError("模拟首次请求失败")
    print(f"[重试机制] 第 {_request_count} 次请求成功")
    return active_llm.invoke(prompt_value, config)


robust_llm = RunnableLambda(flaky_llm).with_retry(
    retry_if_exception_type=(LLMServiceError,),
    stop_after_attempt=3,
    wait_exponential_jitter=True,
)


class ResponseStrategy(RunnableSerializable):
    max_response_length: int = 100
    system_role: str = "你是乐于助人的智能助手"

    def invoke(self, input, config=None):
        messages = input.to_messages() if hasattr(input, "to_messages") else list(input)
        system_message = SystemMessage(
            content=(
                f"{self.system_role}。请用中文回答，"
                f"回答不超过 {self.max_response_length} 字。"
            )
        )
        return robust_llm.invoke([system_message, *messages], config=config)


base_strategy = ResponseStrategy().configurable_fields(
    max_response_length=ConfigurableField(
        id="max_response_length",
        name="最大回复字数",
        description="控制模型回复的最大字数",
    ),
    system_role=ConfigurableField(
        id="system_role",
        name="系统角色",
        description="设定助手的角色和回答风格",
    ),
)

brief_strategy = base_strategy.with_config(
    config={
        "max_response_length": 50,
        "system_role": "你是简洁高效的生活助手，直接给出实用建议",
    }
)

detailed_strategy = base_strategy.with_config(
    config={
        "max_response_length": 200,
        "system_role": "你是资深技术专家，回答要详细并分点说明",
    }
)

TECH_KEYWORDS = ("代码", "python", "编程", "bug", "算法")
LIFE_KEYWORDS = ("天气", "美食", "旅游", "购物")


def is_technical(payload: dict) -> bool:
    content = payload["question"].lower()
    return any(keyword in content for keyword in TECH_KEYWORDS)


def is_life(payload: dict) -> bool:
    content = payload["question"].lower()
    return any(keyword in content for keyword in LIFE_KEYWORDS)


def build_prompt(system_text: str) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system", system_text),
            MessagesPlaceholder(variable_name="history"),
            ("user", "{question}"),
        ]
    )


technical_prompt = build_prompt("你是一名编程技术专家，擅长解答代码、算法和 bug 问题。")
life_prompt = build_prompt("你是一名生活助手，擅长解答天气、美食、旅游和购物问题。")
general_prompt = build_prompt("你是一名通用助手，请友好、准确地回答用户问题。")

store: dict[str, InMemoryChatMessageHistory] = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


def build_chat(strategy):
    branch = RunnableBranch(
        (is_technical, technical_prompt | strategy),
        (is_life, life_prompt | strategy),
        general_prompt | strategy,
    )
    return RunnableWithMessageHistory(
        branch,
        get_session_history=get_session_history,
        history_messages_key="history",
        input_messages_key="question",
    )


detailed_chat = build_chat(detailed_strategy)
brief_chat = build_chat(brief_strategy)


def talk(chat, session_id: str, question: str) -> str:
    reply = chat.invoke(
        {"question": question},
        config={"configurable": {"session_id": session_id}},
    )
    print(f"\n[{session_id}] 用户：{question}")
    print(f"[{session_id}] 助手：{reply.content}")
    return reply.content


if __name__ == "__main__":
    print(f"当前使用模型：{ACTIVE_MODEL}，可选模型：{list(MODEL_REGISTRY)}")

    talk(
        detailed_chat,
        "user_A",
        "Python 里怎么用递归实现二分查找算法？请给我代码示例。",
    )
    talk(detailed_chat, "user_A", "这个算法的时间复杂度是多少？")
    talk(
        detailed_chat,
        "user_A",
        "刚才提到的那个方法，再详细讲讲，最好给出完整代码。",
    )

    talk(brief_chat, "user_B", "北京今天天气怎么样，适合去旅游吗？")
    talk(brief_chat, "user_B", "附近有什么好吃的美食推荐？")
    talk(
        brief_chat,
        "user_B",
        "刚才说的那个美食，去购物中心能买到食材吗？",
    )

    print("\n===== 会话隔离验证 =====")
    for session_id in ("user_A", "user_B"):
        messages = store[session_id].messages
        print(f"\n[{session_id}] 共 {len(messages)} 条消息")
        for message in messages:
            print(f"{message.type}: {message.content[:80]}")

    print(
        "\n验证结果："
        f"user_A 与 user_B 分别保存了 {len(store['user_A'].messages)} 条和 "
        f"{len(store['user_B'].messages)} 条独立历史记录。"
    )
