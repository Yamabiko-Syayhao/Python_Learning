'''
data = {
    "class2608": {"Alice": 85, "Bob": 90},
    "class2609": {"Charlie": 78, "David": 88}
}
1.找出所有学生的最高分及其所在班级

2.计算所有学生的平均分
'''
# 最高分及其所在班级
data = {
    "class2608": {"Alice": 85, "Bob": 90},
    "class2609": {"Charlie": 78, "David": 88}
}
max_score = 0
max_class = ""
for class_name, students in data.items():
    for student, score in students.items():
        # print(class_name, students,"外层循环变量")
        # print(student, score,"内层循环变量")
        if score > max_score:
            max_score = score
            max_student = student
            max_class = class_name
print(f"所有学生的最高分是:{max_score}，所在班级是:{max_class}")
print(f"获得最高分的人是:{max_student}")

# 所有分数
all_scores = []
for stu in data.values():
    all_scores.extend(stu.values())
#     extend()方法把字典的对应值取出来然后合并成新列表,
#     也就是把可迭代对象里边的元素逐个添加到列表中
print(all_scores,"extend方法")
avg_score = sum(all_scores) / len(all_scores)
print(f"所有学生的平均分是:{avg_score}")


# 列表推导式 和上边所有分数的方法一样
new_score_list = [j for i in data.values() for j in i.values()]
print(new_score_list)

# list = []
# max_num = 0
# max_class = ""
# for i,j in data.items():
#     for num in j.values():
#         list.append(num)
#         if num > max_num:
#             max_num = num
#             max_class = i
# print(f"所有学生的最高分是{max_num}，所在班级是{max_class}")
# print(f"所有学生的平均分是{sum(list) / len(list)}")


'''
list = ["白羊座","金牛座","双子座","巨蟹座","狮子座","处女座","天枰座","天蝎座","魔羯座","水瓶座","双鱼座"]

nature = ["积极乐观","固执内向","圆滑世故","多愁善感","迷之自信","精美计较","犹豫不决","阴暗消极","放荡不羁","务实本分","作天作地","安于现状"
]
根据两个列表 让用户输入星座，输出对应的性格特点
请输入你的星座：水瓶座
你的星座是水瓶座，你的性格特点:务实本分
'''
list2 = ["白羊座","金牛座","双子座","巨蟹座","狮子座","处女座","天枰座","天蝎座","射手座","魔羯座","水瓶座","双鱼座"]
nature = ["积极乐观","固执内向","圆滑世故","多愁善感","迷之自信","精美计较","犹豫不决","阴暗消极","放荡不羁","务实本分","作天作地","安于现状"
]
dict1 = {}
for num in range(len(list2)):
    dict1[list2[num]] = nature[num]
print(dict1)

# 查看数据 里边的每一项都是一一对应好的元组
for i in zip(list2, nature):
    print(i, "迭代")

# dict 转为字典
dict2 = dict(zip(list2, nature))
print(dict2)


# key = input("请输入你的星座")
# print(f"你的星座是{key},你的性格特点：{dict1[key]}")




