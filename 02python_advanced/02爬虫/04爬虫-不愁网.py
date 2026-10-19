# 请求接口模块
import requests
# pandas 数据整理模块  可以把数据变成一张"表格" 可以操作里边的内容  uv add pandas
import pandas as pd

# ==========================配置区域====================
# 请求接口----请求数据用的
api_url = "https://www.buchouwang.com/stage-api/website/getNewsList"
# 请求头
headers = {
    # 浏览器的标识
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
    # 来源页  绕过网站的防盗链
    "Referer":"https://www.buchouwang.com/newsList?newsType=1",
    # 请求哪台电脑的数据
    "Host":"www.buchouwang.com",
    # 声明接受的相应数据的格式
    "Accept":"application/json, text/plain, */*"
}
# 请求参数
params = {
    "pageNum":1,
    "pageSize":4,
    "newsType":1,
}
# ==========================爬虫主要逻辑====================
try:
    print("正在获取数据中。。。。。")
    # 请求接口获取数据
    res = requests.get(api_url, headers=headers, params=params)
    # 主动检查http响应状态码 如果请求失败 就抛出异常 如果状态码是200正常往后执行
    res.raise_for_status()
    # 把响应体转成json格式  解析成python对象  通常是字典或者列表
    lis = res.json()['rows']

    # 接下来就是处理列表
    data = [] #准备用来存放新闻信息的
    for i,v in enumerate(lis):
        remark = v['remark']
        newsName = v['newsName']
        createTime = v['createTime']
        data.append({
            "描述":remark,
            "标题":newsName,
            "创建时间":createTime
        })

    # 使用pandas 将列表数据 转为表格 导出excel文件
    df = pd.DataFrame(data)
    # print(df)
    # 输出文件格式  index = False 不导出自带的索引
    df.to_excel("utils/不愁网.xlsx",index=False)
    print("信息表生成！")
except Exception as e:
    print(f"出错了{e}")