"""
CharacterTextSplitter 简单字符分割器
只依靠单个固定的分割符切割文本 默认使用‘ \n\n ’（段落）进行切分
规则强硬，没有“切完还太长就换个符号继续切”的备选策略
"""
from langchain_text_splitters import CharacterTextSplitter
# 测试文本1：结构完整的段落文字 正常文本
text1 = """
周六午后，街道活动室开展了一场零基础数据库入门公益课。第一部分讲师讲解数据表、查询语句与基础关联逻辑；第二部分学员两两搭档动手编写简易数据操作脚本；第三部分各组依次展示成品，交流实操心得。
课堂里有着三类学习心态的学员：
1.务实进阶型：打算三个月内熟练数据库操作，日常高效处理业务数据。
2.好奇认知型：先摸清数据库实际用途，结合自身需求再规划学习深度。
3.实操落地型：只想立刻解决身边琐事，比如统计台账、归类存储本地文件。
授课老师也给出通俗易懂的学习方向：
先上手实操案例，再夯实理论知识；先实现基础功能，再打磨细节优化；先保持定期练习稳步积累，后续再钻研高阶复杂用法。
"""
# 初始化简单字符分割器（也就是设定一些参数）
splitter = CharacterTextSplitter(
    separator='\n', # 唯一指定的切割标记 也就是只能设定一个切割模式
    # \n\n 双连续换行代表段落
    chunk_size=50, # 单块最大字符数
    chunk_overlap=20, # 相邻分片重叠字符数 为了保护上下文的完整性
    length_function=len, # 用 len() 按照字符数计算长度
    is_separator_regex=False, # 设为 False 分割符作为普通字符串匹配
    # 如果设为 True 则代表按照正则表达式的方式处理（匹配）
)
# 根据文本列表及自定义的源数据生成 Document 分片对象
Doc = splitter.create_documents(
    [text1],
    metadatas=[
        {
            "source":"text1",
            "topic":"bs111"
        }
    ]
)
for doc in Doc:
    print(doc.metadata)
    print(doc.page_content)
