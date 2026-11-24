# PaddleOCR
"""
PaddleOCR：百度开源，中文场景准确率最高。
自带文本检测 + 方向分类 + 文本识别，开箱即用。
"""
from paddleocr import PaddleOCR

# use_angle_cls=True 自动纠正文字方向（倒置/旋转）
ocr = PaddleOCR(use_angle_cls=True, lang="ch")
# 新写法
result = ocr.ocr("./docs/1.png")
print(result)
# 定义字符串
page_text = ""
# 检查结果是否为空
if result and result[0]:
    # rec_texts 直接就是所有识别文字的列表
    text_list = result[0]['rec_texts']
    # 将列表转为字符串输出
    page_text = "\n".join(text_list)
print(f"【页纯文本】\n{page_text}")