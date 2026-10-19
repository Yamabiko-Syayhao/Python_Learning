set1 = {11, 22, 33, 44, 55}
set2 = {44, 55, 66, 77, 88}

# 以下演示是，集合可以放到列表当中，列表不能放集合里面
list1 = [set1, set2]
print(list1)

# set3 = {[11,22], [33, 44]}
# print(set3)

# 添加  添加元素的时候，如果元素已经存在 是不会报错的
set1.add(77)
set1.add(77)
print(set1)

# 删除  指定删除某个元素
set1.remove(44)
print(set1)
set1.discard(77)
print(set1, "discard删除")

set1.discard(77)
print(set1, "discard再删除")
# 用discard如果删了不存在的（已经被删了）的元素，那么不会报错，但是remove会

# 随即删除，并返回删除的元素
pp = set1.pop()
print(set1, "pop删除", pp)


# 清空
set1.clear()
print(set1)

# 更新集合
# 当传入的是字符串的时候，会把字符串中的每个字符都拆开成单个字符放进集合
# set1.update(77) 会报错，因为update()接收的是一个可迭代的对象
# 可迭代对象指的是可以用for循环进行遍历的对象
# 常见的可迭代对象有 列表 元组 集合 字符串....
set1.update("1231231231")
print(set1)
set1.update(set2)
print(set1)








