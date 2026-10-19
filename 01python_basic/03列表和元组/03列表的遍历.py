# 列表的遍历：就是循环将列表中的每一个元素取出来
list1 = [11,22,33,44,55]

# 拿到每一项元素
for i in list1:
    print(i)
    # 想修改每一项的值  赋值
    # 列表[下标] === 每一项元素 ==== i
    # 类似于 只读  只能读取不能修改
    # i = 123

print(list1)

print("=="*30)

# 方法一
for i in range(len(list1)):
    # i此时是0 1 2 3 4  下标  所以可以通过下标的方式给列表取值
    print(f"下标为{i}的元素是{list1[i]}")
    # 修改元素中每一项的值
    # list1[i] = 123

print(list1)

print("=="*30)

# 方法二 enumerate函数  获取列表的元素和索引
for i,v in enumerate(list1):
    # i是索引(真实下标)  v是元素(可以理解为是拷贝出来的副本)
    print(i,v)
    list1[i] = 666
    # 注意看看
    # v = 666
print(list1)


# 需求 引导用户输入五个数字，求出和，平均值，最大值，最小值
# 第一步 获取用户输入的五个数字 生成一个列表

# a = int(input("请您输入一个整数"))
# b = int(input("请您输入一个整数"))
# c = int(input("请您输入一个整数"))
# d = int(input("请您输入一个整数"))
# e = int(input("请您输入一个整数"))
# list2 = [a,b,c,d,e]
# print(list2)
# 上边挨个获取元素的重复代码太多 用个循环操作一下
list2 = []
for i in range(5):
    # i是下标
    shu = int(input(f"请您输入第{i+1}个整数:"))
    # 每次循环之后 都把用户输入的数字添加到这个列表最后
    list2.append(shu)
    print(list2)


# 第二步  拿到列表 遍历列表中的每一个元素  进行求和，平均值，最大值，最小值
# sum()求和  min()最小值  max最大值  和/长度=平均值
print(f"五个数字的和是：{sum(list2)}")

avg = sum(list2)/len(list2)
print(f"五个数字的平均数是：{avg}")
print(f"五个数字的最大值是：{max(list2)}")
print(f"五个数字的最小值是：{min(list2)}")