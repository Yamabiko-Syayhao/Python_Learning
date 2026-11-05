import os
import base64
import mimetypes
import dashscope
from dashscope import MultiModalConversation
# {WorkspaceId}换成自己的业务空间id
dashscope.base_http_api_url = 'https://ws-bggm9k3qgbthz61a.cn-beijing.maas.aliyuncs.com/api/v1'

response = MultiModalConversation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 模型选择 自己琢磨琢磨
    model="qwen-image-2.1-pro",
    messages=[{
        "role": "user",
        "content": [
            {"text": """
                "title":"春节快乐",
                "sub_title":"家庭团聚，共享天伦之乐",
                "body_text":"春节是中国最重要的传统节日之一，它象征着新的开始和希望",
                "prompt_text_zh":"灯笼，二哈，梅花",
                "wh_ratios":"竖版",
                "lora_name":"童话油画",
                "lora_weight":0.8,
                "ctrl_ratio":0.7,
                "ctrl_step":0.7,
                "generate_mode":"generate",
                "generate_num":1
            """}
        ]
    }],
    # generate_mode 海报生成模式  必选
    prompt_extend=True
)

if response.status_code == 200:
    url = response.output.choices[0].message.content[0]["image"]
    print(f"Generated image URL: {url}")
else:
    print(f"Error: {response.code} - {response.message}")