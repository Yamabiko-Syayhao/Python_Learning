"""
# 假设让你写一条流水线 输入一个数字 先+10 再+100
# def add10(x):
#     return x + 10
# def add100(x):
#     return x + 100
# chain = add10 | add100
# 普通函数不支持管道写法，因为普通函数本身不是标准零件 不能用 | 拼接到流水线中
# langchain中流水线上有一个硬性要求，所有的零件必须规格线统一，否则装不精确
# Runnable 是langchain中所有的标准零件都必须接收的一套统一的接口规范，它规定了一个组件只要满足两点，
# 就是一个合格的零件，1.就可以用invoke()。2.可以用管道符 | 进行拼接
# langchain内置组件 出场就是合格零件
# chain = prompt | llm | parser 三个合格的零件
"""
from langchain_core.runnables import RunnableLambda
from langgraph_sdk.stream import multi_cursor_buffer

# 怎么把一个普通的函数 包装成标准零件
# RunnableLambda
# 用了三个RunnableLambda，造了三个合格的零件
"""chain = (RunnableLambda(lambda x: x + 10) |
         RunnableLambda(lambda x: x + 100) |
         RunnableLambda(lambda x: x + 1000))

res = chain.invoke(1)
print(f"{res}\n{type(res)}")"""

# ==================== 传入字典类型数据
# def mul(a,b):
#     return a*b
#
# def mul_dict(input_dict:dict):
#     # 接收字典数据 取出对应key 然后交给mul函数 做乘法运算
#     return mul(input_dict["x"],input_dict["y"])
#
# # 将普通函数包装成Runnable对象
# runnable = RunnableLambda(mul_dict)
# res = runnable.invoke({"x":1,"y":2})
# print(res)

# 核心规则：所有传给RunnableLambda包装的函数，永远只接收一个参数

# ==================== 传入自定义类实例（对象）

# 自定义类
class MulClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b

def mul(a,b):
    return a*b

def mul_params(val):
    return mul(val.a,val.b)


run = RunnableLambda(mul_params)
res = run.invoke(MulClass(11,8))
print(res)

