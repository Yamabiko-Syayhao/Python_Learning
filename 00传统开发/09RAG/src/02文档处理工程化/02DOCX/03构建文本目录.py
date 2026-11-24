from docx import Document

def build_catalog(path):
    doc = Document(path)
    toc_tree = []
    for paragraph in doc.paragraphs:
        style = paragraph.style.name
        text = paragraph.text.strip()
        if not text:
            continue
            # 如果段落的样式名称中有 Heading 标题
        if "Heading" in style:
            # 将内容和标题的等级添加到目录树中
            toc_tree.append({
                "title": text,
                "level": style
            })
    for i in toc_tree:
        print(i)

build_catalog("../../dataset/DOCX素材.docx")