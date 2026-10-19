"""
在python中，一等函数（First-Class Functions）指的是函数作为一等公民，
可以像普通变量一样被传递 赋值 作为参数 作为返回值等等
一等函数有几个核心特征
    1.函数可以赋值给变量
    2.函数可以作为参数传递
    3.函数可以作为返回值
    4.函数可以存在容器中（列表。字典。。。。）

    总得来说就是，函数可以当变量用，也有变量有的东西
"""
# 1. 函数可以赋值给变量
def fn1(name):
    return f"hello {name}"

# fn1没有加括号  赋值的是函数本身
sya_hello = fn1
print(sya_hello("Alice"))

# 2.函数可以作为参数传递
def fn2(a):
    return len(a)

def fn3(func,value):
    return func(value)

print(fn3(fn2,[11,22,33]))

# 3.函数可以作为返回值
def fn4(n):
    def fn5(x):
        return x * n
    return fn5  #返回的是函数对象  不是函数的调用

# double拿到的是fn4这个函数的返回值  也就是fn5这个函数
double = fn4(2)
# print(double)
print(double(5))

# 4.函数可以存在容器中
dict1 = {
    # "属性名":"属性值"
    "add": lambda a,b:a+b,
    "sub": lambda a,b:a-b,
}
# dict1字典中的add属性对应的属性值===》匿名函数
print(dict1["add"])
# 调用
print(dict1["add"](10,5))

# pass是python的空语句/占位符，本身什么都不做 没有任何的操作,python的语法规则：def  if for等等后边的代码块不能空着，必须要有缩进代码，如果你暂时还没有想好内部要写什么样的逻辑  那么就写上pass占个位置，防止语法报错
def f1():
    pass

def f2():
    pass
#
# list1 = [f1,f2]
# print(list1[0]())