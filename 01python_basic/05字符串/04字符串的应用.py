# 1.统计"hello"中每个字符出现的次数
# {"h":1, "e":1, "l":2, "o":1}
# 普通方法
# a = "hello"
# count1 = 0
# count2 = 0
# count3 = 0
# count4 = 0
# for i in a:
#     if i == "h":
#         count1 += 1
#     elif i == "e":
#         count2 += 1
#     elif i == "l":
#         count3 += 1
#     else:
#         count4 += 1
#
# dict1 = {"h":count1, "e":count2, "l":count3, "o":count4}
# print(dict1)
from unittest import result

str1 = "hellp"
dict1 = {}
for i in str1:
    # print(i) # 字符串中每个字符
    if i in dict1: # 判断i在不在dict1里面
        # i是变量，在这里也作了字典的键
        # dict["h"]
        print(i, dict1[i], "888")
        dict1[i] += 1 # 给对应键的值加一
    else:
        dict1[i] = 1
        print(i, dict1[i], "999")
print(dict1)
# 以上代码也需要回看，重要





# 2.把字符串"banana"中的重复字符去掉，保持首次出现该字符串的顺序
# 普通方法
b = "banana"
c = ""
for i in b:
    if i in c:
        pass
    else:
        c += i
print(c)


str2 = "banana"
result = ""
for i in str2:
    if i not in result:
        # 字符串的拼接
        # 第一次 "" + "b" = "b"
        # 第二次 "b" + "a" = "ba"
        # 第三次 "ba" + "n" = "ban"
        # 第四次由于不满足if条件，所以不能再进行循环了
        result += i
print(result)



