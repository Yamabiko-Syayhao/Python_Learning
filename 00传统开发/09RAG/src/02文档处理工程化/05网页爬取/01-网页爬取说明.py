"""
RAG 知识库的数据 有时候需要"主动抓"：
    官网产品文档、帮助中心
    竞品资料、行业资讯
    政策法规网站
    技术博客、开源文档
    内部系统（OA/CRM）的网页

爬取 = RAG 知识库的"进水口"，没有数据，一切免谈。

目标：
- requests 抓静态网页
- 设置 Headers / 反爬基础
- 解析列表页 + 详情页（两段式爬取）
- Playwright 抓动态渲染网页（JS 渲染）
- 批量爬取 + 去重 + 限速
- 爬取 → 正文抽取 → 入库 Pipeline
- 爬虫合规与道德（robots.txt）

一、爬虫的两大类型
类型1：静态网页
    HTML 直接返回，requests 就能拿到内容
    工具：requests + BeautifulSoup
类型2：动态网页（SPA）
    内容由 JS 异步渲染（Vue/React）    vue框架渲染的是单页面程序   SPA
    requests 拿到的是空壳
    工具：Playwright / Selenium    了解: 无头浏览器

二、企业爬取标准流程（两段式）
    列表页（抓所有详情链接）
    ↓
    详情页（抓正文内容）
    ↓
    正文抽取（trafilatura）
    ↓
    清洗 / 去重
    ↓
    入库

三、安装依赖
    uv add requests beautifulsoup4 trafilatura
    uv add playwright
    playwright install chromium
"""