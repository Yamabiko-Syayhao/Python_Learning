# 数据类型----就是给数据进行分类
# type() 检测数据类型

# 1.字符串 str  包裹在引号里边的内容
aa1 = "今年的目标是中彩票"
print(aa1,type(aa1))

# 2.数字类型
# 整型  int
aa2 = 999
print(aa2,type(aa2))
# 浮点型  float
aa3 = 99.99
print(aa3,type(aa3))
# 复数complex
# 实部 + 虚部j  复数.real 实部   复数.imag 虚部
aa4 = 3+5j
print(aa4,type(aa4),aa4.real,aa4.imag)

# 3.布尔类型 bool  两个值 True/False
aa5 = True
aa6 = False
print(aa5,type(aa5))
print(aa6,type(aa6))
# 如果布尔类型的值参与数学计算  True会转换成1   False会转换为0
print(False + 6)
print(True + 6)

# 列表/字典/元组/集合    定义一个变量 存储多个数据

# 4.列表 list
aa7 = [666,"李帅豪","田霄悦","邢子健",123,True]
print(aa7,type(aa7))

# 5.字典 dict
aa8 = {
    # 属性:属性值,
    "name":"陈俊朋",
    "age":18,
    "hobby":"学python",
    "flag":True
}
print(aa8,type(aa8))

# 6.元组 tuple 长得像列表 列表能改 元组不能改
aa9 = ("晚上不睡","早上不起","中午崩溃",666,False)
print(aa9,type(aa9))

# 7.集合 set 自动去重
aa10 = {11,22,33,44,55,66,11,77,33}
print(aa10,type(aa10))


# {属性:属性值} 字典
# [值1,值2] 列表
# {值1,值2} 集合
# (值1,值2) 元组 不能改