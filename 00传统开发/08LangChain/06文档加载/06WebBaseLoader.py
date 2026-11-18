import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

import os
os.environ["USER_AGENT"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                            "537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36")

# WebBaseLoader 专门用来抓取静态网页内容的文档加载器
from langchain_community.document_loaders import WebBaseLoader
"""
底层依赖 bs4 运行前需安装包    bs4 是 html解析器 负责从网页当中把正文文字拉出来
"""


# 定义需要抓取内容的目标网页地址
url = "https://www.byesame.com/teacher_intr.html"

# 实例化网页加载器
# header_template 自定义HTTP请求头 模拟真实浏览器访问 防止出现403禁止访问
# 单个页面 默认生成1个document对象
loader = WebBaseLoader(
    url,
    header_template={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36",
    }
)
# 这里的默认行为是把整个 word 完整读取，生成一个独立的document对象

# 让 requests 库不校验证书
loader.requests_kwargs = {"verify": False}
# 发起网络请求 一次性拉取网页内容 返回Document对象列表
web = loader.load()
print(f"共加载了{len(web)}个document对象")

# 判断文段列表是否为空
if web:
    for Web in web:
        # 元数据 存放网页元数据 包含 url 标题 等溯源信息
        print(Web.metadata)
        # 网页纯文本正文
        print(Web.page_content)
