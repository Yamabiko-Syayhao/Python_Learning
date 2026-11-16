# 导入两个核心工具
# RunnableLambda：把普通Python函数包装成流水线能用的Runnable零件
# RunnablePassthrough：数据透传组件，原样保留上游数据，搭配assign可以追加新字段

from langchain_core.runnables import RunnableLambda, RunnablePassthrough

# 订单预处理函数：给订单缺失的字段补上默认值
# order是字典，是传进来的订单字典
def normal_order(order):
    # get取值，city不存在就赋值青岛；coupon不存在默认0；**order展开原始字典，保留全部原有数据
    return {"city": order.get("city", "青岛"), "coupon": order.get("coupon", 0), **order}

# 计算商品总价：遍历商品列表，价格 × 数量全部相加，结果保留2位小数
def calc_total(order):
    # [8,9,800]
    # sum([9,8,800]) = 817
    # round(817, 2) = 817.00
    # 循环items里每一件商品，计算单价乘数量求和，round保留两位小数
    return round(sum(item["price"] * item["quantity"] for item in order["items"]), 2)

# 计算运费逻辑：偏远地区运费12元，普通城市6元；VIP会员减4元，运费最低不能为负数
def calc_shipping(order):
    # 三元表达式判断城市是否属于偏远地区，设置基础运费
    shipping = 12.0 if order["city"] in ["新疆", "西藏", "内蒙古", "青海", "宁夏"] else 6.0
    # 判断是否是VIP，如果是，运费减4块钱
    if order.get("is_vip", False):
        shipping -= 4.0
    # max保证运费最小是0，防止减免后变成负数
    return max(shipping, 0)

# 计算最终实付金额：商品总价 + 运费 - 优惠券金额，保留两位小数
def calc_total_real(order):
    # 817 + 2 - 9 = 810.00
    return round(order["total"] + order["shipping"] - order["coupon"], 2)

# 拼接订单文本摘要，生成一句可读的订单说明文字
def build_summary(order):
    # f-string格式化字符串，读取字典里已经计算完成的各个值
    return f"客户{order['customer']},一共买了 {len(order['items'])} 类商品，应付{order['total_real']} 元 （运费{order['shipping']}元）"
# 每个函数时依赖上游哪些字段？
# 函数	            依赖的上游字段	       产出字段
# normal_order	    原始 order	           补全 city/coupon
# calc_total	    items	                total
# calc_shipping	    city、is_vip	         shipping
# calc_total_real	total、shipping、coupon	 total_real
# build_summary	     customer、items、total_real、shipping	summary

# 使用 | 管道符组装完整LCEL流水线，数据从上到下自动传递
line = (
    # 第一步：调用预处理函数，补全订单缺失字段
    RunnableLambda(normal_order)
    # 纯透传组件：接收上游字典，原封不动传给下游，就是个"复读机"  现在没用，是给未来留的扩展点预留位置方便以后新增业务逻辑
    | RunnablePassthrough()
    # assign方法：保留原数据  追加新字段  保留上游所有key，并行计算新增total、shipping两个字段，合并进字典 为什么一下走俩，因为total 和 shipping 互不依赖，可以并行
    | RunnablePassthrough().assign(
        total=RunnableLambda(calc_total),    # 计算商品总价，存入key：total
        shipping=RunnableLambda(calc_shipping)# 计算运费，存入key：shipping
    )
    # 在上一步完整字典的基础上，追加实付金额字段 total_real
    | RunnablePassthrough().assign(
        total_real=RunnableLambda(calc_total_real)
    )
    # 继续追加订单摘要文本字段 summary
    | RunnablePassthrough().assign(
        summary=RunnableLambda(build_summary)
    )
)

# 程序入口，只有直接运行这个文件时代码才会执行
if __name__ == "__main__":
    # 定义用户提交的原始订单字典数据
    order = {
        "customer": "先亮",
        "city": "青岛",
        "coupon": 9,
        "is_vip": True,
        "items": [
            {"goods_name": "桃", "price": 9, "quantity": 1},
            {"goods_name": "仓鼠", "price": 8, "quantity": 1},
            {"goods_name": "茶叶", "price": 800, "quantity": 1},
        ]
    }
    # 触发整条流水线运行，自动串行+并行完成全部计算
    res = line.invoke(order)
    # 打印加工完成后的完整订单字典
    print('最终结果：', res)
    # 单独打印生成好的订单摘要文本
    print("摘要", res["summary"])
