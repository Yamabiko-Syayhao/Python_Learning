# 需要先下载requests模块，是第三方请求库 用来发送请求，爬取网页
import requests
"""
# get 请求方法1
    requests.get(url="请求的接口地址?参数a=值&参数b=值",
    headers={请求的请求头},
    )                   # ?后有几个值就每次都要&隔开，如果只有一个值就写一个，就不用写&
# get 请求方法2
    res = requests.get(
        url="请求的接口地址",
        params={"参数a":值,"参数b":值},
        headers={请求的请求头}
    )

# post/delete/put请求语法 ---->传递给后端json格式的数据
res = requests.post(
        url="请求的接口地址",
        json={请求参数},
        headers={
            "Content-Type":"application/json"
            }
    )

# post/delete/put请求语法 ---->传递给后端字典格式的数据
res = requests.post(
        url="请求的接口地址",
        json={请求参数},
        headers={
            "Content-Type":"application/x-www-form-urlencoded""
            }
    )


"""
res = requests.get(
    url="https://www.buchouwang.com/stage-api/website/getProductDetails?productId=15",
    # params={"productId":5}
)
print(res)
print(res.status_code,"状态码")
print(res.text)
# re.text 是res请求的具体数据
print(type(res.text))

# 将json字符串转为字典
import json
obj1 = json.loads(res.text)
print(obj1)
print(type(obj1))

print(obj1["data"]) # 获取data里面的数据
print(obj1["data"]["productDetails"]) # 获取productDetails里面的数据







