"""
可迭代对象（Iterable）
    本质 只要这个对象内部实现__iter__函数 并返回一个迭代器对象的 都是可迭代对象
    常见的可迭代对象那个
        list tuple str dict set
        range()
        自己写的带有__iter__的类
"""
# 判断是否是可迭代对象
# collections.abc 这个模块中定义了一堆"协议类" 用来描述一个对象应该具备什么能力
from collections.abc import Iterable,Iterator
lst = [1,2,3]
it = iter(lst) # 迭代器---->lst.__iter__()

# isinstance(对象,类型)  判断某个对象是不是某个类型(某个子类)的实例   返回True/False

# 如果返回True  那么就是可迭代对象 能遍历
print(isinstance(lst,Iterable)) #True
print(isinstance("123",Iterable)) #True
print(isinstance(123,Iterable)) #False  数字类型不是可迭代的对象

# 如果返回True  那么是迭代器
print(isinstance(lst,Iterator)) #False
print(isinstance(it,Iterator)) #True

# 迭代器 = 可迭代对象+__next__
"""
    迭代器  可迭代对象
    可迭代对象：实现了__iter__,能被for循环遍历，能被iter()处理，但他本身不记录遍历进度
    迭代器：实现了__iter__和__next__,它记录遍历位置，每次next()返回下一个元素
"""
