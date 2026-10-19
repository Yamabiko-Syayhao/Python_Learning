# 逻辑运算符
# and与运算：有假则假，全真为真
# or或运算： 有真则真，全假为假
# not非运算： 取反

a = 1
b = 2
c = 3
# 与运算  a<b成立为真  b>c不成立为假  真and假===》假False
print(a < b and b > c)
# 或运算 a<b成立为真  b>c不成立为假  真or假===》真True
print(a < b or b > c)

# and与运算  了解即可
# a为真直接返回b
# a为假 直接返回a  后边的b不执行（有一种短路效果）
print(a and b)
# 0是假的值
print(0 and b)

# not非运算 取反
# a<b也就是1<2成立True  取反False
print(not a < b)

# 成员运算符  in  /  not in
# in 判断a是不是在元组中
print(a in (1,2,3,4,5)) #True
# 1不在（1，2，3，4，5）中是否成立
print(a not in (1,2,3,4,5)) #False

# 身份运算符 is  id
x = 99
y = 99
# ==判断两个变量的值是否相等
print(x == y)
# is 判断内存地址是否相同
print(x is y)
# id() 查看值的内存地址
print(id(x))
print(id(y))

print("=="*20)

list1 = []
list2 = []
# 判断值是否相等
print(list1 == list2)
# 判断内存地址   内存不同
print(list1 is list2)
print(id(list1))
print(id(list2))

# 基本数据类型值和内存都相等  复杂的数据类型（列表/元组/字典/集合）内存不相等
# 赋值这种情况是相等的
aa = []
bb = aa
print(aa is bb)

# 三目运算符
# 条件成立的结果表示式 if 条件 else 条件不成立的结果表达式
cc = 33
res = "孙悟空" if cc > 18 else "猪八戒"
print(res)