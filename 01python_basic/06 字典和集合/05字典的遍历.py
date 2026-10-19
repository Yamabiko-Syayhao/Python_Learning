# 构造器方法定义一个字典
dict1 = dict(name = "阿拉蕾",age = "16")
print(dict1, type(dict1))

for x in dict1:
    print(f"字典属性是---{x}")

for x in dict1.keys():
    print(f"键---{x}")

for x in dict1.values():
    print(f"值---{x}")

for x,y in dict1.items():
    print(x,y, "键和值")
















