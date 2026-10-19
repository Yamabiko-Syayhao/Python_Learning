# 递归函数是直接或者简接调用自身的函数

# 斐波那契数列 --- 前两项是1 后边每一项是前两项之和
# def fn(n):
#     # 基线条件 停止递归条件 防止无限循环 -- 防止死循环
#     if n <= 2:
#         return 1
#     return fn(n-1) + fn(n-2) # 前两项之和
#     # 递归条件 函数调用自身 每一次调用逐步向基线条件去靠近
# lis1 = [fn(n) for n in range(1,10)]
# print(lis1)
# # [1,1,2,3,5,8...]
#
# def fn(n):
#     if n == 1 or n == 2:
#         return 1
#     else:
#         return fn(n-1) + fn(n-2)
# print(fn(6))
#
# def fn(n):
#     if n <=2:
#         return 1
#     return fn(n-1) + fn(n-2)
# print(fn(6))

# 要实现  print(fn(6)) -->[1,1,2,3,5,8]
def fn(n):
    if n <= 1:
        return [1] # 第一个元素
    if n == 2:
        return [1,1] # 前两个元素
    # 假设我想求第n个数 要先拿到前n-1个数 把第n个追加进去即可
    req = fn(n-1)# 可以拿到前n-1个元素
    req.append(req[-1] + req[-2])
    return req
print(fn(6))
"""
fn(6) 需要fn(5)
fn(5) 需要fn(4)
fn(4) 需要fn(3)
fn(3) 需要fn(2)---->卡在基线条件上返回[1,1]
"""







