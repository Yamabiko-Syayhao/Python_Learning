import os
import dashscope
from dashscope import MultiModalConversation

# 北京地域公共接口地址
dashscope.base_http_api_url = "https://ws-bggm9k3qgbthz61a.cn-beijing.maas.aliyuncs.com/api/v1"

api_key = os.getenv("DASHSCOPE_API_KEY")

if not api_key:
    raise RuntimeError("未找到 DASHSCOPE_API_KEY 环境变量")

print("API Key 存在：", bool(api_key))
print("API 地址：", dashscope.base_http_api_url)

response = MultiModalConversation.call(
    api_key=api_key,
    model="qwen-image-3.0-pro",
    messages=[
        {
            "role": "user",
            "content": [
                {"text": "生成一张蓝天白云下的小猫照片"}
            ]
        }
    ],
    prompt_extend=True
)

print("状态码：", response.status_code)
print("请求ID：", response.request_id)
print("完整响应：", response)

if response.status_code == 200:
    print("生成成功！")
    print(response.output.choices[0].message.content)
else:
    print("错误代码：", response.code)
    print("错误信息：", response.message)