'''
推导式：是一种特殊的数据处理方式，可以从一个数据序列构建出
一个新的数据序列
推导式是一种强大简洁的语法 适用于生成列表 字典 元组 集合
注意：使用推导式注意可读性 尽量保证表达式简洁
'''

# 列表推导式
# 列表中的元素是1-100之间能被3整除的整数
list1 = [i for i in range(1, 100) if i % 3 == 0]
print(list1)

# 字典推导式
list2 = ["google", "facebook", "yahoo", "tengxun", "taobaoshangou"]
# {"google":6...}
dict1 = {i:len(i) for i in list2}
print(dict1)

# 元组推导式（python当中其实没有元组推导式）
# 0-9每个数的平方
# tuple1 = (i**2 for i in range(0, 10))
# print(tuple1) 不能这样写 会打印出生成器对象，并非元组
tuple1 = (i**2 for i in range(0, 10))
print(tuple1)

# 生成器 + tuple() 推荐用这种
tuple2 = tuple(i**2 for i in range(0, 10))
print(tuple2)

# 列表推导式 + tuple() 列表转元组
tuple3 = tuple([i**2 for i in range(0, 10)])


# 集合推导式
# 1-10的立方
set1 = {i**3 for i in range(1, 11)}
print(set1)










