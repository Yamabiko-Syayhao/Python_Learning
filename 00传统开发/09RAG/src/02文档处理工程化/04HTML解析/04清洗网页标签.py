from bs4 import BeautifulSoup
from htm import html

soup = BeautifulSoup(html, 'lxml')

def clean_content():
    # soup() 等价于 soup.find_all()  传入一个列表的时候 查找匹配列表中任意一个标签名的所有元素
    for tag in soup(['ul', 'li', 'header', 'nav', 'h1', 'p']):
        # 清洗网页的噪音标签 删除 html 中所有的 ul li header nav h1 p 标签以及内容
        tag.decompose()
    # 提取剩下的没有被删除的标签中的内容 footer/table 标签中的内容
    clean_text = soup.get_text(separator='\n', strip=True)
    print(clean_text)

clean_content()