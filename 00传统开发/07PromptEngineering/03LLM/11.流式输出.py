"""



"""

import os
from openai import OpenAI

# 1. 准备工作：初始化客户端
client = OpenAI(
    # 建议通过环境变量配置API Key，避免硬编码。
    api_key=os.environ["DASHSCOPE_API_KEY"],
    # API Key与地域强绑定，请确保base_url与API Key的地域一致。
    base_url="https://ws-bggm9k3qgbthz61a.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 2. 发起流式请求
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "请介绍一下自己"}
    ],
    stream=True,
    stream_options={"include_usage": True}
)

# 3. 处理流式响应
# 用列表暂存响应片段，最后 join 比逐次 += 字符串更高效
content_parts = []
print("AI: ", end="", flush=True)

for chunk in completion:
    if chunk.choices:
        content = chunk.choices[0].delta.content or ""
        print(content, end="", flush=True)
        content_parts.append(content)

full_response = "".join(content_parts)
# print(f"\n--- 完整回复 ---\n{full_response}")