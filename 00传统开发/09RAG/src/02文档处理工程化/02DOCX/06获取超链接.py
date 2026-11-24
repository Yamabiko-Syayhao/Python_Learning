from docx import Document
import os

def get_href(path):
    # 1.创建文档对象
    doc = Document(path)
    # 2.获取文档资源
    rels = doc.part.rels
    # 准备一个空列表 存超链接
    links = []
    # 循环遍历文档当中所有的资源
    for rel in rels.values():
        # 3.筛选超链接资源
        if "hyperlink" in rel.reltype:
            links.append(rel.target_ref)
    for link in links:
        print(link)
# 微软的 word保存的文件 可以提被提取到超链接 而如果换成 wps 的就不行 因为二者内部保存的超链接的格式是不一样的
get_href("../../dataset/Docx素材_ms.docx")


