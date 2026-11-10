from config import DASHSCOPE_API_KEY,DASHSCOPE_BASE_URL
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate,FewShotPromptTemplate

# 初始化提示词
# {}代表的是占位变量，后面会由真实的数据填充
example_prompt = PromptTemplate.from_template(
    "输入：{input}\n 输出：{output}"
)

# 准备少量样本数据
example = [
    {"input":"悟空","output":"10"},
    {"input":"悟空悟空","output":"100"},
    {"input":"悟空+悟空","output":"20"},
    {"input":"悟空*4","output":"40"},

]

# 组装少样本提示词模板、
final_template = FewShotPromptTemplate(
    # 给大模型举的例子
    examples = example,
    # 指定输出格式
    example_prompt =  example_prompt,
    # 前缀
    prefix = "你是一个汉字算数专家。请严格遵守案例规则计算结果，只输出数字",
    # 后缀
    suffix = "输入：{input} \n 输出",
    input_variables = ["input"]
)
# 给模板填充变量
final_prompt = final_template.invoke({
    "input":"悟空*3-悟空+1"
})
# print(final_prompt)



# 初始化客户端
# 设置初始化 后续调大模型
llm = init_chat_model(
    # qwen3.8-flash
    model = "qwen3.8-flash",
    api_key = DASHSCOPE_API_KEY,
    base_url = DASHSCOPE_BASE_URL,
    model_provider = "openai"

)

res = llm.invoke(final_prompt)
print(res.content)