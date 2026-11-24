# uv add beautifulsoup4
from bs4 import BeautifulSoup
from htm import html
# 通过 BeautifulSoup 方法解析 html 字符串  lxml 是底层解析器 速度最快
soup = BeautifulSoup(html, 'lxml')
# 提取文本
# separator 分割符 不同的标签之间获取的文本用换行符隔开
# strip 是否去掉首尾空格
text = soup.get_text(separator="\n",strip=True)

print(text)