# 爬虫
# 去调用别人网站的接口，将网站上的接口数据生成文档存到本地或者是直接把网站上的图片内容扒下来

import requests
from bs4 import BeautifulSoup
import os
import time
# 下载的时候名字是beautifulsoup4 , 引入包的时候是beautifulsoup
# beautifulsoup 专门用来解析html网页代码的，可以从一堆网页源码中提取文字，链接，图片
# 图片地址等等
# lxml 解析器 第三方的需要先下载 相比于py自带的html.parser速度更快

# 接口前缀  后边有可能要拼接图片链接 方便统一管理
baseUrl = "http://www.norincogroup.com.cn"

# 获取网站的信息
res = requests.get("http://www.norincogroup.com.cn/col/col133/index.html")
# 获取res.text之前  强制告诉request使用utf-8编码格式解码
res.encoding = "utf-8"
# print(res.text) # 请求后的结果有乱码


# 初始化beautifulsoup 对象 解析网页内容
# soup = BeautifulSoup(res.text, "html.parser")
soup = BeautifulSoup(res.text, "lxml")
# 获取网页中所有img标签
img_list = soup.find_all("img")
# print(img_list,len(img_list))

for img in img_list:
    # 获取img标签上的src属性
    # print(img["src"])
    # 跟baseUrl进行拼接 拼接成一个完整的路径
    # baseUrl += img["src"]
    # 发送请求获取图片
    imgs = requests.get(baseUrl+img["src"])
    # print(imgs)
    # os.path.join 直接拼接
    # int(time.time()*1000) 用当前时间生成一个毫秒级别的时间戳作为文件名 避免重复
    file_path = os.path.join("serve_img",f"{int(time.time()*1000)}.jpg")
    # print(file_path)
    with open(file_path, "wb") as file:
        file.write(imgs.content)
print(file_path)





