arr = [10,20,30,40]
print(len(arr))
print(f"列表中元素的最大值：{max(arr)}")
print(f"列表中元素的最小值: {min(arr)}")

print("=="*30)

# 复制一份列表arr 赋值给a1
a1 = arr.copy()
print(a1)

a2 = [1,2,3,4,5]
# 合并列表
a1.extend(a2)
print(a1)

a3 = [1,2,3,1,2,4,5,6,2]
# 统计元素2在列表a3中出现的次数
print(a3.count(2))

a4 = [11,22,33,44,55,66]
# 向列表中追加元素到列表的最后
a4.append(77)
print(a4)

# 在列表的任意位置前边插入元素
a4.insert(3,'hello') # 下标3前面
print(a4,"aaaaaaaa")

# 查找元素在列表中的索引位置  找到返回下标   找不到报错  xxx is not in list
print(a4.index('hello'),"777")
# print(a4.index('hello666'))

# 删除列表中指定的元素
a4.remove('hello')
print(a4)

# 根据提供的下标删除指定的元素
a4.pop(0)
print(a4)

print("=="*30)

a5 = [12,23,34,66,123,9]
# 如果是数字类型 默认从小到大排序
# a5.sort()
# 实现从大到小排序
a5.sort(reverse=True)
print(a5)

a6 = ["12","23","34","66","123","9"]
# 如果是字符串 那么就按照字符的ASCLL码值排序
a6.sort()
print(a6)

# 如果是字符串 但是我还想让他以数字的形式排列大小
a6.sort(key=int)
print(a6)

a7 = [11,33,22,99,56]
# 反转 颠倒
a7.reverse()
print(a7)

# 清空列表
a7.clear()
print(a7)