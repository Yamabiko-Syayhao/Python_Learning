"""
函数的封装：就是把代码公共的部分放到函数里边，不一样的部分以参数的形式传进去，减少代码冗余
    需求 求1-100的和
        求1-1000的和
        求100-10000的和
"""
# sum = 0
# for i in range(1,101):
#     sum+=i
# print(sum)
#
# sum1 = 0
# for i in range(1,1001):
#     sum1+=i
# print(sum1)

# 定义函数  封装公共代码
def get_sum(start,end):
    # 放置和的变量
    sum = 0
    for i in range(start,end):
        sum += i

    print(sum)

get_sum(1,101)
get_sum(1,1001)
get_sum(100,10001)