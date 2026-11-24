# 导入python-pptx库 uv add python-pptx
from pptx import Presentation


def get_title(path):
    prst = Presentation(path)
    # 存储所有文本
    all_text = []
    # 遍历 ppt 中的每一页幻灯片
    for index,slide in enumerate(prst.slides,start=1):
        print(f"第{index}页")
        title = slide.shapes.title
        if title:
            # 查看标题内容
            print(title.text)


get_title("../../dataset/标题提取.pptx")
