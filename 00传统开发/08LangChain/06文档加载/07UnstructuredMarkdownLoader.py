"""
结构化文档 Excel CSV 数据库的表  这些具备固定行列结构，数据库格式规整
非结构化文档 MarkDown pdf word txt 这些是排版自由灵活，没有固定性表格格式
"""

# UnstructuredMarkdownLoader 专门解析 MarkDown 非结构化的文档加载器
from pathlib import Path
from langchain_community.document_loaders import UnstructuredMarkdownLoader
"""
底层依赖 unstructured 包     这个包很大，能解析几十种文件格式
"""

md_path = Path("../dataset/环境变量配置.md")

loader = UnstructuredMarkdownLoader(str(md_path)) # 实例化 md 加载器 传入字符串格式文件对象
# 整篇 md 文档完整读取，生成一个独立的document对象

# load() 一次性把内容读进内存 返回一个 document 列表
md = loader.load()
print(f"该 word 文件被分成了{len(md)}个document对象")

# 判断文段列表是否为空
if md:
    for MD in md:
        # 元数据 存放文件路径等溯源信息
        print(MD.metadata)
        # docx全部正文文本
        print(MD.page_content)
"""
将文档能加载成一个document对象加载器
TextLoader Docx2TxtLoader UnstructuredMarkdownLoader
将一个页面作为一个document对象
WebBseLoader
将文档按照每一行加载的，每一行都是一个 document 对象
CSVLoader
将文档按照页数加载 每个页面都是一个document对象
PyPDFLoader
"""