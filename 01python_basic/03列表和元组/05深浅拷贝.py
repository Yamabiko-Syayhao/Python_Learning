# 定义了一个变量 二维列表
# list1 = [10,20,[30,40]]

# 直接赋值  将list1得值拷贝一份赋值给list2  当我修改list1的时候 list2也会发生改变
# list2 = list1
# list1[0] = 99
# list1[2][0] = 100
# print(f"list1---{list1}")
# print(f"list2---{list2}")

# 浅拷贝 把a复制一份给b，当我去修改a中的第一层元素的时候，b的第一层不会随着a的改变而改变，
# 当我去修改a中的第二层以及深层的时候，b的第二层以及深层会跟着改变
# 原数据和复制后的数据第一层不变，第二层或者深层都会改变
a = [10,20,[30,40]]
# ① 列表的方法  复制
# b = a.copy()
# ② 构造器方法
# b = list(a)
# ③ 切片
# b = a[:]
# a[0] = 99
# a[2][0] = 100
# print(f"a---{a}")
# print(f"b---{b}")

# copy 是python标准库  有两个核心函数 copy.copy()浅拷贝  copy.deepcopy()深拷贝
import copy
# ④ copy.copy()   通用浅拷贝  列表/元组/字典等容器类型
# b = copy.copy(a)
# a[0] = 99
# a[2][0] = 100
# print(f"a---{a}")
# print(f"b---{b}")

# 深拷贝 就是将a复制一份给b,当我去修改a的时候，b所有的层级无论是第一层还是更深层都不跟着改变，拥有独立的内存
a1 = [10,20,[30,40]]
b1 = copy.deepcopy(a1)
a1[0] = 99
a1[2][0] = 100
print(f"a---{a1}")
print(f"b---{b1}")
