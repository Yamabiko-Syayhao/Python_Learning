"""

在思维链每一步生成多个思考分支，模拟迷宫探索；对分支做评估剪枝，淘汰错误路径，保留优质分支继续推导，收敛最优解。

四步：拆分节点→发散分支→评估剪枝→回溯择优
✅适用：复杂规划、谜题、代码推导、博弈决策；❌简单任务不推荐

"""
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 调用的时候将{WorkspaceId} 替换为真实的业务空间id 阿里云百炼的业务空间管理
    base_url="https://ws-bggm9k3qgbthz61a.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
# 定义提示词
content = """
    你是一个营销专家，请用思维树ToT分层推理，为高校校园奶茶店制定淡季引流营销方案，店铺现状：秋冬淡季、学生客流减少、竞品店铺多、客单价偏低。
请严格按照树状步骤逐层分析输出：
    1. 拆解问题：分析校园奶茶店淡季客流少的核心原因、核心目标人群、本次方案核心目标
    2. 从产品优化、优惠活动、校园宣传、增值服务四个维度，分别列举至少5种引流方式
    3. 对每一种引流方式，分析其成本、引流效果、适配校园场景度、优缺点
    4. 筛选性价比最高、落地性最强的组合方案，制定详细落地执行计划
    5. 补充方案预算预估、效果评估标准、风险应对方案
"""
"""
思维树整体逻辑
    解决根本问题：看小明适合哪运动
    分支1：拆分小明运动能力素质分档
    分支2：去列举速度、力量、耐力这三方面对应的运动
    分支3：量化分析所有的运动对于速度、力量、耐力三项素质的要求
    分支4：结合小明之前的个人数据以及运动的素质要求汇总成适配报告
    
"""

"""
思维树提示词的通用模板
    你的身份：
    核心问题：
    请使用思维树ToT分步推理解决以下问题，禁止直接输出答案
    第一层：拆解问题，找已知条件，核心需求，待解决的痛点
    第二层：列举所有的方案，知识维度
    第三层：量化分析，对比各个分支内容的优劣及适配程度
    第四层：筛选最终结果，整合推理的所有过程，输出最严谨的答案
"""




completion = client.chat.completions.create(
    # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    model="qwen3.8-flash",
    messages=[
        {"role": "user", "content": content},
    ]
)
# json在线解析小工具   大模型给出的json格式可能不是很好查看  可以格式化一下   https://www.bejson.com/explore/index_new/index.html
# print(completion.model_dump_json())
print(completion.choices[0].message.content)



