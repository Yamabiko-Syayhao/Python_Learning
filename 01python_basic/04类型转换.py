# 整数
num1 = 123
# 浮点型
num2 = 1.23

# 整数 + 浮点数 = 浮点数
num3 = num1 + num2
print(num3,type(num3))

# int() 强制转为整数
# 浮点型==》整型
xx = int(2.8)
print(xx,type(xx))
# 字符串==》整型 字符串只能写纯整数  不能带小数点
yy = int("777")
print(yy,type(yy))
# zz = int("77.77") #报错
# print(zz,type(zz))

# float() 强制转为浮点型
a = float(1)
b = float('66')
c = float('77.77')
print(a,type(a))
print(b,type(b))
print(c,type(c))
print("=============================")

# str() 强制转为字符串
a1 = str(1)
a2 = str(1.23)
a3 = str(True)
# 字典中属性 加引号的才叫属性  不加引号代表用的是个变量
a4 = str({"aaaa":1})
a5 = str({a:1})
print(a1,type(a1))
print(a2,type(a2))
print(a3,type(a3))
print(a4,type(a4))
print(a5,type(a5))

print("="*20)

# bool() 强制转为布尔型
# 数字0  空字符串 空列表 空字典等转换完的结果是False
# 如果转换的内容具有具体的值 都是True
b1 = bool(1)
b2 = bool(2)
b3 = bool(0)
b4 = bool("")
# 里边有个空格  所以不是空字符串
b5 = bool(" ")
b6 = bool("123")
b7 = bool({})
print(b1,type(b1))
print(b2,type(b2))
print(b3,type(b3))
print(b4,type(b4))
print(b5,type(b5))
print(b6,type(b6))
print(b7,type(b7))

print("="*20)

# tuple() 列表强制转为元组
list1 = [11,22,33]
tuple1 = tuple(list1)
print(tuple1,type(tuple1))

# list() 元组强制转为列表
list2 = list((66,77,88))
print(list2,type(list2))


