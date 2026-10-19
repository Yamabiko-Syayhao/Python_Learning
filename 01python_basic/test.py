'''
data = {
    "class2608": {"Alice": 85, "Bob": 90},
    "class2609": {"Charlie": 78, "David": 88}
}
1.找出所有学生的最高分及其所在班级

2.计算所有学生的平均分
'''

data = {
    "class2608": {"Alice": 85, "Bob": 90},
    "class2609": {"Charlie": 78, "David": 88}
}
list1 = []
max_score = 0      # 记录当前最高分
max_class = ""     # 记录最高分所在的班级
for i in data: # 取出第一层data字典里面的键
    for j in data[i]: # 对应第一层里面的值，也就是里面的两个字典。循环取出值
        x = data[i][j] # data[i][j]是里面的键对应的值
        list1.append(x) # 把字典的值放在列表里面
        # 一边收集一边比较，找到最高分的同时记住它属于哪个班级
        if x > max_score:
            max_score = x
            max_class = i
print(f"所有学生的最高分是{max_score}，所在班级是{max_class}")
print(f"所有学生的平均分是{sum(list1) / len(list1)}")



'''
list = ["白羊座","金牛座","双子座","巨蟹座","狮子座","处女座","天枰座","天蝎座","魔羯座","水瓶座","双鱼座"]

nature = ["积极乐观","固执内向","圆滑世故","多愁善感","迷之自信","精美计较","犹豫不决","阴暗消极","放荡不羁","务实本分","作天作地","安于现状"
]
根据两个列表 让用户输入星座，输出对应的性格特点
请输入你的星座：水瓶座
你的星座是水瓶座，你的性格特点:务实本分
'''
# 方法1 我的方法
list2 = ["白羊座","金牛座","双子座","巨蟹座","狮子座","处女座","天枰座","天蝎座","射手座","魔羯座","水瓶座","双鱼座"]
nature = ["积极乐观","固执内向","圆滑世故","多愁善感","迷之自信","精美计较","犹豫不决","阴暗消极","放荡不羁","务实本分","作天作地","安于现状"
]
dict1 = {i:j for i,j in zip(list2,nature)}
print(dict1)
val = input("请输入你的星座：")
if val in dict1:
    print(f"你的星座是{val}，你的性格特点:{dict1[val]}")
else:
    print("没有这个星座哦！")



# # 方法2 index找下标                                                                                                                                                                                                                                                                                                                                                                     LSP
# val1 = input("请输入你的星座：")
# if val1 in list2:
#     idx = list2.index(val1)      # 找到星座在列表里的位置
#     print(f"你的星座是{val1}，你的性格特点:{nature[idx]}")
# else:
#     print("没有这个星座哦！")




# # 方法3 字典 + get() 方法
# dict1 = dict(zip(list2, nature))
# val3 = input("请输入你的星座：")
# print(dict1.get(val3, "没有这个星座哦！"))
# get方法，有的话返回字典键对应的值，没有的话返回默认值
#
#
#
# #方法4：enumerate 边遍历边找
# val = input("请输入你的星座：")
# for i, sign in enumerate(list2): # 取出下标和对应值
#     if sign == val:
#         print(nature[i]) # 代入对应下标对应到下一个一样下标位置的列表
#         break
# else:                       # for-else：循环正常结束（没 break）才执行                                                                                                                 L
#     print("没有这个星座哦！")













