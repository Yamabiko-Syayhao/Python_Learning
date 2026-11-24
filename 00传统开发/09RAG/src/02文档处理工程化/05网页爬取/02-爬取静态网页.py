# 导入requests库
import requests
# 导入BeautifulSoup是Python解析HTML常用的工具
from bs4 import BeautifulSoup
# 请求头,模拟浏览器访问
headers = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/148.0.0.0 Safari/537.36")
}
# # =================== 1 ===================
# 目标地址
url = "https://www.trae.cn/pricing"
# get发送请求
# resp = requests.get(目标网址, 请求头, 超时时间)
resp = requests.get(url, headers=headers, timeout=10)
# 自动识别编码 防止中文乱码
resp.encoding = resp.apparent_encoding
# 打印状态码和响应内容
# print(f'状态码:{resp.status_code}')
# print(f"响应内容:{resp.text}")

# 将返回的HTML字符串解析为BeautifulSoup对象
soup = BeautifulSoup(resp.text, "lxml")
# 定义空列表,用于存储所有button按钮
# btns = []
# 获取网页的button按钮    select查询css选择器
# 标签选择器   只有标签名  button/a/p/div  没有任何特殊符号
# 类名选择器   在标签中有个属性  class     写法  .类名     举例:  .items-center
# id选择器     在标签中有个属性   id      写法   #id名    举例:   #root
# 后代选择器   举例: #root button   被id为root包裹着的所有的后代button按钮
for btn in soup.select("#root button"):
    print(f"被id为root包裹着的所有的后代button按钮:{btn.text}")
print("========="*10)

# =================== 2 ===================
# 目标网站
url = "https://www.trae.cn/pricing"
# get发送请求
# resp = requests.get(目标网址, 请求头, 超时时间)
resp = requests.get(url, headers=headers, timeout=10)
# 自动识别编码,防止中文乱码
resp.encoding = resp.apparent_encoding
# 将返回的HTML字符串解析为BeautifulSoup对象
soup = BeautifulSoup(resp.text, "lxml")
# 获取header中的所有a标签
a_list = soup.select('header a')
# print(f"获取header里面的所有的a标签{a_list}")

'''
    相对路径
    <a href="/pricing">查询</a>  ===>  <a href="https://www.trae.cn/pricing">查询</a>
    绝对路径
    <a href="https://www.trae.cn/delete">删除</a>

    检查所有的a标签是不是绝对路径,是绝对路径就直接添加到link_list中
    如果a标签不是绝对路径是相对路径,那么这个相对路径需要补全成绝对路径,再添加到link_list中
'''
# 网站的基础域名,用于补全相对路径
base_url = 'https://www.trae.cn'
# 导入urljoin库,用于拼接url和相对路径
from urllib.parse import urljoin
# 定义空列表,用于存储所有a标签的文本和href属性
link_list = []
# 遍历所有a标签
for a in a_list:
    # 绝对路径带盘符http://或者D:盘符
    # 判断href属性是否是绝对路径,startswith检查是否以http://或https://开头
    if a['href'].startswith('http://') or a['href'].startswith('https://'):
        # 提取文本内容和href属性值拼接成字典最后将字典放到列表中
        link_list.append({
            'text': a.get_text(),
            'url': a['href']
        })
    else:
        # 如果不是 urljoin 把相对路径 补全成 绝对路径 包含标签内容
        # full_url = urljoin(base_url, a['href'])
        # 绝对路径 + 相对路径
        full_url = base_url + a['href']
        # 添加到列表中
        link_list.append({
            'text': a.get_text(),
            'url': full_url
        })
# 在网站上以http://  或者https://  这种以域名或者ip开头的也是绝对路径
print(f"获取补全后的a标签{link_list}")