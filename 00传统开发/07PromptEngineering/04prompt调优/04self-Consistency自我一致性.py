"""

基于 CoT，生成3‑5 条不同推理路径，多条答案投票，取出现最多的结果作为最终答案。

强项：数学、多步骤业务计算；❌不适合：文案创作、翻译，消耗 token 高

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
    Q:3个苹果，吃掉一个，又买了2个，一共剩下几个？
    A：路径1，3-1=2，2+2=4
        路径2：3+2=5，5-1=4
        路径3：3-1+2=4
        路径4：3+1+2=6
        结果4出现了3次，所以最终计算结果就是4
    Q:现在隔壁我70岁了，当我6岁的时候，我妹妹的年龄是我年龄的一半，现在妹妹多大
    请生成3-4条独立不同的推理路径，每条给出答案，最终给出计算结果
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


