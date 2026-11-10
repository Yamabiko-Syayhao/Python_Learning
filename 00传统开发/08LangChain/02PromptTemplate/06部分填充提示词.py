from config import DASHSCOPE_API_KEY,DASHSCOPE_BASE_URL
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

# 翻译模板
translator = ChatPromptTemplate.from_messages(
    [
        ("system","你是一个拥有十年工作经验的翻译官，精通{source}和{target}"),
        ("human","翻译：{text}"),

    ]
)
# partial 提前给部分变量赋值 半成品模板 以后只需要传递text即可
eToc = translator.partial(source="英文",target="中文")
cToj = translator.partial(source="中文",target="日语")

final_prompt = eToc.invoke({
    "text":"I am a student",
})

final_prompt2 = cToj.invoke({
    "text":"我是一名学生",
})
print(final_prompt,"最终提示词")

# 初始化客户端
llm = init_chat_model(
    # qwen3.8-flash
    model = "qwen3.8-flash",
    api_key = DASHSCOPE_API_KEY,
    base_url = DASHSCOPE_BASE_URL,
    model_provider = "openai"

)

res = llm.invoke(final_prompt2)
print(res.content)
