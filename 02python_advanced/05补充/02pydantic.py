# pydantic 主要做两件事 数据验证和数据解析（强制转换）uv add pydantic
from pydantic import BaseModel

# 定义数据规则 必须有name age email 并且类型必须对
class User(BaseModel):
    model_config = {"validate_assignment": True}
    name: str
    age: int
    email: str

user = User(name="Alice", age="30", email="test@123.com")
print(user,"user") # name='Alice' age=30 email='test@123.com' user
print(user.model_dump()) # 转为普通字典
print(user.age) # 输出30 字符串"30"自动被转换成了整数
print(user.name)
print(type(user.age))  # 会帮你转为int

# pydantic ver2+ 直接赋值 不做任何检查 validate_assignment 默认值为false
# user.age = "True" # 报错
user.age = "666" # 内部悄悄转换
print(user.age)
print(type(user.age))

# pydantic 在运行时真正进行校验数据，并且还能自动做类型转换
# TypedDict 只在静态检查的时候起作用






