# 1.定义装饰器
# 外层函数 接收普通函数作为参数
def fn1(func):
    # 内层函数
    def wrapper(*args, **kwargs):
        print("这就开始执行了")
        print(args, "args") # args ==> (2, 10)
        # func(*args) # 相当于是 func(2, 10)
        # *args 传参解包，把元组的容器里面的东西拆成一个个元素扔进去
        # func(args) # 相当于是 func((2, 10))
        # args 整个元组作为一个整体传入
        # 元组被拆分成一个个的元素
        ref = func(*args, **kwargs) # 相当于add返回值赋给了ref
        # 这里用的是add自己
        print(ref, "ref的结果")
        print("已经执行完毕了")
        return ""
    return wrapper

# 2.定义普通函数且使用装饰器
# 加了装饰器后，add就会指向fn1返回的wrapper
@fn1
def add(a, b):
    return a+b

# 3.调用普通函数
print(add(2, 10),"add的结果") # 因为有了装饰器实际上调用的是wrapper()



# args传入整体，*args传入解包后的单个元素
# 重点元组解包相关

