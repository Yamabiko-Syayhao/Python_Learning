
## 综合练习三：订单处理与分析管道

### 需求描述
构建一个电商订单处理管道，要求：

1. **原始订单保留**：使用 `RunnablePassthrough` 将原始订单数据一路传递下去。

2. **并行计算**：使用 `RunnableParallel` 同时并行执行以下两个计算：
   - `subtotal`（商品小计）：所有商品 `price * quantity` 求和，保留 2 位小数
   - `shipping`（运费计算）：根据城市判断——如果城市在 `['北京', '上海', '广州', '深圳']` 则运费 8 元，否则 12 元

3. **数据扩展**：使用 `RunnablePassthrough.assign()` 依次追加以下字段：
   - 追加 `subtotal` 和 `shipping` 字段（来自并行计算结果）
   - 追加 `discount` 字段：通过 `config` 传入 `channel` 和 `user_type` 计算折扣
     - App 渠道：优惠 5%
     - VIP 用户：额外优惠 10%
   - 追加 `total` 字段：`subtotal + shipping - discount`

4. **JsonOutputParser 输出摘要**：最终使用 `JsonOutputParser` 让模型生成一段订单摘要 JSON，包含：
   - `order_id`：订单编号
   - `item_count`：商品种类数
   - `total`：应付金额
   - `summary_text`：一句话摘要（如"尊敬的张三，您购买了3类商品，应付 12098.00 元"）

5. **config 情景测试**：对同一笔订单分别用以下配置测试，打印不同结果：
   - Web 普通用户：`channel='web'`, `user_type='normal'`
   - App VIP 用户：`channel='app'`, `user_type='vip'`

测试订单数据：
```python
order = {
    'order_id': 'OD-20260520-001',
    'customer': '张三',
    'city': '北京',
    'items': [
        {'goods_name': '机械键盘', 'price': 320.0, 'quantity': 1},
        {'goods_name': '鼠标', 'price': 89.0, 'quantity': 2},
        {'goods_name': '显示器', 'price': 1599.0, 'quantity': 1},
    ]
}
```
