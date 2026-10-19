# python中元组与列表类似，不同之处在于元组的元素是不允许修改的，是只读的
# 元组---不可变容器 tuple  ()   列表list  []
# 元组与列表相同之处在于 每个元素都有对应的下标  下标从0开始

# 定义元组
tuple1 = ("炸鸡","辣条","汉堡","麻辣烫","咖啡","汉堡")
print(tuple1,type(tuple1))

# 访问元组中的元素
print(tuple1[0])

# 元组中元素的个数
print(len(tuple1))

# 修改元组中的内容  报错  不允许修改
# tuple1[0] = 666

# 将元组复制了三遍
print(tuple1 * 3)

# 统计汉堡出现的次数
print(tuple1.count("汉堡"))

# 查找咖啡所在的下标
print(tuple1.index("咖啡"))

# 判断饺子在/不在元组中  返回值布尔值
print("饺子" in tuple1)
print("饺子" not in tuple1)

# 切片
# 从下标为1的元素 截取到第三个元素
print(tuple1[1:3]) # 输出2个元素，从下标1包括自身，到下一个，不包括下标3
# 下标为1的元素截取到最后
print(tuple1[1:])
# 从开始截取到下标为2的元素/截取前三个元素
print(tuple1[:3])
# 反转
print(tuple1[::-1])
# 从下标为1开始截取 截取到下标为3的元素，步长为2
print(tuple1[1:4:2])