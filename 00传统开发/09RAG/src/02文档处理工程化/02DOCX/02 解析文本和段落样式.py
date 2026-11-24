from docx import Document

def parse_docx_style(path):
    doc = Document(path)
    for paragraph in doc.paragraphs:
        # 获取当前段落的样式名称
        style = paragraph.style.name
        # 获取当前段落的文本内容 去掉首尾空格
        text = paragraph.text.strip()
         # 如果段落内容为空 就跳过本次循环 执行下一次循环
        if not text:
            continue
        print(f"当前段落的样式：{style}；当前段落的内容： {text}")

parse_docx_style("../../dataset/DOCX素材.docx")

"""
Heading 1 -----> 一级标题
Heading 2 -----> 二级标题
Heading 3 -----> 三级标题

Normal -----> 正文
"""



