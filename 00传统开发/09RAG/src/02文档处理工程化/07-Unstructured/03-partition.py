
# ===================== 1 自动识别读取文档 =====================
# 导入自动分区函数，自动识别文件类型解析文档
from unstructured.partition.auto import partition

# 自动识别：传 pdf 用 pdf 解析器，传 docx 用 docx 解析器
# partition 是自动分发器 如果传的是 pdf 文件就会走 pdf 解析器，如果传的是 docx 文件，那么就走 docx 解析器
# PDF：strategy 决定解析策略
#   "fast"      纯文本，快
#   "hi_res"    高精度，带版面分析+表格识别（需要模型）慢但是准
#   "ocr_only"  纯 OCR（扫描件）
# 自动识别文档
elements = partition(
    filename="../../dataset/标题提取.pdf",
    strategy="hi_res",
    # 语言指定简体中文，避免解析错误
    languages=["chi_sim"]
)
# 循环遍历前10个文档元素 读取文档
for el in elements:
    # category：元素类型；text：文本内容
    print(f"[{el.category}] {el.text}")

print("="*50)

# ================= 2 Element 元素类型体系（核心概念）=================
# partition 返回的不是字符串 是 Element 对象列表 每个元素待语义类
"""
Unstructured 把文档拆成语义元素，常见类型：
    Title           标题
    NarrativeText   正文段落
    ListItem        列表项
    Table           表格
    Image           图片
    Header/Footer   页眉页脚
    PageBreak       页码
    Address/EmailAddress  地址/邮箱
这正是 RAG 需要的：按语义而非按字符处理。
"""
# 导入Counter用于统计各类元素数量
from collections import Counter
# 统计文档里各类元素的数量
type_count = Counter(el.category for el in elements)
print("元素类型分布：", type_count)
print("="*50)


# ================= 3 按元素类型结构化处理 =================
"""
企业实践：不同类型元素区别对待。
比如标题用来建目录，表格转 markdown，正文做 chunk。
"""
# 初始化列表，分别存放标题、表格、正文
titles = []
tables = []
texts = []
# 遍历所有解析元素
for el in elements:
    if el.category == "Title":
        titles.append(el.text)  # 收集标题文本
    elif el.category == "Table":
        # 表格可以拿到 HTML 结构
        html = el.metadata.text_as_html
        tables.append(html)
    elif el.category == "NarrativeText":
        texts.append(el.text)  # 收集正文文本
print("标题数：", len(titles))
print("表格数：", len(tables))
print("正文段数：", len(texts))
print("=" * 50)

# =============  4 Metadata 元数据（RAG 溯源 关键）=======================
""" 每个元素都带 metadata，企业 RAG 用它做：
    来源溯源（哪个文件、第几页）
    权限过滤
    引用展示
"""
# 遍历个元素，打印元数据信息
for el in elements:
    meta = el.metadata  # 获取当前元素元数据对象
    print({
        "filename": meta.filename,  # 原始文件名
        "page": meta.page_number,  # 当前元素所在页码
        "filetype": meta.filetype,  # 文件类型
    })
print("="*50)

# =============== 5 智能分块 chunk_by_title（强烈推荐）====================
""" 普通分块按字数硬切，会把一段话切两半。
 chunk_by_title 按"标题"语义边界分块：
    同一标题下的内容聚到一个 chunk
    更符合语义，检索质量更高
"""
# 导入基于标题的智能分块函数
from unstructured.chunking.title import chunk_by_title

# 执行语义分块
chunks = chunk_by_title(
    elements,
    max_characters=1000,  # 每个 chunk 最大字符数上限
    combine_text_under_n_chars=100,  # 小于该长度的小段文本自动合并 避免出现碎片化的分块
    new_after_n_chars=800,  # 软阈值，超过尽量新建块
)
print("分块数量：", len(chunks))
# 循环打印分块
for c in chunks:
    print("-" * 40)
    print(c.text)

#  ==================== 转 LangChain Document（无缝对接 RAG） ====================
""" Unstructured 负责"解析+分块"，
 LangChain 负责"检索+生成"，二者天然配合。 """
# 导入LangChain文档对象，RAG载体
from langchain_core.documents import Document
def to_langchain_docs(chunks):
    """Unstructured chunks → LangChain Document
    :param chunks: unstructured分块结果列表
    :return: langchain Document列表
    """
    docs = []  # 初始化文档列表
    for c in chunks:
        docs.append(Document(
            page_content=c.text,  # 存入分块文本内容
            metadata={  # 元数据字典
                "source": c.metadata.filename,  # 文件来源
                "page": c.metadata.page_number,  # 页码
                "role": ['financial', 'boss']  # 自定义业务元数据
            }
        ))
    return docs
# 将分块转为LangChain文档对象
lc_docs = to_langchain_docs(chunks)
print("LangChain 文档数：", len(lc_docs),lc_docs)
print(lc_docs[0].page_content)

