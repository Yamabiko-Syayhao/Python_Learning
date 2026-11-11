"""
可以携带报错信息和提示词，可以重新让大模型修正自己的错误

"""
from typing import Literal
from pydantic import BaseModel, Field, model_validator
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.output_parsers import OutputFixingParser, RetryWithErrorOutputParser, format_instructions
from langchain_core.prompts import PromptTemplate
from tenacity import retry

# 封装好的大模型调用函数
from utils.llm import chat_utils

# 准备一个原始工单文本
SOURCE_TICKET_TEXT = "用户反应最近三个月网络经常中断，已经重启路由，但是没有任何效果，希望尽快核实处理"
# 规定evidence字段必须一字不差的等于这句话 目的是为了将校验提升到“内容必须匹配原文”逼出来OutputParserException修不好的情况，从而
# 引出了RetryWithErrorOutputParser
REQUIRED_EV = "已重启路由器，但是没有任何效果"

# 定义一个数据模型
class SupportTicket(BaseModel):
    ticket_id: str = Field(description="工单编号")
    priority: Literal['low','medium','high'] = Field(description="优先级")
    # 'account'账户管理， 'billing'计费问题, 'technic'技术问题
    category: Literal['account','billing','technic'] = Field(description="问题类别")
    is_follow:bool = Field(description="是否需要跟进")
    summary:str = Field(description="工单摘要")
    evidence:str = Field(description="必须从工单原文当中摘抄一段原文")

    # 自定义校验器 mode='after'表示所有字段都赋值完成之后再执行这个校验
    @model_validator(mode = 'after')
    def check_evidence(self):
        if self.evidence == REQUIRED_EV:
            return self
        else:
            # ValueError 会被Pydantic包装成校验错误  最终OutputParserException
            raise ValueError(f"evidence必须精确等于{REQUIRED_EV},用于确保来源的可追溯性")

# 定义提示词
template = """
工单内容:{ticket_text}
{format_instructions}

"""

# 实例化pydantic输出解析器，绑定工单数据结构
pydantic_parser = PydanticOutputParser(pydantic_object=SupportTicket)

# 实例化提示词模板
prompt = PromptTemplate(
    template=template,
    input_variables=["ticket_text"],
    partial_variables={"format_instructions":pydantic_parser.get_format_instructions()},

)
# 填充用户的提示词，填充上工单内容
final_prompt = prompt.format_prompt(ticket_text=SOURCE_TICKET_TEXT)


#模拟一个大模型的错误输出
bad_output = """
{
    "ticket_id":"BS123456",
    "priority":"high",
    "category":"billing",
    "is_follow":"False",
    "summary":"网慢",
}
"""

"""
本次错误输出有哪些问题：
    缺少evidence 
    网慢后边跟着逗号
    摘要太短了
"""

try:
    # 第一层 原始解析器 直接解析
    res_parser = pydantic_parser.parse(bad_output)
except OutputParserException as e:
    print("原始解析失败\n",str(e))
    # 第二级 自动修复
    fix_parser = OutputFixingParser.from_llm(
        parser=pydantic_parser,
        llm=chat_utils()
    )
    try:
        res_fixed = fix_parser.parse(bad_output)
        print(res_fixed,"自动修复解析器修复完毕")
    except OutputParserException as e:
        print("fix自动修复失败\n",str(e))
        # 第三级 报错重试
        retry_parser = RetryWithErrorOutputParser.from_llm(
            parser=pydantic_parser,
            llm=chat_utils(),
            max_retries=3,
        )
        try:
            # parse_with_prompt() 要求传入一个PromptValue对象 ,而不是字符串
            res_retry = retry_parser.parse_with_prompt(bad_output,final_prompt)
            print(res_retry, "重试")
        except OutputParserException as e:
            print("RetryWithErrorOutputParser解析失败", str(e))