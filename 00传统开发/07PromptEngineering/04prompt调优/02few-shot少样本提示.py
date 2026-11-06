"""

提供少量示范样例，让模型模仿样例的格式、逻辑、风格完成新任务。

原理：用样例给模型定规则，不需要微调模型，低成本提升效果
✅适用：自定义分类、固定格式生成、特殊提取规则；❌不适用：海量样本场景（适合微调）

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
    写一首俳句，要符合格式，要有季语。用日语原版
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