import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)

from utils.llm import chat_utils

llm = chat_utils()
json_parser = JsonOutputParser()


def calc_subtotal(order: dict) -> float:
    return round(
        sum(item["price"] * item["quantity"] for item in order["items"]),
        2,
    )


def calc_shipping(order: dict) -> float:
    return 8.0 if order["city"] in ("北京", "上海", "广州", "深圳") else 12.0


def calc_discount(order: dict, config: dict | None = None) -> float:
    cfg = config.get("configurable", {}) if config else {}
    channel = cfg.get("channel", "web")
    user_type = cfg.get("user_type", "normal")

    rate = 0.0
    if channel == "app":
        rate += 0.05
    if user_type == "vip":
        rate += 0.10
    return round(order["subtotal"] * rate, 2)


def calc_total(order: dict) -> float:
    return round(order["subtotal"] + order["shipping"] - order["discount"], 2)


calc_parallel = RunnableParallel(
    subtotal=RunnableLambda(calc_subtotal),
    shipping=RunnableLambda(calc_shipping),
)


def merge_calc(payload: dict) -> dict:
    return {**payload["order"], **payload["calculated"]}


enrich_order = (
    RunnableParallel(
        order=RunnablePassthrough(),
        calculated=calc_parallel,
    )
    | RunnableLambda(merge_calc)
    | RunnablePassthrough.assign(discount=RunnableLambda(calc_discount))
    | RunnablePassthrough.assign(total=RunnableLambda(calc_total))
)


summary_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是订单摘要生成助手。请严格根据订单数据生成 JSON，"
            "金额保留两位小数，不要输出 JSON 以外的内容。\n{format_instructions}",
        ),
        (
            "user",
            "订单数据：\n{order_data}\n\n"
            "请生成包含以下字段的 JSON：\n"
            "- order_id：订单编号\n"
            "- item_count：商品种类数\n"
            "- total：应付金额\n"
            "- summary_text：一句话摘要，示例：尊敬的张三，您购买了3类商品，应付 12098.00 元",
        ),
    ]
).partial(format_instructions=json_parser.get_format_instructions())


def prepare_summary_input(order: dict) -> dict:
    return {"order_data": json.dumps(order, ensure_ascii=False, indent=2)}


summary_chain = (
    RunnableLambda(prepare_summary_input)
    | summary_prompt
    | llm
    | json_parser
)

pipeline = enrich_order | summary_chain


if __name__ == "__main__":
    order = {
        "order_id": "OD-20260520-001",
        "customer": "张三",
        "city": "北京",
        "items": [
            {"goods_name": "机械键盘", "price": 320.0, "quantity": 1},
            {"goods_name": "鼠标", "price": 89.0, "quantity": 2},
            {"goods_name": "显示器", "price": 1599.0, "quantity": 1},
        ],
    }

    scenarios = [
        ("Web 普通用户", {"configurable": {"channel": "web", "user_type": "normal"}}),
        ("App VIP 用户", {"configurable": {"channel": "app", "user_type": "vip"}}),
    ]

    for name, config in scenarios:
        detail = enrich_order.invoke(order, config=config)
        summary = pipeline.invoke(order, config=config)
        print(f"\n===== {name} =====")
        print(
            "明细："
            f"subtotal={detail['subtotal']}, "
            f"shipping={detail['shipping']}, "
            f"discount={detail['discount']}, "
            f"total={detail['total']}"
        )
        print("摘要 JSON：")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
