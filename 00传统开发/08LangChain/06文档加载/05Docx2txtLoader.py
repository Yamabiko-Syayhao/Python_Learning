import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
from pathlib import Path
# Docx2txtLoader word文档加载器 专门读.docx文件
from langchain_community.document_loaders import Docx2txtLoader
"""
底层依赖 docx2txt 运行前需要安装
只能读取新版docx文件 之前的老式后缀.doc （office2003）无法解析
"""

docx_path = Path("../dataset/demo.docx")
# autodetect_encoding=True 自动识别文件编码 避免中文乱码问题
loader = Docx2txtLoader(str(docx_path)) # 实例化 word 加载器 传入字符串格式文件对象
# 这里的默认行为是把整个 word 完整读取，生成一个独立的document对象

# load() 一次性把内容读进内存 返回一个 document 列表
docx = loader.load()
print(f"该 word 文件被分成了{len(docx)}个document对象")

# 判断文段列表是否为空
if docx:
    for Docx in docx:
        # 元数据 存放文件路径等溯源信息
        print(Docx.metadata)
        # docx全部正文文本
        print(Docx.page_content)
