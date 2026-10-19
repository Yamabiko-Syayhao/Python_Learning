set1 = {11, 22, 33, 44, 55}
set2 = {44, 55, 66, 77, 88}

# 判断11是否在集合里面
print(11 in set1)
# 判断11是否不在集合里面
print(11 not in set1)


# 并集 两个集合合起来
print(set1 | set2)
# 交集 两个集合重复的部分
print(set1 & set2)
# 对称差集 两个集合中不同时存在的内容
print(set1 ^ set2)
# 差集 第一个集合有，第二个集合没有的元素
print(set1 - set2)
print(set2 - set1)

# 子集 set1里面所有的元素都在set2里面
print(set1 <= set2)
#真子集 set1所有的元素都能在set2里面找到，且set1和set2不能完全一模一样
print(set1 < set2)
# 超集 set2所有的元素都在set1中
print(set1 >= set2)
# 真超集 set2所有的元素都在set1中找到 并且set2和set1不能一模一样
print(set1 > set2)








