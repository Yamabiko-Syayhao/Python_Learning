list1 = ["1","10","22","345","234","105"]
# 从小到大排序
# 方法一  按照整数的逻辑进行排序，排序比较的时候，把每一项都临时转为int去比较，但是列表元素本身依旧是字符串，不会改变原有的数据类型
list1.sort(key=int)
print(list1)

# 方法二 列表推导式
list2 = [int(i) for i in list1]
list2.sort()
print(list2)