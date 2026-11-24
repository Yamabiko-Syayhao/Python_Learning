import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
from pathlib import Path
# TextLoader 纯文本加载器 专门读txt
from langchain_community.document_loaders import PyPDFLoader
"""
PyPDFLoader底层依赖第三方的包 pypdf 所以运行之前要先安装依赖
"""

pdf_path = Path("../dataset/Python文档.pdf")
loader = PyPDFLoader(pdf_path) # 实例化PDF加载器 传入文件路径对象
# 这里的默认行为是把整个pdf中的每一页完整读取，每一页都会生成一个独立的document对象

# load() 一次性把内容读进内存 返回一个 document 列表
pdf = loader.load()
print(f"该pdf文件被分成了{len(pdf)}个document对象")

for i,Pdf in enumerate(pdf):
    print(i,Pdf)
    # 输出的解释：
    # page_content 是文件的文本内容 整个 pdf 的正文
    # metadata 是元数据 记录这个文档来自哪个文件  溯源 metadata={'producer': 'Skia/PDF m149', 'creator': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36', 'creationdate': '2026-07-27T08:13:12+00:00', 'title': 'Python 教程 — Python 3.14.6 文档', 'moddate': '2026-07-27T08:13:12+00:00', 'source': '..\\dataset\\Python文档.pdf', 'total_pages': 4, 'page': 3, 'page_label': '4'}

