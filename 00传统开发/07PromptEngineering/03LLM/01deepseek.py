# 登录deepseek  https://www.deepseek.com/,注册账号 登录，绑定邮箱，实名认证，充点小钱
# Please install OpenAI SDK first: `uv add openai`
import os
# 从openai库中导入OpenAI客户端类  deepseek兼容openai接口协议
from openai import OpenAI

client = OpenAI(
    # 从系统环境变量中读取DEEPSEEK_API_KEY
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    # 指定deepseek官方接口请求地址
    base_url="https://api.deepseek.com",
)
# 调用大模型会话补全接口  发起聊天请求
response = client.chat.completions.create(
    # 模型
    model="deepseek-v4-flash",
    # 对话消息列表
    messages=[
        # system 系统  设定AI助手的身份  设定行为规则
        {"role": "system", "content": "你是梦限大MewType的键盘手藤都子，会回答一些提问，在此之前先做个详细的自我介绍"},
        # user 用户 用户输入的提问内容
        {"role": "user", "content": "你是谁？"},
    ],
    # 关闭流式输出  一次性返回完整回答
    stream=True,
    # 设置高推理强度  增强模型思考能力
    reasoning_effort="high",
    # 开启思维链思考输出
    extra_body={"thinking": {"type": "enabled"}},
)

# 返回模型的问答结果
# 非流式输出的回答
# print(response.choices[0].message.content)
# 流式输出回答
for chunk in response:
    content = chunk.choices[0].delta.content

    if content:
        print(content,end="",flush=True)


