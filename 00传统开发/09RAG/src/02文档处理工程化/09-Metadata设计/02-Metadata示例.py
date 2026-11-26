# 导入时间模块，用于获取、格式化文件时间
from datetime import datetime
# 导入哈希模块，用于生成文档唯一ID
import hashlib
# 导入操作系统模块，获取文件属性、路径信息
import os
# "如何给 RAG 系统里的文档打上规范的'标签'（Metadata）"，让文档在向量库里不仅能"按语义搜"，还能"按部门/权限/时间/来源精准筛"，并且回答能带出处、能控权限
# =====================================================
# 二、企业 Metadata 标准字段体系 通俗理解：这就是"标签模板"，后面所有代码都在按这个模板填内容
""" 企业 RAG 推荐的标准元数据字段（按需裁剪）：
【来源类】 这个文件从哪来，第几页
    doc_id          文档唯一ID
    source          文件名/URL
    file_type       pdf/docx/html...
    page            页码
    chunk_index     第几个分块
【业务类】 这个文件属于哪个部门，什么分类
    title           所属标题/章节
    category        文档分类（合同/手册/FAQ）
    dept            归属部门
    tags            业务标签
【权限类】 谁能看？是公开的还是内部的，还是机密的
    access_level    密级（public/internal/secret） 加密等级
    公开（官网）  内部（OA）  私有（财务部门）
    allowed_roles   可访问角色列表
    公司：员工--经理（部门领导）---总经理---老板
【时间类】 这个文件什么时候写的，是第几版
    created_at      创建时间
    updated_at      更新时间
    version         版本号
【质量类】 这切片多长 什么语言
    lang            语言（zh/en）
    char_count      字符数
"""

# =====================================================
# 三、自动提取文件级 Metadata
# 业务背景 每次入库一个文档，如果人工手动填标签会累死的 所以系统需要从文件本身自动提取一些基础信息
""" 文件入库时，先提取一批"文件级"通用元数据。 """
# 给定一个文件路径，自动读出它的基本信息。
def extract_file_metadata(file_path):
    """从文件路径自动提取元数据
    :param file_path: 文档完整路径
    :return: 文件级元数据字典
    """
    # 获取文件状态信息，文件不存在则赋值None os.stat() 读取操作系统文件创建时间
    stat = os.stat(file_path) if os.path.exists(file_path) else None
    # 获取纯文件名（不含前面路径）
    filename = os.path.basename(file_path)

    return {
        # 对文件路径md5，截取前12位作为文档唯一ID 同一路径永远同一 ID，方便更新/删除
        "doc_id": hashlib.md5(file_path.encode()).hexdigest()[:12],
        "source": filename,
        # 取后缀名并转小写，作为文件类型
        "file_type": filename.split(".")[-1].lower(),
        "created_at": (
            # 读取文件创建时间，格式化成年-月-日
            datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d")
            if stat else datetime.now().strftime("%Y-%m-%d")
        ),
    }

# 测试：提取示例文档元数据
print(f'提取示例文档元数据：{extract_file_metadata("../../dataset/产品手册_v2.pdf")}')

# =====================================================
# 四、从文件名/路径推断业务 Metadata
# 企业里面的知识库通常是按文件夹整理的
# 所以我们可以直接从路径当中提取出部门和加密的等级
""" 企业实践：用目录结构和命名规范，自动推断部门、密级。
比如路径 /knowledge/销售部/internal/话术.docx
"""
# 部门名称映射：中文目录名 → 英文标识
DEPT_MAP = {"销售部": "sales", "产品部": "product", "技术部": "tech"}
# 密级映射：目录标识 → 密级字段值
LEVEL_MAP = {"public": "public", "internal": "internal", "secret": "secret"}

def infer_business_metadata(file_path):
    """从路径推断部门和密级
    :param file_path: 文件路径
    :return: 业务元数据字典（部门、密级）
    """
    # 设置默认值：未知部门，内部文档
    meta = {"dept": "unknown", "access_level": "internal"}
    # 按路径分隔符拆分目录
    parts = file_path.split("/")
    # 遍历每一段目录名称
    for part in parts:
        # 如果目录名匹配部门，更新dept
        if part in DEPT_MAP:
            meta["dept"] = DEPT_MAP[part]
        # 如果目录名匹配密级，更新access_level
        if part in LEVEL_MAP:
            meta["access_level"] = LEVEL_MAP[part]
    return meta

# 测试：根据路径推断业务元数据
print(f'根据路径推断业务元数据：{infer_business_metadata("/knowledge/销售部/secret/话术.docx")}')

# =====================================================
# 五、给 Chunk 注入 Metadata（核心） 给每个 Chunk 贴标签
""" 分块时，把"文件级元数据" + "Chunk 级元数据"合并注入。
title 字段尤其重要：让 chunk 携带它所属的标题上下文。
"""
def build_chunks_with_metadata(chunks, file_meta, title=""):
    """给每个 chunk 注入完整元数据
    :param chunks: 纯文本分块列表
    :param file_meta: 文件级基础元数据
    :param title: 当前分块所属章节标题
    :return: 带文本+完整元数据的chunk列表
    """
    result = []
    # 遍历分块，同时拿到序号
    for idx, chunk_text in enumerate(chunks):
        # 复制文件元数据，避免原字典被修改 继承了文件级的标签
        meta = dict(file_meta)
        # 追加chunk独有的元数据字段
        meta.update({
            "chunk_index": idx,             # 第几块
            "title": title,                 # 所属章节标题
            "char_count": len(chunk_text),  # 当前分块字符长度
            "lang": detect_lang(chunk_text),# 文本语言  detect_lang() 统计中文字符占比 这个方法定义在了下面
        })
        # 将文本和元数据打包存入结果列表
        result.append({"text": chunk_text, "metadata": meta})
    return result

def detect_lang(text):
    """简易语言检测：统计中文字符占比判断中文/英文
    :param text: 待检测文本
    :return: zh 中文 / en 英文
    """
    import re
    # 匹配所有中文字符并统计数量
    zh = len(re.findall(r"[\u4e00-\u9fa5]", text))
    # 中文字符超过总长度30%判定为中文，否则英文
    return "zh" if zh > len(text) * 0.3 else "en"

# =====================================================
# 六、转 LangChain Document（带 metadata）天生有两个字段：page_content（文本）+ metadata（标签）。把上一步的字典塞进去。
""" LangChain 的 Document 天然支持 metadata 字段。 """
# 导入LangChain文档对象
from langchain_core.documents import Document

def to_documents(chunks_with_meta):
    """把带元数据的chunk转为LangChain Document对象
    :param chunks_with_meta: 带元数据的chunk列表
    :return: LangChain Document列表
    """
    # 列表推导式循环生成Document实例
    return [Document(page_content=item["text"], metadata=item["metadata"]) for item in chunks_with_meta ]

# =====================================================
# 七、Metadata 的三大作用（结合向量库）
# --- 作用1：元数据过滤检索（最常用）---
""" 检索时先按元数据缩小范围，再做向量相似度。
比如只在"销售部 + 近三个月"的文档里检索。
"""
# Chroma 向量库查询示例代码
# results = vectorstore.similarity_search(
#     query="退款政策",
#     k=5,
#     filter={"dept": "sales", "access_level": "internal"}  # 元数据过滤条件 只在销售部的内部文档去检索
# )

# --- 作用2：来源溯源（回答带引用）---
""" 回答末尾标注来源，提升可信度，是企业 RAG 标配。 """
def format_citation(doc):
    """生成文档引用信息
    :param doc: LangChain Document对象
    :return: 格式化的来源引用字符串
    """
    m = doc.metadata
    # 获取来源文件名与页码，无页码则显示'-'
    return f"【来源：{m.get('source')} 第{m.get('page', '-')}页】"

# --- 作用3：权限过滤（数据安全）---
""" 检索结果按用户角色过滤，看不到无权限的内容。 """
def filter_by_permission(docs, user_roles):
    """按用户角色过滤检索结果，实现权限控制
    :param docs: 向量检索返回的文档列表
    :param user_roles: 当前用户角色列表
    :return: 用户有权查看的文档列表
    """
    allowed_docs = []
    # 遍历检索到的文档
    for doc in docs:
        # 获取文档密级，默认内部文档
        level = doc.metadata.get("access_level", "internal")
        # 公开文档任何人可见
        if level == "public":
            allowed_docs.append(doc)
        # 内部文档，员工角色可访问
        elif level == "internal" and "employee" in user_roles:
            allowed_docs.append(doc)
        # 机密文档，经理角色才可访问
        elif level == "secret" and "manager" in user_roles:
            allowed_docs.append(doc)
    return allowed_docs

# =====================================================
# 八、Metadata Schema 设计（Pydantic）
""" 用 Pydantic 定义 Metadata 结构，保证字段规范、可校验。
生产环境强烈推荐，避免脏数据进库。 """
# 导入Pydantic基础模型与字段工具
from pydantic import BaseModel, Field
# 导入类型注解
from typing import List, Optional

class ChunkMetadata(BaseModel):
    """企业级 Chunk 元数据 Schema，自动校验字段类型"""
    doc_id: str                               # 文档唯一ID
    source: str                               # 文档来源文件名
    file_type: str                            # 文件类型 pdf/docx
    page: Optional[int] = None                # 页码，可选字段
    chunk_index: int = 0                      # 当前分块序号，默认0
    title: str = ""                           # 所属章节标题，默认空字符串
    category: str = "general"                 # 文档分类，默认通用
    dept: str = "unknown"                     # 归属部门，默认未知
    access_level: str = "internal"            # 密级，默认内部文档
    # default_factory 默认值工厂 工厂模式 保证每次都生成一个全新的列表
    allowed_roles: List[str] = Field(default_factory=lambda: ["employee"]) # 允许访问角色，默认员工
    created_at: str = ""                      # 文档创建时间
    version: str = "v1"                       # 文档版本，默认v1
    lang: str = "zh"                          # 文本语言，默认中文
    char_count: int = 0                       # chunk字符数量

# 使用示例：实例化元数据对象
meta = ChunkMetadata(
    doc_id="a1b2c3",
    source="产品手册.pdf",
    file_type="pdf",
    page=12,
    title="第三章 部署方式",
    dept="product",
    access_level="internal",
)
# 转为字典打印
print(f"打印字典：{meta.model_dump()}")

# =====================================================
# 九、示例：文件 → 带元数据的 Documents
""" 把前面所有步骤串起来。 """
def process_with_metadata(file_path, chunks, title=""):
    """完整流程：提取元数据 → 注入 chunk → 转 Document
    :param file_path: 文件路径
    :param chunks: 分块文本列表
    :param title: 当前分块所属章节标题
    :return: LangChain Document列表（携带完整元数据）
    """
    # 提取基础文件元数据
    file_meta = extract_file_metadata(file_path)
    # 合并推断得到的业务元数据 从文件路径去推断业务标签
    file_meta.update(infer_business_metadata(file_path))
    # 将元数据注入每一个chunk
    chunks_with_meta = build_chunks_with_metadata(chunks, file_meta, title)
    # 转换为LangChain文档对象返回
    return to_documents(chunks_with_meta)

# 主程序入口测试代码
if __name__ == "__main__":
    demo_chunks = ["本产品支持私有化部署。", "提供 7x24 技术支持。"]
    docs = process_with_metadata(
        "/knowledge/产品部/internal/手册.pdf",
        demo_chunks,
        title="部署说明"
    )
    for d in docs:
        print(f"文档元数据：{d.metadata}")

# =====================================================
# 十、Metadata 设计经验总结
"""
1. 字段要"够用就好"：不是越多越好，过多增加维护成本
2. 一定要有 doc_id + chunk_index：方便溯源、更新、删除
3. 权限字段从第一天就设计：后补极其痛苦
4. 用 Schema 校验：杜绝脏元数据进库
5. 时间字段统一格式：方便范围过滤 yyyy-MM-dd hh:mm:ss  (看需求）
6. 向量库要支持元数据过滤：Milvus/Chroma/PgVector 都支持
7. title 注入 chunk：极大提升检索语义（下一节 Chunk 策略会再讲）
"""
