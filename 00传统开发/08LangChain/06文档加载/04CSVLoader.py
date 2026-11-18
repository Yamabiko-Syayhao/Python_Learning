import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
from pathlib import Path
# TextLoader 纯文本加载器 专门读txt
from langchain_community.document_loaders import CSVLoader
"""
PyPDFLoader底层依赖第三方的包 pypdf 所以运行之前要先安装依赖
"""

csv_path = Path("../dataset/sample-simple.csv")
# autodetect_encoding=True 自动识别文件编码 避免中文乱码问题
loader = CSVLoader(str(csv_path),autodetect_encoding=True) # 实例化 CSV 加载器 传入文件路径对象
# 这里的默认行为是把整个 csv 表格中的每一行完整读取，每一行都会生成一个独立的document对象 表头除外，它被当成列名用掉了

# load() 一次性把内容读进内存 返回一个 document 列表
csv = loader.load()
print(f"该pdf文件被分成了{len(csv)}个document对象")

for i,Csv in enumerate(csv):
    # 元数据 存放行号 文件来源等溯源信息
    print(i,Csv.metadata)
    # 文本 把当前这一行列的名字以及此列所对应具体的每行的值拼接成一段可读文本 [列名：每行值]
    print(i,Csv.page_content)
