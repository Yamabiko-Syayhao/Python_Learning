from pathlib import Path

from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    FewShotPromptTemplate,
    load_prompt,
)
from langchain_core.output_parsers import StrOutputParser

from config import DASHSCOPE_API_KEY, DASHSCOPE_BASE_URL
from langchain_openai import ChatOpenAI


# ====== 1. 初始化大模型（OpenAI 兼容协议）======
llm = ChatOpenAI(
    model="qwen3.8-flash",
    api_key=DASHSCOPE_API_KEY,
    base_url=DASHSCOPE_BASE_URL,
)


# ====== 2. 通用翻译模板 ======
# source: 源语言  target: 目标语言  text: 待翻译文本
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一名专业的翻译，请把{source}准确翻译成{target}。"),
        ("human", "翻译文本：{text}"),
    ]
)

# ====== 3. 用 partial 预设三个翻译方向 ======
# partial 把 source / target 提前填死，之后只传 text 即可
en2zh = chat_prompt_template.partial(source="英文", target="中文")
zh2en = chat_prompt_template.partial(source="中文", target="英文")
zh2ja = chat_prompt_template.partial(source="中文", target="日文")


# ====== 4. 为 zh2en 创建 FewShot 示例增强模板 ======
# 单个示例的排版格式：变量名 chinese / english 要和 examples 里的 key 一致
example_prompt = PromptTemplate.from_template("中文: {chinese}\n英文: {english}")

# 至少 3 组示例，覆盖日常用语 + 专业术语
examples = [
    {"chinese": "今天天气真好。", "english": "The weather is really nice today."},
    {"chinese": "感谢您的耐心等待。", "english": "Thank you for your patience."},
    {"chinese": "人工智能正在改变各行各业。", "english": "Artificial intelligence is transforming every industry."},
    {"chinese": "您的订单已发货。", "english": "Your order has been shipped."},
]

zh2en_fewshot = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="你是一名专业的中译英翻译，请参考下面示例，把中文准确翻译成英文，只输出英文译文。",
    # suffix 里的变量就是最终调用时要传的参数
    suffix="中文: {chinese}\n英文:",
    input_variables=["chinese"],
)


# ====== 5. LCEL 串行管道：prompt | llm | parser ======
# 数据流：输入 dict -> 模板拼出提示词 -> 大模型返回 AIMessage -> 解析成纯字符串
en2zh_chain = en2zh | llm | StrOutputParser()
zh2en_chain = zh2en_fewshot | llm | StrOutputParser()
zh2ja_chain = zh2ja | llm | StrOutputParser()


# ====== 6. 保存 / 加载模板 ======
BASE_DIR = Path(__file__).resolve().parent
SAVE_PATH = BASE_DIR / "zh2en_fewshot.json"


def save_and_verify():
    """把 FewShot 模板存成 JSON，再用 load_prompt 读回来验证一致性。"""
    zh2en_fewshot.save(str(SAVE_PATH))
    loaded = load_prompt(str(SAVE_PATH))

    sample = {"chinese": "今天天气真好，我们一起去公园散步吧。"}
    same = loaded.invoke(sample).to_string() == zh2en_fewshot.invoke(sample).to_string()

    print(f"模板已保存到: {SAVE_PATH}")
    print(f"加载后与原模板拼装结果一致: {same}")
    return loaded


if __name__ == "__main__":
    print("=== 英译中 ===")
    print(
        en2zh_chain.invoke(
            {"text": "Artificial intelligence is reshaping every industry at an unprecedented pace."}
        )
    )

    print("\n=== 中译英（FewShot 增强）===")
    print(zh2en_chain.invoke({"chinese": "今天天气真好，我们一起去公园散步吧。"}))

    print("\n=== 中译日 ===")
    print(zh2ja_chain.invoke({"text": "感谢您的耐心等待，您的订单已发货。"}))

    print("\n=== 保存与加载验证 ===")
    loaded_prompt = save_and_verify()

    print("\n=== 用加载后的模板再翻译一次 ===")
    loaded_chain = loaded_prompt | llm | StrOutputParser()
    print(loaded_chain.invoke({"chinese": "今天天气真好，我们一起去公园散步吧。"}))
