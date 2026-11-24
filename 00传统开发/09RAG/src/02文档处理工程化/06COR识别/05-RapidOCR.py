"""
    RapidOCR（轻量化，免费  易部署）
    RapidOCR：基于 ONNXRuntime 的轻量 OCR。
    优点：无需安装 paddle，包小、跨平台、CPU 友好。
    企业边缘部署/Docker 镜像瘦身首选。
"""
# uv add  rapidocr-onnxruntime
from rapidocr_onnxruntime import RapidOCR
# 初始化RapidOCR对象
rapid_ocr = RapidOCR()
# 识别图片 result 识别结果列表， elapse 各阶段耗时（检测，识别等用了多少秒，可以用来做性能分析）
result, elapse = rapid_ocr("docs/1.png")
# result[0]:坐标,图片上这行文字所在的矩形四个角的像素坐标
# result[1]:文本,图片上文字识别结果
# result[2]:置信度,对识别结果的信心值,0-1,如果是0,则表示置信度低,不建议使用
# result: [ [坐标, 文本, 置信度], ... ]
# 定义空字符串
str = ''
# 检查结果是否为空
if result:
    # 遍历结果
    for item in result:
        # 拼接文本
        str += item[1] + ';'
print(str)

"""
from rapidocr import RapidOCR

# 初始化 RapidOCR 对象
rapid_ocr = RapidOCR()

# 识别图片
result = rapid_ocr("docs/1.png")

# 定义空字符串
str_list = []
# 新包结果直接是 RapidOCROutput 对象，文本在 .txts 属性中
if result and result.txts:
    for text in result.txts:
        str_list.append(text)

print(';'.join(str_list))
"""