# 函数作为一种数据类型
def fn(x,y):
    return x * y

# function
print(type(fn))

# 把fn函数整个赋值给f这个变量
f = fn
# 函数
print(f)


print(f(5,8))

# 将函数放在列表中存储
def fn1(a,b):
    return a + b

def fn2(a,b):
    return a - b

def fn3(a,b):
    return a * b

list1 = [fn1,fn2,fn3] # 把上面三个函数放到这个列表里面
print(list1)
for i in list1:
    print(i(12,3), end = " ")