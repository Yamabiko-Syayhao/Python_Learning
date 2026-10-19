# 函数定义方式
# 1.def 普通函数 命名函数
def fn1(a,b):
    return a+b
print(fn1(10,20))

# 2.lambda匿名函数---没有函数名称 一行简短函数  不需要写def
# lambda 形参1,形参2,形参n:结果
# 匿名函数自调用
# lambda x,y:x+y
# (lambda x,y:x+y)(10,20)
(lambda x,y:print(x+y,"匿名函数的输出"))(10,20)

# 3.函数表达式  可以将一个匿名函数赋值给一个变量
xx = lambda x1,y1:x1+y1
# xx 是个匿名函数  <function <lambda> at 0x00000282660B93A0>
print(xx)
print(xx(20,60)) # 这里赋值调用了

print("=="*30)

# filter() 输出的是一个过滤器 生成的内容   需要转为列表/元组的方式查看
# 语法  filter(lambda x:条件,列表变量)

# 需求 从下边的列表中 过滤出偶数
num = [1,2,3,4,5,6,7,8,9]
# 拿到列表num中的每一个元素给x 再去判断条件x%2==0是否成立   如果条件成立则保留元素，最终生成筛选之后的迭代器
ev_num1= filter(lambda x:x%2==0,num)
# 是个迭代器对象 看不到真实数据 <filter object at 0x0000014670632C80>
print(ev_num1)
# 需要转为列表/元组的形式才能查看
ev_num2 = list(ev_num1)
print(ev_num2)
# filter 惰性迭代器 只能消费一次  第二次就空了
ev_num3 = list(ev_num1)
print(ev_num3) # 输出的是[] 空列表，因为上面已经用了一次了

# map() 加工器    生成的内容需要转为列表/元组的方式查看
# 语法  map(lambda x:加工结果,列表变量)
list1 = [1,2,3,4,5,6,7,8,9]
diedai = map(lambda x:x**3,list1)
# <map object at 0x00000250301D74F0>
print(diedai)
result = tuple(diedai) # 转为元组的方式查看
print(result)


# 列表中每一个元素都是个字典
list2 = [
    {"name":"张三","age":"18"},
    {"name":"李四","age":"8"},
    {"name":"王五","age":"36"},
]
# sort(key=?,reverse=?)
# key= 指定排序顺序的函数（最重要）
# reverse= 是否反转  布尔值
# list2这个列表 中的每一个元素都是字典  所以x就是个字典  字典取值===》字典["属性"]
# sort会把列表中的每一个元素 挨个丢给key后边这个函数 作为函数的参数
list2.sort(key=lambda x:int(x["age"]),reverse=True) # reverse=True 反转排序
"""
sort 需回看
"""

# 不用lambda  用普通函数
# def get_age(item):   # 上面的lambda就是相当于这个函数
#     return int(item["age"])
#
# list2.sort(key=get_age, reverse=True)
print(list2)

