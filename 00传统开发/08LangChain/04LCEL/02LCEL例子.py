# 让大模型输出结构化数据 并且用Pydantic做严格校验
# PydanticOutputParser Pydantic输出解析器 可以将大模型的输出直接解析成Pydantic模型对象
# 用于静态类型检查 不影响运行时的行为
import json
from typing import Literal, final
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
# BaseModel 数据模型基类 field 给字段添加描述 校验
from pydantic import BaseModel,Field


# 封装好的大模型调用函数
from utils.llm import chat_prompt

from langchain_core.runnables import RunnablePassthrough





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
parser = PydanticOutputParser(pydantic_object=CourseInfo)

template = """
    你是一个课程信息提取小助手，请从以下文本中，提取所需要的结构化数据，超出限制不符合要求的按照设定区间进行修改
    文本：{text}
    {format_instructions}
"""

# 3.创建提示词模板
prompt = PromptTemplate(template=template)

chain = (
    RunnablePassthrough.assign(
        # _约定好 我接收这个参数 但是我不用
        format_instructions = lambda _:parser.get_format_instructions()
    )
    | prompt
    | chat_prompt
    | parser
)

if __name__ == "__main__":
    res = chain.invoke({
        "text":"课程带薪摸鱼的108种方式，由李老师主讲，总计67课时，属于初级课程，课程售价0.2元，是一门线上课适合老板不在的时候在工位偷偷学习，并随时准备切换窗口的资深打工人"
    })
    print(res.model_dump_json(indent=2))
    print("解析成功")
    print(res.to_dict())
    # try:
    #     with open("res.json","w",encoding="utf-8") as f:
    #         f.write(res.model_dump_json(indent=2))
    # except Exception as e:
    #     print("保存失败",e)





