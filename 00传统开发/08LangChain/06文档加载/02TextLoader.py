# 用 langchain 中的 TextLoader把一个 txt 文件读进来 变成一个标准的文档对象（document对象）
# 屏蔽废弃类的警告
import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

# py自带的路径工具 用它拼路径 比手写字符串
from pathlib import Path
# TextLoader 纯文本加载器 专门读txt
from langchain_community.document_loaders import TextLoader

text_path = Path("../dataset/text_demo.txt")
print(text_path,type(text_path)) # text_path 不是字符串 是path路径对象 <class 'pathlib.WindowsPath'>

loader = TextLoader(str(text_path),encoding="utf-8") # 实例化文本加载器 参数1:str 必须把 text_path 对象转为字符串
# 参数2:防止中文乱码（encoding）
# 这里的默认行为是把整个txt完整读取，生成单个document对象 不会自动切分

# load() 一次性把内容读进内存 返回一个 document 列表
txt = loader.load()
print(f"读取到了{len(txt)}个document对象")
print(txt)
print(type(txt))

for i,txt in enumerate(txt):
    print(f" txt 中包含了哪些属性？===",txt)
    # 输出的解释：
    # page_content 是文件的文本内容 整个txt的正文
    # metadata 是元数据 记录这个文档来自哪个文件  溯源 metadata={'source': '..\\dataset\\text_demo.txt'}

