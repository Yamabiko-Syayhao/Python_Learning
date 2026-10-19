# 引入随机模块
import random

# random.choice(列表)  一次抽取一个  允许重复
# random.choices(列表,k=抽几个) 有放回抽样 允许重复 可以抽取到同一个元素  返回列表
# random.sample(列表,k=n) 无放回抽样 不允许重复

fruits = ["apple", "banana", "peach"]
# print(random.choice(fruits))
# 内部悄悄循环了6次 每次都放回  最终把这六个结果包装成一个列表返回出来
# 对外表现出来的是“一次性拿了六个元素出来”  但是实际上底层是循环多次调用单个抽取的逻辑，进行有放回抽样
# print(random.choices(fruits,k=6))

# 一次性从列表中取出来3个 取出来不还回去
# print(random.sample(fruits,k=3))




# 花色
suites = ["♠","♦","♣","♥"]
# 大小王
joker = ["大王","小王"]
# 牌面数字
num = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
# 生成一副牌面 52张花色牌+大小王
# pai = []
# for i1,v1 in enumerate(suites):
#     for i2,v2 in enumerate(num):
#         # 字符串拼接
#         # print(v1+v2)
#         pai.append(v1+v2)

old_pai = [f"{huase}{i}" for huase in suites for i in num]

# 追加上大小王这两张牌
old_pai.extend(joker)
# pai+=joker

# print(old_pai)

# 把所有的牌都抽出来重新生成一个新的列表
new_pai = random.sample(old_pai, len(old_pai))
# print(new_pai)

wanjia1 = []
wanjia2 = []
wanjia3 = []
dizhu = []
for i,v in enumerate(new_pai):
    if i < 17:
        wanjia1.append(v)
    elif 17 <= i < 34:
        wanjia2.append(v)
    elif 34 <= i < 51:
        wanjia3.append(v)
    else:
        dizhu.append(v)

wanjia1.extend(dizhu)

# print(f"地主的牌{wanjia1}")
# print(f"农民1的牌{wanjia2}")
# print(f"农民2的牌{wanjia3}")