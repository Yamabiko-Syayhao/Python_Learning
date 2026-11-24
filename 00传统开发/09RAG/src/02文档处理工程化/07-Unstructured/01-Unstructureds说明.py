""" 前面我们学了 PDF、Word、PPT、HTML、OCR… 每种格式一套 API，企业里几十种格式，不可能写几十套解析器
Unstructured是文档解析器，是一个库，可以统一解析 PDF / Word / PPT / Excel / HTML / 邮件 / 图片…

 Unstructured 解决了这个问题：
    可以统一解析 PDF / Word / PPT / Excel / HTML / 邮件 / 图片…
    统一输出"结构化元素"（Title / NarrativeText / Table / ListItem …）
    NarrativeText 叙事文本===正文
    自带 Chunk 分块能力
    LangChain / LlamaIndex 官方集成
 它是企业 RAG"文档接入层"的主要工具之一。
一、Unstructured 核心理念
    Unstructured 非结构化的
     任意格式文档
    ↓ partition()  统一解析
    ↓ List[Element]  结构化元素列表
        每个元素有：category（类型）、text（文本）、metadata（元数据）
     metadata方便溯源
    ↓ chunking  智能分块
    ↓ Embedding → VectorDB

二、安装依赖
    uv add "unstructured[all-docs]"  -i https://pypi.tuna.tsinghua.edu.cn/simple
    部分格式需要系统依赖：
    brew install libmagic poppler tesseract   (macOS)
"""