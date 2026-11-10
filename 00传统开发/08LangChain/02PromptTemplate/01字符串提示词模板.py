# uv add langchain langchain-openai
from langchain_classic.chains.summarize.map_reduce_prompt import prompt_template

from config import DASHSCOPE_API_KEY,DASHSCOPE_BASE_URL
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
# ChatOpenAI走的是openAI兼容协议 一个模型只有有对应的openai兼容接口的时候才能使用

# 初始化提示词
# {}代表的是占位变量，后面会由真实的数据填充
prompt_template1 = PromptTemplate(
    template="""
    你是一个{角色}，请用{风格}的风格，回答以下问题：
    问题：{问题}
    """,
    # input_variables 声明模板中的所有占位变量 校验传入参数是否全 列表中的值要跟{}中的值一一对应
    input_variables = ["角色","风格","问题"]
)
final_template2 = prompt_template1.invoke({
    "角色":"音乐制作人",
    "风格":"严肃",
    "问题":"介绍一下日系流行",
})


# 简洁写法
prompt_template2 = PromptTemplate.from_template(
    """
    你是一个{角色}，请用{风格}的风格，回答以下问题：
    问题：{问题}
    """
)
# 使用上边初始化过的提示词模板prompt_template1/prompt_template2
# 方法1：format 将变量注入到模板中 最终生成一个可以直接发给大模型的完整字符串
final_template1 = prompt_template2.format(
    角色 = "你是一个音乐制作人",
    风格 = "幽默又正经",
    问题 = "讲一下涉谷系"
)


# 初始化客户端
# 设置初始化 后续调大模型
llm = init_chat_model(
    # qwen3.8-flash
    model = "qwen3.8-flash",
    api_key = DASHSCOPE_API_KEY,
    base_url = DASHSCOPE_BASE_URL,
    model_provider = "openai"

)
# 1
# res = llm.invoke(final_template1)
# print(res.content)

# 2

# print(final_template2)
# print(type(final_template2))
res = llm.invoke(final_template2)
print(res)