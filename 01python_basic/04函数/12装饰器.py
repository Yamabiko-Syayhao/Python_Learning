"""
接收函数作为参数，返回新函数的高阶函数
作用是不修改原函数代码。不修改原函数的调用方式，给原函数新增额外的功能
（日志，计时，捕获异常等等）

定义装饰器
def 外层函数名(外层接收的函数)
    def 内层函数名():
        函数体--编写装饰器逻辑 + 调用原函数
    return 内层函数名

"""


# def log_print(func):
#     def wrapper(): # 内层函数
#         print("日志---我来了")
#         func()
#         print("日志---拜拜了")
#     return wrapper # 返回包装之后的函数
#
#
# def a():
#     print("hello world")
#     b()
#     print("hello again")
#
# def b():
#     print("hello")
#     c()
#     print("8")
#
# def c():
#     print("2608")
#
# # 手动包装一下原函数，用装饰器包装原函数
# a = log_print(a) # 把对应的log_print的返回值赋给a
# b = log_print(b)
# c = log_print(c)
# # 原函数a b c的代码一行没动 也实现了我一开始的需求 这就是装饰器的核心价值
# a()

"""
语法糖：编程语言中的术语，它指的是在编程语言中添加的某种语法，这种语法
对语言的功能没有影响，但更方便程序员去使用，可以提高代码的可读性和
简洁性。总之，底层实现完全一样，但是更方便，更好看
用语法糖去实现会简洁，看起来更易读一些
"""

def log_print(func):
    def wrapper():
        print("日志---我来了")
        func()
        print("日志---拜拜")
    return wrapper

@log_print
def a():
    print("hello")
    b()
    print("world")

@log_print
def b():
    print("hello")
    c()
    print("world")

@log_print
def c():
    print("hello")
    print("world")

a()








