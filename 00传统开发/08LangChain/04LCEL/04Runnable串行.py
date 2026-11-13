"""
串行：按顺序挨个执行 |的规则就是前一段跑完了返回什么，就把这个结果直接丢给下一段当中输入，一步接一步
实现串行方法有两种
    RunnableLambda 把普通函数包裹一下，直接拼流水线，适合写短小逻辑和
    直接去继承’Runnable‘基类 自己完整写一个独立组件 适合复杂 重用性高的业务模块（计算，校验，格式化等等）
"""
from langchain_core.runnables import RunnableLambda,Runnable
from typing import Any,Dict

# ============== 使用RunnableLambda实现简单的串行流水线
# def add(a,b):
#     return a+b
# def sub(a):
#     return a-10
#
# add_runnable = RunnableLambda(func=lambda x:add(x[0],x[1]))
# sub_runnable = RunnableLambda(func=sub)
# # 串行编排 先执行add_runnable 拿到结果自动传给sub_runnable执行
# res = add_runnable | sub_runnable
# print(res.invoke((18,27)))

# -------------------自定义复杂的串行业务逻辑
# 传进小写字母
class UpperName(Runnable):
    #     # 必须实现invoke方法 invoke就是组件被执行的时候调用的入口函数
    # input_dict:上游传进来的数据 这里是字典
    # config:langchain预留的配置参数 一般写None即可
    # ** kwargs 保证你的自定义组件不会因为“多传递了参数”而报错
    def invoke(self, input_dict: Dict[str, Any], config: Any = None, **kwargs) -> Dict[str, Any]:
        # 从传入的字典中取出name原始值
        raw_name = input_dict["name"]
        # 把名字转为大写；input_dict保留传入的全部旧字段，追加新字段upper_name
        return {
            **input_dict,  # 解包 把旧字典的所有字段"摊开"复制进来
            "upper_name": raw_name.upper()
        }


# ----------------------自定义第二个流水线组件：生成欢迎文案----------------------
# 接收上一个函数的结果，生成欢迎文案
class SayHello(Runnable):
    # invoke是固定必须实现的执行方法
    def invoke(self, input_dict: Dict[str, Any], config: Any = None, **kwargs) -> Dict[str, Any]:
        # 读取上一个组件生成好的大写名字
        big_name = input_dict["upper_name"]
        # 拼接欢迎字符串
        msg = f"欢迎你，{big_name}！"
        # 在原有字典基础上新增欢迎消息字段
        return {
            **input_dict,
            "welcome_msg": msg
        }


# ===================== LCEL串行流水线组装 =====================
# 使用 | 管道符串行执行：先走UpperName，它的输出自动传给SayHello作为输入
# chain = UpperName() | SayHello()

chain = (
    RunnableLambda(lambda x:{**x,"upper_name":x["name"].upper()})
    | RunnableLambda(lambda x:{**x,"welcom_msg":f"欢迎你，{x['upper_name']}"})
)

result = chain.invoke({"name":"zhangsan"})
print(result)


