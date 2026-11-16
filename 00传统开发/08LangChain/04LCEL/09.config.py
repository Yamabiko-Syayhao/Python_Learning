# 本代码展示的是 同一套订单流水线代码  调用的时候通过config动态传入购买渠道，会员等级等参数，实现不同的折扣计算
from langchain_core.runnables import RunnableLambda

# 格式化  重新建一个字典  只保留了order_id和price两个字段（原来字典其他字段会丢失）
def format_order(order):
    return {
        # 订单编号是字符串  订单价格是浮点数
        "order_id": str(order["order_id"]),
        "price": float(order["price"])
    }

# 核心   计算折扣
# config接收运行时config配置
def calc_discount(order, config):
    # 获取自定义配置区域的configurable
    cfg = config.get("configurable", {})
    # 获取销售渠道和是否是vip会员
    channel = cfg.get("channel", "shop")
    is_vip = cfg.get("vip", False)

    # 原价
    original = order["price"]
    # 折扣
    discount = 0
    # 如果是线上渠道 APP 优惠10%
    if channel == "app":
        discount += original * 0.1
    # VIP会员 额外优惠10%
    if is_vip:
        discount += original * 0.1
    #实付  原价-折扣价
    pay = original - discount

    # 完整结果 并且保留订单原始的字段
    return {
        "original_price": original, #原价
        "discount": round(discount, 2), #折扣 两位小数
        "pay_price": round(pay, 2), #实付
        "channel": channel, #渠道
        "vip": is_vip, # 是否是vip
        **order
    }

# 先格式化订单--》读取配置做计算
chain = RunnableLambda(format_order) | RunnableLambda(calc_discount)

if __name__ == "__main__":
    base_order = {"order_id": "O001", "price": 100}

    res1 = chain.invoke(base_order, config={
        "configurable": {"channel": "shop", "vip": False}
    })
    print("场景1结果：", res1)
    print("-" * 40)

    res2 = chain.invoke(base_order, config={
        "configurable": {"channel": "app", "vip": True}
    })
    print("场景2结果：", res2)