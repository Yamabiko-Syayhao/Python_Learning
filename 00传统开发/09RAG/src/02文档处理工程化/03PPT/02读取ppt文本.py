# 导入python-pptx库 uv add python-pptx
from pptx import Presentation


def get_text():
    prst = Presentation('../../dataset/苦糖果.pptx')
    # 存储所有文本
    all_text = []
    # 遍历 ppt 中的每一页幻灯片
    for slide in prst.slides:
        # 遍历每一页里的所有元素（文本，图片，表格，形状）
        for shape in slide.shapes:
            # hasattr 判断对象中是否存在 text 文本属性-----判断 提取 纯文本
            if hasattr(shape, "text"):
                text = shape.text.strip()
                # 判断是否有文本 如果存在文本就添加到列表当中
                if text:
                    all_text.append(text)
    # 将列表拼接成字符串
    content = "\n".join(all_text)
    print(content)


get_text()
