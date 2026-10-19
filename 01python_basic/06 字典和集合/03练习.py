# 需求引导用户输入一段英文内容，将输入的英文内容拆分
# 成小写的英文字母，输出字典
# 类似[("a",1),("b",2),("c",0)...]的形式
# 格式化输出 a出现了多少次 b出现了多少次 c出现了多少次... 26行

# 1
# text = input("请输入一串英文字母：")
# text = text.lower()
# dict1 = {i:0 for i in "abcdefghijklmnopqrstuvwxyz"}
#
# for i in text:
#     if i in dict1:
#         dict1[i] += 1
#     else:
#         dict1[i] = 1
# print(list(dict1.items()))
#
# for i,j in dict1.items():
#     print(f"{i}出现了{j}次")

# 2.我的答案
# 引入内置模块string
import string
from unittest import result

# content = input("请输入一段英文").lower()
# print(content)
# {"a":1,"b":2,"c":3,"d":4}
# print(string.ascii_letters) # a-z A-Z 共52个字母
# print(string.ascii_lowercase) # 26个小写字母
# print(string.ascii_uppercase) # 26个大写字母
result = {letter:0 for letter in string.ascii_lowercase}
print(result,"\n还没有内容的字典")
print("")

# 让用户输入英文且转小写
content = input("请输入一段英文").lower()
for x in content:
    # 判断输入的内容中每个字符是否存在 result 这个字典的属性中
    if x in result:
        # 如果存在 那么就修改字典中该属性对应的属性值 + 1
        result[x] += 1
print(result,"\n有内容之后的字典")
print("")
item_list = list(result.items())
print(item_list,"\n想要的列表")
# 将items_list遍历一下
for i in item_list:
    print(i,"每一项的值")
    print(f"{i[0]}出现了{i[1]}次") # 由于字典每一对键值对都被放入了一个元组里面
    # 所以i[0]是元组的第一个数，i[1]是元组的第二个数，也就是键和值







