"""
什么是迭代器？
    迭代器（Iterator）是一个可以记住遍历位置的对象(相当于一个会记录的工具人，
    只会往前走不回头，挤一次出一个数据)

    它实现了两个特殊方法：必须会的两个技能
        __iter__():返回迭代器对象本身
        __next__():返回下一个元素  如果没有元素时抛出StopIteration异常

    迭代器特点：
        --只往前走 不能往后退
        --用一次少一次，遍历完为空
        --惰性计算，非常节省内存
"""
# 自定义一个迭代器类  模拟一下简单的range
class MyRange:
    # 初始化
    def __init__(self, stop):
        self.stop = stop #数到stop就停止
        self.current = -1  #计数器从-1起步  当第一次+1操作直接变为0
        self.count = 0
    def __iter__(self):
        print("__iter__被调用了")
        return self #返回迭代器对象本身
    def __next__(self):
        print("__next__被调用了")
        # 每次调用的时候 都会执行下边的逻辑
        self.current += 1 # 计数器++
        if self.current >= self.stop: #判断一下计数器是否大于等于stop停止的值
            # raise 关键字  主动抛出异常  可以理解为"我要报错了，请立刻中断正常流程"
            raise StopIteration #StopIteration 不算错误  它是迭代器正常结束的信号
        return self.current  #没有达到停止的条件  那么就输出内容

# 实例化一个迭代器对象
# mr = MyRange(5) # 5传入到了__init__里面
# mr.__iter__()

# 手动挤数据
# print(next(mr)) #0
# print(next(mr)) #1
# print(next(mr)) #2
# print(next(mr)) #3
# print(next(mr)) #4
# print(next(mr)) #没有值了  报错抛出异常 超出了实例化的范围

# 利用for循环 进行取值  全自动挤数据 自动停不报错
# 隐式调用iter([0,1,2,3,4])---->[0,1,2,3,4].__iter__()
for i in MyRange(5):
    print(i)
#for循环内部执行流程
# 先调用iter(),返回迭代器对象，--》不断调用next() 疯狂往外
# 一个一个输出数据--》捕获到StopIteration异常信号。自动停手
# 相当于把上面mr.__iter__() 和几行的print(next(mr))都执行了