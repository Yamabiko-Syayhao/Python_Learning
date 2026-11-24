"""
Playwright 抓取动态网页渲染
大部分现代网站 (Vue / React / Angular SPA) 内容 由 JS 渲染, requests 拿到的是空壳  <div id="app"></div>, 所以这个时候 必须先让浏览器真正跑一遍 JS，再取渲染后的 DOM 必须用浏览器 内核来执行 js

Playwright 的核心工作就是模拟真实浏览器环境，来抓取那些需要执行 JS 才能显示内容的网页。它需要的是一个纯净、可控且能跨平台运行的浏览器内核  下载的是一个绝对纯净、零插件的浏览器

可以使用国内镜像源来加速下载：
set PLAYWRIGHT_DOWNLOAD_HOST=https://cdn.npmmirror.com/binaries/playwright

playwright install chromium

"""
# 导入Playwright库  同步接口
from playwright.sync_api import sync_playwright
def fetch_dynamic(url):
    # with上下文管理器,自动关闭浏览器和页面
    with sync_playwright() as pw:
        # 1 启动浏览器 headless=True无头模式--不显示浏览器窗口
        browser = pw.chromium.launch(headless=True)
        # 2 创建一个标签页
        page = browser.new_page()
        # 3 访问网页 等待DOM(网页标签)加载完成 这样速度快 等HTML被解析完就返回，不等图片、样式、子资源加载完 超时时间30秒
        page.goto(url, wait_until='domcontentloaded', timeout=30000)
        # 4 等待指定id为app的元素出现 超时时间30秒 ---- [如果指定元素出现了说明网页加载完成了] 最关键的一步
        page.wait_for_selector('#app',  state='attached', timeout=30000)
        # 拿到 JS 渲染后的完整 HTML
        html = page.content()
        # 关闭浏览器 释放资源
        browser.close()
        # 返回渲染后的HTML
        return html
html = fetch_dynamic('https://www.buchouwang.com/')
print(html)