from spider_html import SPIDER_HTML

# 转换为 md 文件格式的工具
import html2text

# 初始化调用html2text
h = html2text.HTML2Text()
# 忽略 表格 超链接 图片 标签
h.ignore_tables = True
h.ignore_links = True
h.ignore_images = True
h.body_width = 0
print(h.handle(SPIDER_HTML))

with open("product.md", "w", encoding="utf-8") as f:
    f.write(h.handle(SPIDER_HTML))
    print("文件已保存为 product.md")