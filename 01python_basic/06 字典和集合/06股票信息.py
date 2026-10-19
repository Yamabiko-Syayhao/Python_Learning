'''
    1 找出大于100的股票并创建新字典
    2 找出价格最高的和最低的对应的股票代码
    3 按照股票的价格从高到低排序

obj = {
    'AAPL':191.88,
    'GOOG':1186.96,
    'IBM':149.24,
    'ORXL':48.44,
    'ACN':166.89,
    'FB':208.9,
    'SYMC':21.89
}
'''


obj = {
    'AAPL':191.88,
    'GOOG':1186.96,
    'IBM':149.24,
    'ORXL':48.44,
    'ACN':166.89,
    'FB':208.9,
    'SYMC':21.89
}

# new_obj = {}
# for i,j in obj.items():
#     if j > 100:
#         new_obj[i] = j
# print(new_obj)
#
#
# for i,j in obj.items():
#     if j == max(obj.values()):
#         print(f"最高股票的代码 {i}")
#     if j == min(obj.values()):
#         print(f"最低股票的代码 {i}")
#
#
# result = []
# for i, j in obj.items():
#     result.append((j, i))
# result.sort(reverse=True)
# print(result)
# sorted_obj = {}
# for j, i in result:
#     sorted_obj[i] = j
# print(sorted_obj)

# 以下为老师写的答案

# ========== 先搞懂 obj[i] 到底是键还是值 ==========
# 核心一句：方括号里的 i 是"键"，整个 obj[i] 是"值"
#   obj = {'AAPL': 191.88, 'GOOG': 1186.96}
#   i            -> 键（钥匙），比如 'AAPL'
#   obj[i]       -> 值（东西），比如 191.88
#   obj          -> 整个字典
# 类比：obj 像一排带标签的柜子，i 是标签，obj[i] 是打开标签 i 的柜子后看到的东西
#
# 对比两种遍历：
#   for i in obj:            只发给你"钥匙"，要拿"东西"必须自己开柜子 obj[i]
#   for i, j in obj.items(): 直接把钥匙(i)和东西(j)一起发给你，不用再 obj[j]
#
# ========== 那 new_obj[i] = j 到底是键还是值？ ==========
# 判定标准不是"字典空不空"，而是"在等号左边还是右边"！
#   变量[键] 在等号左边 -> 表示"要写入的位置（键）"
#   变量[键] 在等号右边 -> 表示"读取出来的值"
# 看这一行：
#   new_obj[i] = obj[i]
#    左边 new_obj[i]：i 是键，表示"往 new_obj 这个键的位置写东西"
#    右边 obj[i]    ：i 是键，表示"从 obj 读出这个键对应的值"
# 注意：obj[i] 空不空、有没有数据，都不影响它算键还是值，
#       左右位置才决定它是"写位置"还是"读值"。
# 空/非空只决定另一件事：这个键原来有没有
#   没有 -> 是"添加"一对；已有 -> 是"修改"这一对
# 再验证同一行两边都有 i：
#   new_obj[i] = obj[i]   左边 i 当键用，右边 i 也当键用，都成立
#   new_obj[i] = j        左边 i 当键用，右边 j 本来就是值
# 记法：方括号里的东西永远是键；整个 x[key] 在左边是"位置"，在右边是"值"。

# ---------- 任务1：大于100的股票 ----------
new_obj = {}
for i in obj:              # for i in obj 拿到的 i 是"键"（股票代码）
    # print(i,obj[i])
    # 属性名和属性值
    # 判断大于100的股票：obj[i] 才是"值"（价格），所以能和 100 比大小
    if obj[i] > 100:
        # 赋值：左边 new_obj[i] 是"新字典里以 i 为键的位置"，右边 obj[i] 是取出的值
        new_obj[i] = obj[i]
print(f"大于100的股票组成的新字典是{new_obj}")

# ---------- 任务2：最高/最低价对应的代码 ----------
# max(obj, key=obj.get)：max 遍历 obj 的每个键，对每个键调用 obj.get(键) 量出价格，
# 比完返回价格最大的那个"键"（股票代码）。key 就是"按什么标准比大小"。
print(max(obj, key = obj.get))
# print(min(obj, key = obj.get))
# 等价于下面这个 lambda 写法：给每个键 i，返回 obj[i]，效果一样
print(min(obj, key = lambda i: obj[i]))


# key = obj.get 对于每个键/属性 去用obj.get取出来对应的值，然后再进行对比

# obj.get 补充说明：
#   obj.get("GOOG")      -> 传入键，返回值 1186.96
#   obj.get("XXXX")      -> 键不存在返回 None（不报错，而 obj["XXXX"] 会报错）
#   obj.get("XXXX", 0)   -> 键不存在返回你给的默认值 0
#   obj.get（不加括号）是"工具本身"，obj.get(...)（加括号）才是用它干活
#   所以才能把 obj.get 当参数传给 max/sorted，让它们自己拿键去换值

# ---------- 任务3：按价格从高到低排序 ----------
# sorted(要排序的字典的变量，key=通过什么参数进行排序，reverse= 升序/降序)
# 区别：.sort() 原地改自己；sorted() 返回一个排好的新结果
# 这里 key=obj.get，还是按每个键对应的"价格"来排；返回的是排好序的"键的列表"
sort_obj = sorted(obj, key = obj.get, reverse = True)
print(sort_obj)









