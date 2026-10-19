obj = {
    "name":"arl",
    "age":16,
    "sex":"female",
    "arr":[11,22,33]
}
score = {}
print(max(obj)) # 直接对字典使用 max() 时，默认比较的是键
print()
# 1.获取
# 字典["属性/键"] 如果获取不到的属性值会报错
# 字典.get("属性/键") 如果获取不到的属性值 会返回 None
print(obj["name"])
print(obj.get("name"))


# 如果get()获取某个值的属性获取不到返回None  但是可以设置默认值，如果设置了就会返回默认值
print(obj.get("xxx", "默认值66"))
# print(obj.get("age", "默认值66")) # 这个可以获取到，不会返回设置的默认值

# 2.修改
# 字典["属性/键"] = "修改的值"
obj["name"] = "myk"
print(obj["name"])

# 3.添加 如果字典里面有这个键那就是修改，没有就是添加
# 字典["属性/键"] = "添加的值"
obj["job"] = "keyboard"
print(obj)

# 如果有这个属性就返回原来的值，如果没有就添加
obj.setdefault("sss","默认值88")
print(obj)

print(30 * "==")

# 4.删除
# del 字典["属性/键"]
del obj["job"]
del obj["sss"]
print(obj)


# 5.判断键是否存在
print("sex" in obj)
print("arr" not in obj)

obj2 = {
    "a":"yuno",
    "b":16,
    "c":"女",
    "name":"nono"
}

# 需求 将obj2合并到obj当中, 属性名也就是键名不能一致 一致会被覆盖掉
obj.update(obj2) # obj中重复的键被obj2覆盖掉了
print(obj)

# 这里len()会统计有多少对键值对
print(len(obj))

# 以下都是获取对应的值然后把它们放入列表里面
# 字典.keys() 字典的键
print(list(obj2.keys()))

# 字典.values() 字典的值
print(list(obj2.values()))

# 字典.items() 字典的键和值 这个每个键和值都会变成一个元组
print(list(obj2.items()))



# 清空字典clear
obj2.clear()
print(obj2)

# 判断字典是否为空
print(obj2 == {})





