"""
JsonOutputParser json输出解析器
"""
from plistlib import dump

from langchain_core.output_parsers import JsonOutputParser

from config import DASHSCOPE_API_KEY,DASHSCOPE_BASE_URL

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

json_parse = JsonOutputParser()
template = '''
    你是一个经验丰富的学习桂花助手，需要根据用户需求生成json数据
    {format_instructions}
    
    请返回一个包含下面字段的json对象：
    -teach_name:技术名称
    -diff:技术难度
    -goal:目标
    -days:学习时间
    -daily_plan:每天学习计划
        -day:第几天
        -task:任务
        
    用户需求{text}
'''
# 创建一个提示词模板
prompt_template = PromptTemplate(
    template=template,
    # input_variables 声明模板中的所有占位变量 校验传入参数是否全 列表中的值要跟{}中的值一一对应
    input_variables = ["text"],
    # partial_variables 提前注入变量 后续只需要传text就行
    # json_parse.get_format_instructions() 内置格式提示词 告诉模型要输出什么样的格式
    partial_variables={"format_instructions":json_parse.get_format_instructions()}
)

# 使用提示词模板 填充
final_template = prompt_template.format(text="如何在一周内学会langchain")


# 初始化客户端
# 设置初始化 后续调大模型
llm = init_chat_model(
    # qwen3.8-flash
    model = "qwen3.8-flash",
    api_key = DASHSCOPE_API_KEY,
    base_url = DASHSCOPE_BASE_URL,
    model_provider = "openai"

)

res = llm.invoke(final_template)
res_dict = json_parse.parse(res.content)
# print(res_str)

print(res_dict,type(res_dict))

import json
with open(file="output2.txt",mode="w",encoding="utf-8") as f:
    json.dump(res_dict,f,ensure_ascii=False,indent=4)
    print("保存成功\n23")
