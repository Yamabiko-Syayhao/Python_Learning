"""
此分割是按照 token 数量分割 而不是字符长度
适用场景：严格控制 Embedding / LLM 的 token 上限 防止输入超限报错
通常搭配 tiktoken(openai官方分词工具) 计算真实token

业务报错：
chunk 太大 ----->超出模型上下文窗口，请求报错或者被截断
chunk 太小 ----->语义破碎，向量检索不准确

生产方案：先给定 token 预算，直接按照 token 做切分

"""
import tiktoken
from langchain_text_splitters import TokenTextSplitter

# 测试文本
text = """ 在生产环境中,很多团队会先检索再让模型回答用户问题
如果文档切分过大,可能会超过模型上下文窗口,如果切分过小,会损失语义的完整性
所以常见做法: 先规定好token 预算数据,再用TokenTextSplitter切分
Embedding模型通常也是有最大输入token, 为了避免超量报错,一般会把chunk限制在一个保守范围内,比如300~1000
,后续再根据检索效果进行参数调整 """

# 加载分词器（tiktoken）
# cl = ChatLanguage 100k=词表规模大约10万 base=基础编码器
encoding_name = "cl100k_base" # cl100k_base 是 GPT4/3.5 使用的分词器
# get_encoding() 拿到这个分词器对象 后边会用他将文本变成 token 序列 数出来
# 真实的 token 数
encoding = tiktoken.get_encoding(encoding_name)
splitter = TokenTextSplitter(
    encoding_name=encoding_name,
    chunk_size=80, # 每个分片最大的 token 数量
    chunk_overlap=20, # 分片之间重叠 token 保留上下文连贯性
)
# 生成 Document 对象 并且附带溯源信息

Tok = splitter.create_documents(
    [text],
    metadatas=[
        {"source":"text","topic":"测试文本"},
    ]
)

for tok in Tok:
    print(tok.metadata)
    print(tok.page_content)
    # 查看真实的 token 数
    print(len(encoding.encode(tok.page_content)))