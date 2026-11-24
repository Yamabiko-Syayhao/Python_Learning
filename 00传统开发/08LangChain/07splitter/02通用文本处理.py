from langchain_core.documents import Document
"""
RecursiveCharacterTextSplitter 递归字符文本分割器
通用场景下的默认首选的分割器 
此文本切割器的切割逻辑是由大到小，逐级尝试的分割
优先使用段落分割符切割，如果切片还是超过了长度限制，就可以用换行或者空格，最后还是不行
话可以单个字符硬切
一定要保证每段的文字不超过 chunk_size （每小段文字限制）
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter
# 测试文本1：结构完整的段落文字 正常文本
text1 = """
周六午后，街道活动室开展了一场零基础数据库入门公益课。第一部分讲师讲解数据表、查询语句与基础关联逻辑；第二部分学员两两搭档动手编写简易数据操作脚本；第三部分各组依次展示成品，交流实操心得。课堂里有着三类学习心态的学员：1.务实进阶型：打算三个月内熟练数据库操作，日常高效处理业务数据。2.好奇认知型：先摸清数据库实际用途，结合自身需求再规划学习深度。3.实操落地型：只想立刻解决身边琐事，比如统计台账、归类存储本地文件。授课老师也给出通俗易懂的学习方向：先上手实操案例，再夯实理论知识；先实现基础功能，再打磨细节优化；先保持定期练习稳步积累，后续再钻研高阶复杂用法。
"""

# 测试文本2：无标点超长字符串，用来测试强制硬切逻辑 极端文本
text2 = """
这是一段非常非常非常非常非常非常非常非常非常非常非常非常非常非常非1常非
常非常非常非常非常非常非常非常非2常非常非常非常非常非常非常非常3非常非常非常非常非常非
常非5常非常非常非常非常非常非7常非常非常非常非常非常非常非常非常非常非常非常非常8非常非常非常
非常非常非常非常99非常非常非常非常00非常非常非常非常非常非常非常非常非常54非常非常非常非常非常非8
8常非常非常非常非常非常非常非常非常非54常非常长的文本
"""

# 初始化递归分割器（也就是设定一些参数）
splitter = RecursiveCharacterTextSplitter(
    separators=['\n\n','\n',' ',''], # 切割优先级 即 段落 换行 空格 字符
    # \n\n 双连续换行代表段落
    chunk_size=120, # 单块最大字符数
    chunk_overlap=30, # 相邻分片重叠字符数 为了保护上下文的完整性
    length_function=len, # 用 len() 按照字符数计算长度
    is_separator_regex=False, # 设为 False 分割符作为普通字符串匹配
    # 如果设为 True 则代表按照正则表达式的方式处理（匹配）
)
"""
split_text() 输入原始字符串，输出切割后的纯文本列表 适合调试查看切分效果 没有溯源信息

create_documents() 输入字符串列表 再加上你自己定义的 metadata ,
批量生成Document对象

split_documents() 接收已经加载完成的 Document 对象，切割后自动继承原始 metadata
    业务当中最常用 文本加载器读完了文档 都是 document 对象 然后 split_document 切块
    溯源信息不会丢失
"""
# -------------------- 方式1：split_text 只切了纯的字符串 用于调试查看切分效果
# Chunk = splitter.split_text(text1)
# for index, chunk in enumerate(Chunk):
#     print(f"{index}======{chunk}")

# -------------------- 方式2：create_documents 批量从文本创建 document
# metadata 最重要的作用是追溯来源 可以从中得知你的文本来自哪个文件，第几页之类的信息
# Doc = splitter.create_documents(
#     [text1, text2],
#     # 自定义的 metadata
#     metadatas=[
#         {"source":"text1","topic":"测试素材1"},
#         {"source":"text2","topic":"测试素材2"}
#     ]
# )
# for doc in Doc:
#     print(doc.metadata)
#     print(doc.page_content)

# -------------------- 方式3：用 split_documents 切割
# 模拟 loader 读取之后得到的原始文档（document）对象
raw_docs = [
    Document(page_content=text1,metadata={"source":"text1","topic":"测试素材1"}),
    Document(page_content=text1,metadata={"source":"text2","topic":"测试素材2"}),

]
Doc = splitter.split_documents(raw_docs)
# 切分之后每一个小分片都会继承父文档当中的 metadata 溯源信息
for doc in Doc:
    print(doc.metadata)
    print(doc.page_content)
