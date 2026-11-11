#

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field
from langchain_core.exceptions import OutputParserException
# OutputFixingParser 自动修复解析器 如果解析失败 会自动调用llm进行修复输出
# 局限性：只能解决一些比较简单的问题 比如说格式错误/类型错误/引号出错。不过涉及到语义理解的大错他修复不了
# 他记不住我们给他的提示，它修复用的是它自己内部的提示词，跟你原始的业务prompt无关
from langchain_classic.output_parsers import OutputFixingParser
# 封装好的大模型调用函数
from utils.llm import chat_prompt, chat_utils


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

# OutputFixingPaser
fix_parse = OutputFixingParser.from_llm(
    parser=pydantic_parser,
    llm = chat_utils(),
)
res = fix_parse.parse(bad_output)
print(res)

# try:
#     # parse 解析字符串
#     res = pydantic_parser.parse(bad_output)
#     print(res,"原始解析结果")
# except OutputParserException as e:
#     print("解析失败，交给大模型修复")
#     # 构造了一个专门修复json格式的提示词
#     fix = f"""
#         把下面损坏的文本修正成标准的JSON
#         错误文本：{bad_output}
#         报错信息：{e},
#         规则：price应该是数字，status是布尔，不要多余文字
#     """
#     res = chat_prompt(fix)
#     fix_res = pydantic_parser.parse(res.content)
#     print(res,"修复之后的结果")
#     print(fix_res,"修复之后的校验结果")

