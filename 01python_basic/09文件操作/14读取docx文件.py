# python-docx
from docx import Document

# 打开word文档
doc = Document("utils/cs.docx")

# 读取段落文字
content = ""
for i in doc.paragraphs:
    content += i.text + "\n"
print(f"读取到的word内容是{content}")









