"""
模块化：把代码按照某些功能拆分成多个独立的文件，每个文件都是一个模块
按照需要去引入
引入模块有三种
    自定义的方法
    第三方方法
    系统内置方法
目的：让代码不堆在同一个文件里面，可引入使用
"""


# python中导入模块的五种方法
# =================  第一种 完整导入模块 =================
# 语法：import 模块名  适用于需要使用该模块中多个功能时
# 特点 需要用 模块名.去访问
"""
import math
print(math.ceil(3.14)) # ceil 向上取整
print(math.floor(3.9999)) # floor 向下取整
print(math.pi) # pi 圆周率
print(math.factorial(3)) # 斐波那契数列
"""

# ================= 第二种 导入模块所有内容（不推荐）  =================
# 语法：from 模块 import *
# 缺点：把模块当中所有的公开名字全部导入到当前的全局命名空间里面，所以你在使用的
# 时候很容易搞混，不清楚这个函数来自哪个模块，容易造成变量重复。容易污染命名空间
"""from math import *
print(ceil(3.14))  # 必须要这么用
print(floor(3.9999))
print(pow(3,2))"""

# ================= 第三种 精准导入指定功能（推荐使用）  =================
# 语法：from 模块名 import 函数1,函数2,函数3......
# 优点：按需导入 只导入需要的内容 节省资源 代码简洁
# from math import ceil,floor,pi
# print(ceil(3.14))
# print(floor(3.9999))
# print(pi)

# ================= 第四种 模块别名导入  =================
# 语法：import 模块名 as 别名
# 优点：简化长的模块名 代码更简洁 避免变量冲突
"""import math as m
print(m.ceil(3.14))
print(m.floor(3.9999))
print(m.pi)"""

# ================= 第五种 函数别名导入  =================
# 语法：from 模块名 import 函数名1 as 别名,函数名2 as 别名,函数名3 as 别名,
from math import ceil as c, floor as f, pi as p
print(c(3.14))
print(f(3.9999))
print(p)

