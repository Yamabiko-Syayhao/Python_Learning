# 1.定义装饰器
# 外层函数 接收普通函数作为参数
def fn1(func):
    # 内层函数
    def wrapper(x, y):
        print(x**y, "求两个数的平方")
        ref = func(10, 20) # 保存的是原来的add(10, 20)
        # 如果想把原来外面用的add()里面的2, 10 要写ref = func(x, y)
        print(ref, "ref的结果")
        print(x*y, "求两个参数的积")
        return ""
    return wrapper

# 2.定义普通函数且使用装饰器
# 加了装饰器后，add就会指向fn1返回的wrapper
@fn1
def add(a, b):
    return a+b

# 3.调用普通函数
print(add(2, 10),"add的结果") # 因为有了装饰器实际上调用的是wrapper()




