"""
函数返回值就是这个函数最终运行的结果
所有的函数如果没有写返回值的情况下，返回值都是None

return 关键字用来返回函数的结果
return 后面跟着什么值函数的返回值就是什么
return 后面不能乱写，得跟着有意义的值
return 后面的代码不执行
"""
from unittest import result


# 只是打印函数名
def fn(a, b):
    print(a, b)
print(fn)
"""
print(fn) 
只是单纯打印函数，<function fn at 0x0000025E05C478A0>
并不会执行函数内部的代码【函数本身，函数地址】
"""


# 打印函数的调用
print(fn(1, 2))
"""
会输出两行结果，一行是调用了fn执行里面的print(a, b) fn(1, 2)和fn()不同
因为fn(1, 2)，就是函数调用了，所以会先运行一遍函数。所以先打印了函数的调用
第二行是打印了函数的默认返回值None （因为没有指定返回值所以默认的是return None）
"""

print(30*"==")

def fn1(x, y):
    return x + y
# return 后面的代码不执行
# print(f"{x},{y}")
# 把调用了的fn1()返回值赋值给a，关键在于return 后面的值
a = fn1(3, 5)
print(a)

"""
函数内部的东西暂时无法拿到函数外部使用，函数的
返回（return）其实就是想把内部的东西拿到外部用
"""
def get_sum(a, b):
    return a + b
y1 = get_sum(10, 20) + 66
print(y1)

'''
函数的调用赋给了result，直接先去执行该函数的函数体。
然后又把返回值赋给了result
如果函数的返回值是普通的return，一调用就会执行函数体
'''
# print(30*"==")
# def fn2(x, y):
#     print("这就开始执行函数体了")
#     return x * y
# result = fn2(5, 8)
# print(result)



"""
但是如果是用到yield的函数，在调用的时候不会去执行函数内部的代码。
它只会返回一个迭代器对象  <generator object fn2 at 0x0000024286BB8EE0>，
然后代码暂停
如果要执行就要用到next
还有for循环自动带的有next
"""
def fn2(x, y):
    print("这就开始执行函数体了")
    yield x * y
fn2(1, 2)
result1 = next(fn2(5, 8))
print(result1)

a = [1, 2, 3, [1, 2, 3]]
b = a.copy()
print(a)
print(b)

# 甲方需求，生成一长串数字希望不要占用特别大的内存
# return版本，会生成1到10000的列表占用内存大
def get_num(n):
    res = []
    for i in range(1, n + 1):
        res.append(i)
    return res
nums = get_num(10000)
print(get_num(10000))
print(nums[:5])



# yield版本 这个占用内存会比上面小，因为上面是直接输出个1到10000的列表
# 而这下面由于for循环特性的自带的next会被执行了，每次只有一个数字被拿到外面
def get_num1(n):
    res = []
    for i in range(1, n + 1):
        yield i

gg = get_num1(10000)
# for循环自动next
for num in gg:
    print(num)
    # 这个分支不写，把1-100000全部生成
    if num >= 5:
        break








