# 让大模型输出结构化数据 并且用Pydantic做严格校验
# PydanticOutputParser Pydantic输出解析器 可以将大模型的输出直接解析成Pydantic模型对象
# 用于静态类型检查 不影响运行时的行为
from typing import Literal, final

from langchain_core.output_parsers import StrOutputParser

from config import DASHSCOPE_API_KEY,DASHSCOPE_BASE_URL

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
# BaseModel 数据模型基类 field 给字段添加描述 校验
from pydantic import BaseModel,Field
# 解析失败的时候抛出异常
from langchain_core.exceptions import OutputParserException

# 封装好的大模型调用函数
from utils.llm import chat_prompt

# 1.定义数据模型（告诉代码 我要什么结构）
class CourseInfo(BaseModel):
    course_name:str = Field(description="课程名称")
    teacher:str = Field(description="教师名称")
    # level字段只能从"初级","中级","高级"中取值 其他的值校验报错
    level:Literal["初级","中级","高级"] = Field(description="课程难度")
    # ge = 10 大于等于10，le = 50 小于等于50 课时必须在10-50之间
    course_hours:int = Field(description="课时，一节课（45）分钟算一节课",ge=10,le=50)
    # gt = 0 表示大于 价格必须大于0 lt则是小于
    price:float = Field(description="课程价格",gt=0)
    online:bool = Field(description="是否为线上课程")
    # default 设置字段默认值
    remark:str = Field(description="备注",default="")

# 2.创建输出解析器 实例化一个Pydantic输出解析器
# 传入定义好的数据模型类
pydantic_parser = PydanticOutputParser(pydantic_object=CourseInfo)
# print(pydantic_parser.get_format_instructions())

# 3.创建提示词模板
template ="""
    你是一个课程信息提取小助手，请从以下文本中，提取所需要的结构化数据，超出限制不符合要求的按照设定区间进行修改
    文本：{text}
    {format_instructions}
"""
prompt = PromptTemplate(
    template=template,
    input_variables=["text"],
    partial_variables={"format_instructions":pydantic_parser.get_format_instructions()},
)

# 4.填充原文 text生成完整提示词
final_prompt = prompt.format(text="""
    课程带薪摸鱼的108种方式，由李老师主讲，总计67课时，
    属于初级课程，课程售价0.2元，是一门线上课
    适合老板不在的时候在工位偷偷学习，并随时准备切换窗口的资深打工人
""")




# 初始化客户端
# 设置初始化 后续调大模型
llm = init_chat_model(
    # qwen3.8-flash
    model = "qwen3.8-flash",
    api_key = DASHSCOPE_API_KEY,
    base_url = DASHSCOPE_BASE_URL,
    model_provider = "openai"

)
# 大模型返回文本 str 未校验
res = llm.invoke(final_prompt)
print(res.content)

try:
    res_parser = pydantic_parser.invoke(res)
    # 返回courseIfo 实例对象
    print(res_parser,type(res_parser))
except OutputParserException as e:
    print("错误消息",e)







