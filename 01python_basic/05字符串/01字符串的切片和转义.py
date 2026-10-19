# 只要被引号包裹的都是字符串
a = "今天是9.14，周一"
b = "距离中秋放假还有11天"
c = """
hello
world
"""

print(a)
print(b)
print(c)

print("="*30)

# 转义
a1 = "\"xx代码xxx\"" # 转义字符反斜杠 \ 让py识别特殊字符
print(a1)



print("C:\\Users\\Public\\NortonLifeLock\\mybook")
a2 = r"C:\Users\Public\NortonLifeLock\mybook" # 加上r就可以输出原始字符
# r会自动帮字符串里面的特殊字符转义。如果要单个转义就用\（反斜杠）

# 还有另外一种，单引号和双引号可以交叉使用。
a3 = "'today is monday'"
a4 = "'today is tuesday'"
print("="*30)


# 字符串切片
strs = "梦限大是超越虚拟与现实的界限的一只乐队"
print(strs, type(strs))
# 取出来下标为0的元素，也就是第一个元素
print(strs[0])
# 从下标为0的位置开始截取，截取到下标为-1（倒数第一个元素）之前
# 去掉-1那个元素
# 意思是都不包含最后一个元素
print(strs[4:11])
print(strs[4:])
print(strs[:4])
print(strs[::-1]) # 反转输出
print(strs[::]) # 全省略了，相当于print(strs)

# 重复三次
print(strs*3)

# 切片格式[开始:结束:步长] 都可以省略[::]








