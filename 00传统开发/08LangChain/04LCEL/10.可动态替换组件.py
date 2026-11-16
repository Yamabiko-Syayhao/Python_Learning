# 网页端满100减10，APP端满80减15，小程序满50减20
# RunnableSerializable 可序列化的运行组件
# ConfigurableField 把类的属性标记为“运行时可动态修改的配置字段”
from langchain_core.runnables import RunnableSerializable, ConfigurableField


# 优惠券计算组件类 继承了RunnableSerializable 就具备了可配置的能力
class Coupon_Calc(RunnableSerializable):
    # 默认满减门槛 消费满100元才可以用券
    full_money: int = 100
    # 默认抵扣金额 满足门槛优惠10元
    reduce_money: int = 10
    # 重写invoke输入订单数据order 返回计算结果 config运行时配置
    def invoke(self,order,config=None):
        price = order['pay_price']
        if price >= self.full_money:
            # 券后的价格
            final = price - self.reduce_money
            use_coupon = True
        else:
            final = price
            use_coupon = False
        # 返回了字典 里面有完整的计算结果
        return {
            "original_price": price, # 原价
            "use_coupon": use_coupon, # 是否使用优惠
            "pay_after_coupon": final, #
        }
# 将类当中的两个变量标记为“运行时可动态修改的配置字段”
# configurable_fields() 返回新对象 必须赋值接收
base_coupon = Coupon_Calc().configurable_fields(
    full_money = ConfigurableField(
        id = "full_money", # 配置唯一标识 必须跟属性名一致 修改配置时用这个id
        name = "满减门槛", # 中文展示名称 用于文档展示
        description="达到该门槛时才能使用优惠卷" # 字段描述说明
    ),
    reduce_money = ConfigurableField(
        id = "reduce_money",
        name = "减免金额",
        description = "满足门槛抵扣多少钱"
    )
)

# with_config 拿着基础的模板base_coupon 克隆出一个“预设好某些配置”的新副本 原模板不受影响
web_coupom = base_coupon.with_config(config={
    "full_money": 100,
    "reduce_money": 10,
})

app_coupom = base_coupon.with_config(config={
    "full_money": 80,
    "reduce_money": 15,
})

mini_coupom = base_coupon.with_config(config={
    "full_money": 50,
    "reduce_money": 20,
})


if __name__ == "__main__":
#     准备一条测试的订单，商品总价是90元
    test = {"pay_price":90}
    print(web_coupom.invoke(test))


