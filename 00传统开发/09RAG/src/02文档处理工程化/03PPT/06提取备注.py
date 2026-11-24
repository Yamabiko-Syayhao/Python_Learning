# 导入python-pptx库 uv add python-pptx
from pptx import Presentation


def get_images():
    prst = Presentation('../../dataset/苦糖果.pptx')
    # 遍历 ppt 中的每一页幻灯片
    for index, slide in enumerate(prst.slides, start=1):
        # 获取每一页的备注
        notes = slide.notes_slide.notes_text_frame.text
        if notes:
            print(f"写在第{index}页的备注是:{notes}")

get_images()
