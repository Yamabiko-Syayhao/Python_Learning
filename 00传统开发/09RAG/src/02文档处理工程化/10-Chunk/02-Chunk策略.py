# 导入文本加载器，用于读取本地txt文档
from langchain_community.document_loaders import TextLoader
# 路径工具类，方便管理文件路径
from pathlib import Path
# LangChain文档对象，承载文本+元数据
from langchain_core.documents import Document
# 固定字符分割器
from langchain_text_splitters import CharacterTextSplitter

# 定义知识库txt文件路径
txt_path = Path('../../dataset/智能客服平台知识库.txt')
# 实例化文本加载器，指定编码utf-8防止中文乱码
loader = TextLoader(str(txt_path), encoding='utf-8')
# 加载文档，得到Document列表
docs = loader.load()

# 固定长度分块 最直接,但不推荐单独使用
def chunk_by_len():
    """固定分隔符分块，简单粗暴，不推荐生产单独使用"""
    splitter = CharacterTextSplitter(
        separator='\n\n',  # 优先按 段落 分隔符 切分
        chunk_size=100,    # 每个块最大字符长度
        chunk_overlap=0    # 块之间不重叠
    )
    # 对文档执行分割，得到chunk列表
    chunks = splitter.split_documents(docs)
    # 打印切分后的块数量
    print(f"固定长度分块切分数: {len(chunks)}, 分块的内容: {chunks}")
# 调用
# chunk_by_len()
# 重叠分块 overlap
"""
为什么要重叠?
    防止关键信息正好 落在切割边界 被切断
    让相邻的 chunk 共享同一部分内容/目标答案, 保证上下文语义连续
经验之谈: overlap 一般 设置为 chunk_size 的 10% ~ 20%
"""

# 递归分块 RecursiveCharacterTextSplitter 最常用的
"""
先按 优先级 依次尝试分隔符段落 -> 句子 -> 词 -> 字符, 尽量在 '自然边界' 切, 最大限度的保留语义
"""
# 导入递归字符分割器，企业RAG最常用
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_by_recursive():
    """递归分块：按优先级分隔符依次切分，优先在语义断点切割"""
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""], # 分隔符优先级：段落>换行>空格>字符
        chunk_size=200,    # 块最大字符数
        chunk_overlap=100   # 相邻块重叠100字符，防止信息被切在边界 overlap 占了 50%，这明显偏高（经验值 10%~20%）。后果是索引冗余翻倍、相邻块大量重复。这里应该是演示用的夸张值，生产要降到 20~40
    )

    # 分割文档
    chunks = splitter.split_documents(docs)
    # 输出切分块总数
    print('递归切分数', len(chunks))
    # 遍历打印每一个chunk
    for doc in chunks:
        print(f"递归切分块内容: {doc.page_content}")

# chunk_by_recursive()
# print('=/=' * 30)

# 五. 按结构分块 markdown 标题感知
# 格式： 一级标题：   # 内容
# 导入Markdown标题分割器，可以识别# ## ###标题，自动按标题切分并携带标题元数据
from langchain_text_splitters import MarkdownHeaderTextSplitter

def chunk_by_markdown():
    """Markdown结构化分块：识别标题层级，按章节切分"""
    # 打开文件读取全部文本
    with open(txt_path, 'r', encoding='utf-8') as f:
        text= f.read()
    # 定义需要识别的markdown标题标记，和对应的元数据key
    headers_to_split_on = [('#', 'h1'), ('##', 'h2'), ('###', 'h3')]
    # 实例化markdown标题分割器
    md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    # 执行文本分割
    md_chunks = md_splitter.split_text(text)
    # 打印切分数量
    print(len(md_chunks))
    # 遍历每个markdown块
    for chunk in md_chunks:
        print(f'元数据', chunk.metadata)
        print(f'内容', chunk.page_content)
        print('*' * 30)

# chunk_by_markdown()

# 六. 语义切分 SemanticChunker 高级
"""
之前所学的 都是按 '格式' 切,而语义分块 是按 '意思' 切, 用 Embedding 计算 相邻句子的相似度,在  '语义发生 跳变' 的地方切开
优点: 边界 最符合语义
缺点: 慢 要调用 Embedding
"""
# 导入语义分割器
from langchain_experimental.text_splitter import SemanticChunker
# 通义千问Embedding
from langchain_community.embeddings import DashScopeEmbeddings, dashscope
# 读取.env环境变量文件
from dotenv import load_dotenv
# 加载环境变量，override=True覆盖已有环境变量
load_dotenv(override=True)

def chunk_by_semantic():
    """语义分块：根据句子向量相似度，语义发生变化处自动切分"""
    # 读取文档全部文本
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()
        # 导入os模块读取环境变量
        import os
        # 实例化语义分割器 原理：把文本按句子切开 → 每句算 embedding → 算相邻句相似度 → 相似度骤降处断开。percentile 表示“取相似度分布的第 95 百分位作为断点阈值”，即只在前 5% 最陡的下降处切
        semantic_splitter = SemanticChunker(
            embeddings=DashScopeEmbeddings(
                dashscope_api_key=os.getenv('DASHSCOPE_API_KEY'),  # 读取dashscope密钥
                # base_url='https://ws-bggm9k3qgbthz61a.cn-beijing.maas.aliyuncs.com/compatible-mode/v1', # 读取接口地址
                model="qwen3.7-text-embedding-flash"  # 使用的向量模型名称
            ),
            breakpoint_threshold_type='percentile',  # 断点判定策略：按相似度分位数找断点，默认95
            breakpoint_threshold_amount=90,
            sentence_split_regex=r'(?<=[。!？!\n])'
        )
        # chunks = semantic_splitter.split_documents(docs)
        # 对纯文本执行语义切分
        chunks = semantic_splitter.split_text(text)
        # 打印分块数量
        print(len(chunks))
        # 循环输出每个语义块
        for chunk in chunks:
            print(chunk)
            print('*' * 60)

# chunk_by_semantic()

# 七.父子分块 (Small-to Big)
"""
经典矛盾的 "两全方案":
    用 [小块] 做检索 -> 精准
    用小块对应的 [大块/父块] 喂给 LLM -> 语义完整
检索命中小块后, 回溯到它所在的父块 再生成答案
"""
def build_parent_child_chunks(text, parent_size=500, child_size=120):
    """
    先切父块（500），再在每个父块内部切子块（120），子块记录 parent 文本和 parent_id。
    构建父子分块结构: 小块用于检索, 大块用于生成
    parent_size: 父块大小 提供完整语义背景
    child_size: 子块大小 更容易命中关键词
    """
    """
    RecursiveCharacterTextSplitter 并不是简单的在第500个字符出 暴力截断,是递归的尝试按照 separators列表中的的分隔符去切分,
    尽量在接近 chunk_size 的地方找到合适的语义边界(比如段落 换行 句号等).
    在极端情况下(比如一段特别 long long long 的的文本内容既没有换行也没有标点符号),仍然可能发生一个句子被拆到两个父块中的情况.
    这确实会导致两个父块各自语义不完整,进而影响子块和最终答案的质量, 所以在实际操作时,可以考虑给 overlap 20~50的一个覆盖区间(500 * 10% = 50)
    """
    # 父块分割器：父块之间无重叠，每个父块是独立完整语义单元
    parent_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""], chunk_size=parent_size, chunk_overlap=0)
    # 子块分割器：在父块内部切割，设置overlap，防止关键词切在边界
    child_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""], chunk_size=child_size, chunk_overlap=20)
    # 第一步：全文切分成父块
    parent_chunks = parent_splitter.split_text(text)
    # 创建映射列表：存储子块到父块的关联关系
    mapping = []
    # 遍历每一个父块，携带父块序号
    for p_idx, p_chunk in enumerate(parent_chunks):
        # 将当前父块文本切分为多个子块
        child_chunks = child_splitter.split_text(p_chunk)
        # 遍历子块，建立父子映射关系
        for c_chunk in child_chunks:
            mapping.append({
                'child': c_chunk, # 小块, 用于向量检索, 存储到向量数据库
                'parent': p_chunk, # 大块, 用于喂给 LLM 生成答案
                'parent_id': p_idx # 父块唯一编号，也可以换成hash
            })
    # 返回父子分块映射结果
    return mapping
# 打开文件, 读取全部文本
# with open(txt_path, 'r', encoding='utf-8') as f:
#     text = f.read()
#     # 分块
#     res = build_parent_child_chunks(text)
#     for i, chunk in enumerate(res):
#         print(f"第{i+1}个子块：{chunk}")
#         print('*' * 60)

# 八. chunk 大小如何选择
"""
经验区间---前提是文档经过清洗后的纯文本：
 | 文档类型       | chunk_size   | overlap  | 说明                  |
 | ----------- | ---------- | ------- | ------------------- |
 | FAQ / 问答    | 100-300       | 0-30     | 一问一答，本身就短        |
 | 通用文档/手册   | 300-600       | 50-100  | 最通用区间               |
 | 长文/论文/合同  | 500-1000      | 100     | 需要更多上下文            |
 | 代码          | 按函数/类切     | -       | 用代码感知 splitter      |
 | 表格          | 整表或整行      | -       | 不能从中间切表格           |

选型总结：
    模型上下文越长 → chunk 可以越大
    希望问答越精确 → chunk 越小
    实在不确定 → 先用 RecursiveCharacterTextSplitter(500, 50)
"""
# 结构分块 + 递归分块”的标准组合
class ChunkProcessor:
    """分块处理器: 结构分块 + 递归分块 双层策略"""
    def __init__(self, chunk_size=500, overlap=50):
        # 初始化markdown标题分割器，识别三级标题
        self.md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[('#', 'h1'), ('##', 'h2'), ('###', 'h3')])
        # 初始化递归分割器，设置块大小与重叠长度
        self.recursive_splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', '。', '？', '！', '，'],
            chunk_size=chunk_size,
            chunk_overlap=overlap
        )

    def split(self, markdown_text, base_metadata=None):
        """双层分块入口函数：先按标题切章节，章节内部再递归分块"""
        # 如果基础元数据为空，赋值空字典
        base_metadata = base_metadata or {}
        # 第一层：按markdown标题切分出各个章节
        sections = self.md_splitter.split_text(markdown_text)
        # 保存最终生成的Document对象列表
        final_docs = []
        # 遍历每一个标题章节
        for section in sections:
            # 拼接标题路径 h1>h2>h3，作为上下文前缀，增强检索语义
            title_path = '>'.join(v for k, v in section.metadata.items() if k.startswith('h'))
            # 第二层：对章节内部文本递归切分
            sub_chunks = self.recursive_splitter.split_text(section.page_content)
            # 遍历章节内所有子块
            for idx, chunk in enumerate(sub_chunks):
                if len(chunk.strip()) < 10: # 质量过滤，丢弃太短无效文本
                    continue
                # 复制基础元数据，防止修改原字典
                meta = dict(base_metadata)
                # 合并当前章节的标题元数据
                meta.update(section.metadata)
                # 新增标题路径字段
                meta['title'] = title_path
                # 记录当前块序号和字符长度
                meta['chunk_idx'] = f'{idx}_{len(chunk)}'
                # 将标题前缀拼接到chunk正文，向量编码时带上主题信息
                content = f'{title_path}\n{chunk.strip()}'
                # 组装LangChain Document对象，加入结果集
                final_docs.append(Document(metadata=meta, page_content=content))
        # 返回全部处理完成的文档块
        return final_docs
