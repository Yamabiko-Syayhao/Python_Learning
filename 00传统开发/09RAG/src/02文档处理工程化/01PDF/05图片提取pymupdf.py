# 基础文本解析工具 uv add pypdf pdfplumber pymupdf
# pypdf 适合进行 PDF 的基础操作 如合并 拆分 简单的文字提取
# pdfplumber 更适合处理复杂的表格数据提取，或者是需要获取字符坐标信息的场景
# pymupdf 通常作为默认的首选 速度快精度高，适合常规文本提取和图像处理

import pymupdf

def parse_by_pymupdf_img():
    pdf = pymupdf.open("../../dataset/内科学知识库.pdf")
    for page_num,page in enumerate(pdf,start=1):
        # 获取当前页所有的图片 返回的数据是元组(有完整信息)
        images = page.get_images(full=True)
        # print(images,"所有图片")
        for idx,image in enumerate(images,start=1):
            # 图片在pdf内部的唯一对象编号 图片的唯一标识
            xref = image[0]
            # 通过 xref 加载图片二进制到 pixmap 对象
            # Pixmap 是 pymupdf 中的位图对象，里面封装了像素数据，色彩空间，宽高，通道数
            # Pixmap(pdf,xref) 按照 xref 从文档中解码出图片
            pixmap = pymupdf.Pixmap(pdf,xref)
            # 通常是 CMYK + 专色通道等复杂多通道图片（印刷用）
            # 1 灰度 3 RGB 4 RGBA
            if pixmap.n >= 5:
                pixmap = pymupdf.Pixmap(pymupdf.csRGB,pixmap)
            print(f"第{page_num}页第{idx}张图片提取中....")
            img_path = f"../../dataset/pdf_img/page{page_num}_img{idx}.png"
            # 确定保存
            pixmap.save(img_path)
            # 释放资源
            pixmap = None


    print("提取结束")
    # 关闭pdf文档
    pdf.close()
# 调用函数
parse_by_pymupdf_img()