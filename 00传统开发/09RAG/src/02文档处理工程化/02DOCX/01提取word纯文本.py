# 使用 python-docx 库 可以精细读取段落样式 保留标题 段落 表格 图片等信息
# uv add python-docx
# 使用 docx2txt 提取 word 中的内容


# ======================= docx2txt的方法 =======================
# import docx2txt
# text = docx2txt.process(r"../../dataset/两界村 - demo.docx")
# print(text)

# ======================= python-docx Document 的方法 =======================
from docx import Document
# Document 对象用来获取文档的属性
def get_text(path):
    # 使用 Document 打开文档 创建文档对象
    doc = Document(path)
    # 定义列表 用于存储所有段落对象
    all_text = []
    # 遍历文档所有的段落
    for paragraph in doc.paragraphs:
        # 提取段落文本 去掉首尾空格添加到列表中
        all_text.append(paragraph.text.strip())
        # 将列表转为字符串拼接
    print("\n".join(all_text))
# 实际开发当中 文件名必须是英文 不要有空格等特殊字符 此处注意
get_text("../../dataset/两界村 - demo.docx")

# ======================= langchain 的方法 =======================
# from langchain_community.document_loaders import Docx2txtLoader
# from pathlib import Path
# # docx_path = Path("../../dataset/两界村 - demo.docx")
# loader = Docx2txtLoader("../../dataset/两界村 - demo.docx")
# docx = loader.load()
# # 对于 Docx2txtLoader 不论你的文字有多少页， 默认打包成一个 Document 对象 放在列表下标为0 的位置
# for doc in docx:
#     print(doc.page_content)
# # 或者
# print(docx[0].page_content)

# ======================= langchain 和 docx2txt 的方法适合快速预览
# ======================= python.docx 适合惊喜阅读
