"""
LCEL 的全称是 LangChain Expression Language（LangChain表达式语言）
就是langchain自带的流水线语法
用“|”把一个一个可独立运行的AI组件穿起来，前一个的输出当成后一个的输入，不用手动定义
变量，不用写传值代码
流程示例： 提示词拼接文字，丢给ai拿结果，把ai的结果转为json格式
提示词模板prompt | 大模型llm | 解析器parser
"""
from itertools import chain

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field
# 封装好的大模型调用函数
from utils.llm import chat_prompt
# 原样透传输入 你给他什么 他就原封不动的还给你
from langchain_core.runnables import RunnablePassthrough


# 1.定义数据模型（告诉代码 我要什么结构）
class Result(BaseModel):
    answer: str = Field(description="回答")
    suggest:str = Field(description="建议")
# 准备一下“三件套”提示词模板prompt | 大模型 | 解析器

# 2.创建输出解析器 实例化一个Pydantic输出解析器
# 传入定义好的数据模型类
parser = PydanticOutputParser(pydantic_object=Result)
# print(pydantic_parser.get_format_instructions())

# 3.创建提示词模板
prompt = ChatPromptTemplate(
    [
        ("human","请简单回答问题，并且给一条建议，格式要求：{format_instructions}\n 问题：{question}")
    ]
)
"""
LCEL标准写法
chain = (
    RunnablePassthrough.assign(
        变量=lambda x:解析器变量.get_format_instructions(x)
     )
    | 提示词变量
    | 大模型变量 你调用的大模型
    | 解释器变量
)"""

chain = (
    RunnablePassthrough.assign(
        format_instructions=lambda x:parser.get_format_instructions()
     )
    | prompt
    | chat_prompt
    | parser
)
# 此处只需要传递question format_instruction 由流水线自动注入 不用手动传递
resp = chain.invoke({"question":"怎么快速学完typescript"})
print(f"{resp}\n{type(resp)}") # 为<class '__main__.Result'>类型的变量
# 直接按照字段去访问 不用手动转换格式
print(resp.answer)
print(resp.suggest)







