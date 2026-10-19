"""
字典dict：可以存储任意数据类型 是一种可变容器(指的
是创建之后可以原地修改其内容，增删改)
    key:value   属性名:属性值     键:值
    字典被 {} 包裹着，键是唯一的，但是值可以重复
    {
    键:值
    key1:value1,
    key2:value2,
    key3:value3,
    keyn:valuen
    }
"""

a = 'awdawd'
print(a.replace('a', 'b'))
print(a,"relace方法字符串实例") # 还是awdawd
# 字符串不能改内容，上面这种只是在单独输出的时候不同

# 创建字典方法1 直接创建---推荐使用
stu = {
    "1001":"阿拉蕾",
    "1002":"藤都子",
    "1003":"峰月律"
}
print(stu,type(stu))

# 创建字典方法2 构造器 构造方法
stu2 = dict[str, str|int](name = "藤都子", age = 16, sex = "female")

# stu2 = dict(name = "藤都子", age = 16, sex = "female") 还可以这样写
# 不用特意写中间的[str, str|int]
print(stu2,type(stu2))

# 创建字典方法3 字典推导式
stu3 = {i:i*2 for i in range(1, 5)}
print(stu3,type(stu3))

# 取值
# 字典["属性"]
# 字典.get("属性")
print(stu["1002"])
print(stu.get("1002"))

# print(stu["1004"]) # 获取不到会报错
# print(stu2.get("name1")) # 获取不到不报错，返回None

# 赋值 字典["属性"] = "要修改的值"
stu2["name"] = "良子"
print(stu2)
