# 导入python-pptx库 uv add python-pptx
from pptx import Presentation


def get_images():
    prst = Presentation('../../dataset/苦糖果.pptx')
    count =1
    # 遍历 ppt 中的每一页幻灯片
    for index, slide in enumerate(prst.slides, start=1):
        for shape in slide.shapes:
            # 判断是否有表格
            if shape.shape_type == 13: # 固定的 规定 13 为图片类型
                # 获取图片对象
                img = shape.image
                # 获取图片的扩展名 png，jpg...
                ext = img.ext
                # 获取图片的二进制流数据 用来保存图片的
                blob = img.blob
                # 为什么不放 index 而放 count 如果一个 ppt 上有多个图片。那么用 index 有图片覆盖的风险
                img_path = f"../../dataset/ppt_img/img_{count}.{ext}"
                # 写入本地文件
                with open(img_path, "wb") as f:
                    f.write(blob)
                print(f"已经提取保存第{count}张图片，图片的名字是img_{count}.{ext}")
                count += 1

get_images()
