# Typing 模块基础
# 变量类型注解 基本类型注解
name:str = "Alice"
age:int = 18

# 函数注解 name1是str类型，times是int类型
# -> 返回值类型注解 表示greet函数返回一个字符串
def greet(name1:str,times:int = 1) -> str:
    print(f"{name1}" * times)
    return f"Hello {name1}. How are you?" * times

greet(123) # 运行时不会报错，但是IDE上会有警告
# python中的类型注解只是“提示”，不会强制检查数据类型，写错了也不会报错
"""
# python 3.8+的写法
# typing模块提供了类型提示支持，让代码更易读
from typing import List,Dict
names:List[str] = ["Alice","Bob","Carol"]
print(names)

dict1:Dict[str, int] = {"name":23,"age":18}
print(dict1)
"""
# python3.9+的写法 不需要再从Typing中引入List等等
names:list[str] = ["Alice","Bob","Carol"]
print(names)
dict1:dict[str, int] = {"name":23,"age":18}
print(dict1)

# 3.10+的写法  |或
list2:list[str | int] = ["Alice","Bob","Carol",999]
print(list2)

# TypedDict 在python中用于给字典提供类型提示的工具，主要用于静态类型检查，让
# 字典拥有类似“固定键名和值类型”的结构
# 直白的说就是给字典加上结构
from typing import TypedDict
class User(TypedDict):
    name: str
    age: int
    sex: str

"相当于你这个字典必须有name age sex 并且值的类型不允许错"
user:User = {
    "name":"Alice",
    "age":18,
    "sex":"female"
}
print(user)
print(user["name"])




