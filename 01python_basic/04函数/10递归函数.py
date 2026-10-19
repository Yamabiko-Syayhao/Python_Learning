# 递归函数 自己直接或者间接的调用自己的函数
# 一定要有个条件满足 可以跳出  否则死循环

# 求5的阶乘  5！  5*4*3*2*1
def fn1(n):
    if n == 1:
        return 1
    return n*fn1(n-1)
"""
    n=5  fn1函数的返回值是5*fn1(4)
    n=4  fn1函数的返回值是4*fn1(3)
    n=3  fn1函数的返回值是3*fn1(2)
    n=2  fn1函数的返回值是2*fn1(1)
    n=1  1
"""
print(fn1(5))


# 递归求和 1-100的和
def fn2(end):
    if end <= 1:
        return 1
    return end + fn2(end-1)

print(fn2(100))


list1 = [
    {
        "name":"name1",
        "value":"1",
        "children":[
            {
                "name":"name1-1",
                "value":"11"
            },
            {
                "name":"name1-2",
                "value":"12"
            },
            {
                "name":"name1-3",
                "value":"13",
                "children":[
                    {
                        "name":"name1-3-1",
                        "value":"131"
                    },
                    {
                        "name":"name1-3-2",
                        "value":"132"
                    }
                ]
            }
        ]
    },
    {
        "name":"name2",
        "value":"2",
        "children":[
            {
                "name":"name2-1",
                "value":"21"
            }
        ]
    },
    {
        "name":"name3",
        "value":"3",
    }
]

# 以下是理解递归还有字典和列表循环操作的重要函数操作，读到这里务必重点记笔记
# 帮我写一个函数  处理一下上边的list1这个树状结构的数据
# 实现树状结构的数据的遍历  获取所有节点的值放到一个列表中
# ["name1","name1-1","name1-2""name1-3","name1-3-1"....,"name2","name3"]
arr = [] # 先定义一个列表下面要用
def fn3(val):
    for item in val:
        # print(item) # 这里输出了上面列表每一项的值，每一项都是字典
        # item["name"] # 这里会拿键所对应的值
        arr.append(item["name"]) # 把键所对应值都放到这个再次定义的列表里面
        # 判断每一层是否有children属性
        if item.get("children"): # 要有一个判断，如果遇到键为children的就执行下面的
            # 继续调用自己这个函数
            # 把children 这个键所对应的值列表当作参数传递进去
            fn3(item["children"])
    return arr
print(fn3(list1))

# list2 = [
#     {
#         "name":"name3",
#     },
#     {
#         "name":"name4",
#     },
#     {
#         "name":"name5",
#     }
# ]
# for item in list2:
#     print(item)






