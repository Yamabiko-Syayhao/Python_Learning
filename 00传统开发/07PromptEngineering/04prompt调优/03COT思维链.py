"""

不让模型直接输出答案，强制分步拆解问题，输出中间推理步骤，再给出最终结果。

解决：数学计算、逻辑推理、复杂阅读理解，减少一步直答带来逻辑错误
❌不适合：简单翻译、短句分类（浪费 token）

"""
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 调用的时候将{WorkspaceId} 替换为真实的业务空间id 阿里云百炼的业务空间管理
    base_url="https://ws-bggm9k3qgbthz61a.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
# 定义提示词
content = """
    question:王手里有三个苹果，又从张那里枪了六个，又被李从手里抢了七个，问王还有几个？
    answers:王一开始有三个苹果，后来抢了六个，一共3+6=9个，后来又被抢走了七个，所以他手里还有
    9-7=2个
    question:公交车上有三个人,过了两站下去了两个,又过了三站上来了八个人,问公交车上还有多少人?
    answer:
"""

completion = client.chat.completions.create(
    # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    model="qwen3.8-flash",
    messages=[
        {"role": "user", "content": content},
    ]
)
# json在线解析小工具   大模型给出的json格式可能不是很好查看  可以格式化一下   https://www.bejson.com/explore/index_new/index.html
# print(completion.model_dump_json())
print(completion.choices[0].message.content)


