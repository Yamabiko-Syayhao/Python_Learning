# 自定义模块 开发者自己写的.py文件 放在项目目录中 直接导入
# 1.完整导入模块
# import com_python
# print(com_python.max_num([1, 2, 3, 4]))

# 2.导入模块中所有内容
# from com_python import *
# print(max_num([1, 2, 3, 4, 5, 6]))

# 3.精准导入模块
# from com_python import max_num, min_num, avg_num
# print(max_num([1, 2, 3, 4, 5, 6]))
# print(min_num([1, 2, 3, 4, 5, 6]))
# print(avg_num([1, 2, 3, 4, 5, 6]))

# 4.别名导入模块
# import com_python as cp
# print(cp.max_num([1, 2, 3, 4, 5, 6]))
# print(cp.min_num([1, 2, 3, 4, 5, 6]))
# print(cp.avg_num([1, 2, 3, 4, 5, 6]))

# 5.函数别名导入模块
from com_python import max_num as ma, min_num as mi, avg_num as av
print(ma([1, 2, 3, 4, 5, 6]))
print(mi([1, 2, 3, 4, 5, 6]))
print(av([1, 2, 3, 4, 5, 6]))





