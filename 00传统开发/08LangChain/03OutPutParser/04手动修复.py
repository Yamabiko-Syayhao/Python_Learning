# 核心思想 用AI修复AI的输出  把"解析失败"变成一个可自动恢复的闭环

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field
from langchain_core.exceptions import OutputParserException
# 封装好的大模型调用函数
from utils.llm import chat_prompt

# 定义数据模型约束 约束字段
class GoodInfo(BaseModel):
    good_name: str = Field(description="商品名称")
    price: float = Field(description="商品价格",ge=0)
    status: bool = Field(description="商品是否有货")

# 模拟大模型输出了一个坏的结果
bad_output = """
    我提取到的数据如下：
    {'good_name':'iphone18','price':'18888.88','status':'yes'}
"""

"""
    问题：
        类型错误 price应该是float,status应该是bool
        多余前缀 我提取到的数据如下：  json外边带着多余的文字
        json语法错误  json标准要求key必须是双引号  key:value
"""

# 实例化一个Pydantic输出解析器 传入定义好的数据模型类
# pydantic_object 不保证模型一定会按照指令生成
pydantic_parser = PydanticOutputParser(pydantic_object=GoodInfo)

try:
    # parse 解析字符串
    res = pydantic_parser.parse(bad_output)
    print(res,"原始解析结果")
except OutputParserException as e:
    print("解析失败，交给大模型修复")
    # 构造了一个专门修复json格式的提示词
    fix = f"""
        把下面损坏的文本修正成标准的JSON
        错误文本：{bad_output}
        报错信息：{e},
        规则：price应该是数字，status是布尔，不要多余文字
    """
    res = chat_prompt(fix)
    fix_res = pydantic_parser.parse(res.content)
    print(res,"修复之后的结果")
    print(fix_res,"修复之后的校验结果")