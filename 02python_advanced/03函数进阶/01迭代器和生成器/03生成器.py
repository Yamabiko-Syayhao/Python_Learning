"""
生成器Generator
    一种用函数语法写出来的迭代器  可以让你不用手动实现__iter__/__next__,语法更简洁

特点：
    用yield关键字往外蹦数据
    调用一次next() 执行到下一个yield，暂停 等待
    惰性计算，不占用大量内存
"""

# 定义一个生成器函数
def my_generator(n):
    i = 0
    while i < n:
        yield i  #泵一个数据 就会暂停等待  下一次进来的时候再继续  不是从头开始
        i += 1
# 使用
# g1 = my_generator(5)
# print(next(g1))
# print(next(g1))
# print(next(g1))
# print(next(g1))
# print(next(g1))
# 抛出异常
# print(next(g1))

# for循环 全自动泵数据
# for i in my_generator(5):
#     print(i)

# 生成器表达式 此处的()不是元组 是个标志  返回的是一个生成器对象   惰性的 使用的时候才算
gen = (x for x in range(5))
print(gen) #<generator object <genexpr> at 0x000002719A9E9B10>
print(type(gen)) #<class 'generator'>
# 取值  next一个个取值  还可以for循环
print(next(gen))

# 列表推导式  立刻生成所有值
list1 = [x for x in range(5)]
print(list1) #[0,1,2,3,4]
print(type(list1))

"""
三者的关系
可迭代对象 Iterable  实现了__iter__()方法的对象 可以被for循环遍历
迭代器  Iterator 同时实现了__iter__和__next__()方法  能被next()逐个取值，取完值之后抛出StopIteration
生成器 Generator 一种用更简洁的语法--函数语法写出来的迭代器  自动具备上边两个方法

迭代器一定是可迭代对象，可迭代对象不一定是迭代器，生成器一定是迭代器
"""