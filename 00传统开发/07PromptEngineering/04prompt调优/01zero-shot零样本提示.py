"""

不给任何样例，仅凭指令，依靠模型原生知识完成任务。

✅优点：上手简单；❌缺点：小众复杂任务准确率低
适用：翻译、简单改写、常识问答、基础总结
不适用：小众分类、高精度标注

"""
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    #调用的时候将{WorkspaceId} 替换为真实的业务空间id 阿里云百炼的业务空间管理
    base_url="https://ws-bggm9k3qgbthz61a.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
# 定义提示词
content = """
    将文本分为中性，正面和负面
    文本：我觉着兰州拉面还可以
    情感：
    
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





