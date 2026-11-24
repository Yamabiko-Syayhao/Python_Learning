"""
HTML 是企业知识库里"最被低估"的数据源

很多人以为 HTML 只是网页，其实企业内部大量知识也有可能都是 HTML：
    Confluence / 语雀 / Wiki 导出页
    内部帮助中心、FAQ 页面
    Notion / 飞书文档导出
    富文本编辑器（CKEditor、TinyMCE）存到数据库里的正文
    邮件正文（HTML 邮件）
    爬虫抓回来的网页

如果不会 HTML 解析：
    要么把一堆 <div><span> 标签喂给大模型 → token 爆炸 + 噪音
    要么用正则瞎删标签 → 把表格、标题、列表结构全删没了

需要掌握的内容：
- HTML 的本质与 DOM 树
- 企业中的 HTML 来源
- BeautifulSoup 提取纯文本
- 按标签提取标题 / 段落 / 列表 / 表格
- 只提取正文（去广告、去导航、去页脚）
- HTML 转 Markdown（RAG 最佳实践）
- 企业级 HTML 解析 Pipeline


一、HTML 的本质 [超文本标记语言]
HTML 本质是一棵 DOM 树（树形结构 Document Object Model）：
    <html>
    └── <body>
        ├── <h1>标题</h1>
        ├── <p>正文段落</p >
        ├── <ul><li>列表项</li></ul>
        └── <table>...</table>

解析 HTML = 遍历这棵树，按"语义标签"还原结构。

二、企业中的 HTML 类型
类型1：Wiki / Confluence 导出
    特点：标题层级清晰、表格多
类型2：帮助中心 / FAQ
    特点：问答结构、适合直接做 Chunk
类型3：富文本数据库字段
    特点：脏标签多、需要清洗
类型4：爬虫网页（下一节专讲）
    特点：导航、广告、推荐位噪音极多

三、核心难点
整页 HTML 里真正有价值的"正文"往往只占 20%，
其余 80% 是导航栏、侧边栏、广告、页脚、JS 脚本。
企业方案：正文抽取（Readability / trafilatura） + 结构化转换。

四、安装依赖
    uv add beautifulsoup4 lxml html2text trafilatura markdownify -i https://pypi.tuna.tsinghua.edu.cn/simple
"""