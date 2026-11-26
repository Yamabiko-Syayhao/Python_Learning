""" Chunk 分块 是 RAG 中 投入产出比 比较高的一种优化手段
为什么 分块非常重要/关键
    Embedding 模型有长度上限 512、8192 token
    检索的最小单位是 chunk， 切错了 召回了错的内容
    chunk 太大 -> 噪音多, token贵, 答案被稀释
    chunk 太小 -> 语义不完整, 上下文丢失


- 固定长度分块 CharacterTextSplitter
- 重叠分块 overlap 的意义  核心作用只有一个：防止关键语义恰好被切在边界上而完全丢失。让相邻 chunk 共享一段文本，使得被切断的句子或知识点至少在一个 chunk 里是完整的

- 递归分块 RecursiveCharacterTextSplitter  最常用

- 按结构分块 markdown / 标题

- 语义分块 SemanticChunker
- 父子分块 小块检索 大块回答

- chunk 大小如何选择? 先给一个可落地的起点：300–500 中文字（约 256–512 token），overlap 10%–15%。这是多数场景的安全默认值，但不是终点

问题:
- 为什么分块, 分块的核心矛盾是什么
    语义的完整性          vs          检索的精准度
    chunk 太大 -> 语义越完整, 但检索 越不 精准, token也越贵
    chunk 太小 -> 检索越精准 语义越残缺
本质上: 分块的策略 其实是在这两者之间找平衡
"""