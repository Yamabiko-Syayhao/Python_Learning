
"""
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    # 定义对象的官方字符串表示 主要给开发者看 主要用于调试和开发
    def __repr__(self):
        return f"Student(name={self.name}, age={self.age})"
    # 定义 == 运算符的行为 也就是说“相等”的判断逻辑
    def __eq__(self, other):
        return self.name == other.name and self.age == other.age

stu1 = Student("arl",16)

print(stu1)
print(repr(stu1)) # 和上面那个运行是一样的

stu2 = Student("arl",16)
print(stu1 == stu2)
"""

# 如果没有上面定义的__eq__那print(stu1 == stu2)会输出false

# 装饰器 用于简化创建主要用于存储数据的那种类，它自动生成__init__,__repr__,
# __eq__,等方法，减少样本代码
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    age: int

s1 = Student("arl",16)
s2 = Student("arl",16)
print(s1)
print(s2)
print(s2 == s1) # True







