"""
把代码公共部分放到函数里面，不一样的部分以参数的形式传进去，减少代码的冗余度
    函数 求和1-100
    1-1000
    100-10000
"""
def get_sum(a, b):
    sum = 0
    for i in range(a, b + 1):
        sum += i
    return sum
print(get_sum(1, 100))
print(get_sum(1, 1000))
print(get_sum(100, 10000))




