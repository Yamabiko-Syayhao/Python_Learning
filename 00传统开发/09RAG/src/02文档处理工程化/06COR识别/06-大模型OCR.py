"""
    传统 OCR 只能"认字"，认不出版面逻辑。
    多模态大模型（VLM）能：认字 + 理解版面 + 直接输出结构化。
    比如一张发票图，直接让 Qwen-VL 输出 JSON。

    企业用途：
        复杂版面、手写体、票据信息抽取、图表理解
"""
# 导入os库,用于获取环境变量
import os
# 导入OpenAI库,用于调用OpenAI API
from openai import OpenAI
# 导入base64库,用于将图片转换为base64编码的字符串
import base64
# 创建OpenAI客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://ws-bggm9k3qgbthz61a.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
# 定义函数
def vlm_ocr(image_path):
    # 将接收的图片读取为二进制数据
    with open(image_path, "rb") as f:
        # 将图片转换为base64编码的字符串
        b64 = base64.b64encode(f.read()).decode()
    # 调用OpenAI API,发送图片和指令
    resp = client.chat.completions.create(
        model="qwen3.8-max-0902",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "提取这张发票的字段，输出JSON：发票号、金额、购买方统一社会信用代码/纳税人识别号、销售方统一社会信用代码/纳税人识别号、项目名称、开票人、日期"},
                {"type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
            ]
        }]
    )
    return resp.choices[0].message.content
str = vlm_ocr("docs/1.png")
print(str,type(str))

'''
    将本地图片读取为二进制数据 ---> 通过base64库将图片转换为base64编码的字符串 ---> 编写提示词 ---> LLM ---> 生成结果
'''