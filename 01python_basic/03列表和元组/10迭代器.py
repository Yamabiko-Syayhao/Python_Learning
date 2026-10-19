'''
迭代器：相当于一个取号机器 内部记录位置 一次只能拿出一个元素
可迭代对象：字符串 列表 元组 集合
'''
list1 = [11, 22, 33, 44, 55]
# 通过iter方法生成迭代器
yy = iter(list1)
# next()取出下一个元素 只能前进不能后退
print(next(yy))
print(next(yy))
print(next(yy))
print(next(yy))
print(next(yy))
# 如果再往下取，后边没有元素了，所以如果再来一个print(next(yy))会报错












