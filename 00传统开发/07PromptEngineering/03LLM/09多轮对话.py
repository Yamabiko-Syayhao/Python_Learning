# 多轮对话核心一句话：模型本身无状态，“记忆”全靠messages列表的累计
import os
from email import message

from openai import OpenAI
from openai.types.beta import assistant

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    #调用的时候将{WorkspaceId} 替换为真实的业务空间id 阿里云百炼的业务空间管理
    base_url="https://ws-bggm9k3qgbthz61a.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)


def get_response(messages):
    completion = client.chat.completions.create(
            # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            model="qwen3.8-flash",
            messages=messages
    )
    # 把大模型的结果返回出去
    return completion.choices[0].message.content

# 初始化
messages = []

# 第一轮对话
messages.append({"role": "user", "content": "讲一下typescript"})
print(f"第一轮：")
print(f"用户提问：{messages[0]["content"]}")
assistant_output = get_response(messages)
messages.append({"role": "assistant", "content": assistant_output})
print(f"大模型回答:{assistant_output}\n")

# 第二轮对话
messages.append({"role": "user", "content": "它的主要语法有？"})
print(f"第二轮：")
print(f"用户提问：{messages[0]["content"]}")
assistant_output = get_response(messages)
messages.append({"role": "assistant", "content": assistant_output})
print(f"大模型回答:{assistant_output}\n")



# json在线解析小工具   大模型给出的json格式可能不是很好查看  可以格式化一下   https://www.bejson.com/explore/index_new/index.html
# print(completion.model_dump_json())


