"""
import os
import time
import requests
# beautifulsoup   专门用来解析html网页代码的，可以从一堆网页源码中提取文字，链接，图片，图片地址等等
# lxml 解析器  第三方的需要先下载   相比于python自带的html.parser速度更快
# 同时下载俩   uv add beautifulsoup4 lxml

from bs4 import BeautifulSoup

# 接口前缀  后边有可能需要拼接图片链接  方便统一管理
# https://www.byesame.com/teacher_intr.html
# https://www.byesame.com/assets/images/teachers/1-%E5%B2%B3%E8%80%81%E5%B8%88.png
# ./assets/images/teachers/1-岳老师.png
baseUrl = "https://www.byesame.com"

# 获取网站信息
res = requests.get("https://www.byesame.com/teacher_intr.html")
# 获取res.text之前 强制告诉request使用utf-8编码格式解码
res.encoding = "utf-8"

# 初始化beautifulsoup对象 解析网页内容
# soup = BeautifulSoup(res.text,"html.parser")
soup = BeautifulSoup(res.text,"lxml")

# 获取网页中所有的img标签
img_list = soup.find_all("img")

for img in img_list:
    # 获取img标签上的src属性
    # print(img["src"])
    # 跟baseurl拼接  拼接成一个完整的路径
    # https://www.byesame.com./assets/images/teachers/1-岳老师.png
    # baseUrl + img["src"][1:]
    # 发送请求  获取图片
    imgs = requests.get(baseUrl + img["src"][1:])
    # print(imgs)
    # os.path.join 拼接路径
    # int(time.time()*1000) 用当前时间生成一个毫秒级别的时间戳作为文件名  避免重复
    file_path = os.path.join("utils","teacher_img",f"{int(time.time()*1000)}.jpg")
    print(file_path)
    # 目录万一不存在 做个准备  创建目录   exist_ok=True表示目录存在不报错
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as file:
        file.write(imgs.content)

"""

# 想优化一下   希望只存储老师的图片  并且希望本地存储的图片以老师名命名
import os
import requests
from bs4 import BeautifulSoup
"""
    加请求头headers的目的
        让我们的程序伪装成一个"正常的浏览器"去访问网站，而不是一个"赤裸裸的爬虫"
        
    请求头参数
        User-Agent：浏览器的标识  告诉人家当前设备是什么？伪装成谷歌浏览器
        Referer: 来源页  绕过网站的防盗链
        Accept: 声明接受的响应数据的格式
        Accept-Language: 语言协商 让服务端返回更符合预期的内容
        Host: 请求哪台电脑的数据  主机ip/域名
"""

# 通用请求头（html页面（网页）和图片（jpg/png/gif））
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
    "Referer":"https://www.byesame.com",
    "Accept":"*/*",  #最宽松  谁都能接收
}
# 请求html页面可以用的请求头
"""
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
    "Referer":"https://www.byesame.com",
    # 相当于告诉服务器 我想要网页文本 html文档
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9",  
}
"""
# 请求图片可以用的请求头
"""
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
    "Referer":"https://www.byesame.com",
    # 相当于告诉服务器 我想要图片二进制资源
    "Accept":"image/avif,image/webp,image/apng,*/*;q=0.8",  
}
"""
baseUrl = "https://www.byesame.com"
res = requests.get("https://www.byesame.com/teacher_intr.html",headers=headers)
res.encoding = "utf-8"
soup = BeautifulSoup(res.text,"lxml")
img_list = soup.find_all("img")
print(len(img_list))

for img in img_list:
    src = img.get("src","")
    # print(src,"src")
    # 只想保留老师的图片
    if 'teachers/' not in src:
        continue

    # （若开头的点可能有可能没有）
    img_url= baseUrl + src[1:] if src.startswith(".") else baseUrl + src
    # 发送请求  获取图片
    imgs = requests.get(img_url,headers=headers)
    rel_name = src.split("/")[-1]
    # print(rel_name,"真实名字")
    file_path = os.path.join("utils","teacher_img1",rel_name)
    # print(file_path)
    # 目录万一不存在 做个准备  创建目录   exist_ok=True表示目录存在不报错
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    #
    with open(file_path, "wb") as file:
        file.write(imgs.content)

