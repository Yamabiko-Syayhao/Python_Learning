# RunnableBranch 是LCEL表达式中if-else条件分支组件 按照顺序条件 命中哪一个就执行哪条处理数据
from langchain_core.runnables import RunnableBranch, RunnableLambda

# 处理原始 工单信息 清洗 工单 去掉空格转小写
def clean(ticket):
    return {"content": ticket["content"].strip().lower(), **ticket}

# 判断是否有退款工单
def check_refund(ticket):
    return any(word in ticket["content"] for word in ("退款", "refund"))

# 判断是否有关于技术问题的工单
def check_tech(ticket):
    return any(word in ticket["content"] for word in ("报错", "bug", "登录不上"))

# 命中的是退款 ----> 分配到退款队列
def refund_handler(ticket):
    # 追加队列标识 和等待时长 保留原有的工单信息
    return {"queue": "refund_queue", "wait": "2h", **ticket}

def tech_handler(ticket):
    return {"queue": "tech_queue", "wait": "4h", **ticket}

def normal_handler(ticket):
    return {"queue": "normal_queue", "wait": "24h", **ticket}

"""
变量 = RunnableBranch(
    (判断条件,RunnableLambda(普通函数),
    (判断条件,RunnableBranch(普通函数)),
    RunnableLambda(不成立执行的函数)
)
"""

branch = RunnableBranch(
    # 第一个判断 匹配退款关键字 执行退款处理函数
    (check_refund, RunnableLambda(refund_handler)),
    # 第二个判断 匹配技术故障关键字 执行技术处理函数
    (check_tech, RunnableLambda(tech_handler)),
    # 前边条件均不满足 执行普通逻辑
    RunnableLambda(normal_handler)
)

chain = RunnableLambda(clean) | branch

if __name__ == "__main__":
    # 定义了三类不停类型的测试工单数据

    case_list = [
        {"id": "T001", "content": "登录不上，软件有bug",},
        {"id": "T002", "content": "我申请退款"},
        {"id": "T003", "content": "请问营业时间是多少"}
    ]
    for item in case_list:
        print(chain.invoke(item))