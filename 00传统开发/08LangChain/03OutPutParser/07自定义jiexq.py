# 提问--->模型回答--->把回答拆分成列表
from typing import List
from langchain_core.exceptions import OutputParserException
# 输出的解析器基类
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import PromptTemplate
# 封装好的调用大模型函数
from utils.llm import chat_prompt

# 自定义解析器
class NameListParser(BaseOutputParser):
    # 必须实现的方法1 方法里面的这段文字会被塞到提示词里面， 告诉大模型如何去回答
    def get_format_instructions(self) -> str:
        return "输出五个中国女生的姓名，名字之间用中文的逗号隔开，不要多余解释，不要序号，不要换行"
    # 必须实现的方法2 把大模型返回的字符串 转换成列表
    def parse(self,text: str) -> List[str]:
        # 去掉前后空格
        cleaned_text = text.strip()
        # 检查内容是否为空
        if not cleaned_text:
            raise OutputParserException("你的内容不能为空，解析失败")
        # 分割字符串 返回列表
        name_list = [name.strip() for name in cleaned_text.split("，")]
        return name_list

# 实例化自定义解析器
name_parse = NameListParser()
# 构建提示词模板
prompt = PromptTemplate(
    template="根据需求生成名字：{demand}\n {format_instructions}",
    input_variables=['demand'],
    partial_variables={'format_instructions':name_parse.get_format_instructions()},
)
"""
    根据需求输出名字{demand}
    输出五个中国女生的姓名，名字之间用中文的逗号隔开，不要多余解释，不要序号，不要换行
"""

# 填充半成品提示词模板中的demand
final_prompt = prompt.format_prompt(demand="古风")
print(final_prompt)
# 调用大模型
res = chat_prompt(final_prompt)
# 调用自定义解析器去解析内容
res_final = name_parse.parse(res.content)
print(res_final)