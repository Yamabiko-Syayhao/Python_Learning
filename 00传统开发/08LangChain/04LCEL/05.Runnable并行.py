'''
1. 输入值 `5` **同时发给 3 个任务**：平方、立方、+10，三个任务一起跑，谁都不用等谁
2. 每个任务单独算出自己结果
3. RunnableParallel 自动把全部结果打包成一个字典，key 就是我们自己定义的名字
4. 和串行`|`区别：
   - 串行 A|B：A 跑完，A 的输出传给 B，先后执行
   - 并行：同一个输入分给多个组件，同时执行，最后合并结果
'''
# 导入类型注解
from typing import Any, Dict
# 导入并行工具RunnableParallel、简易函数包装RunnableLambda
from langchain_core.runnables import RunnableParallel, RunnableLambda

# ---------------------- 定义3个独立计算逻辑 ----------------------
# 逻辑1：计算数字的平方
def calc_square(num: int) -> int:
    return num * num

# 逻辑2：计算数字的立方
def calc_cube(num: int) -> int:
    return num * num * num

# 逻辑3：计算数字+10
def calc_add10(num: int) -> int:
    return num + 10

# 使用RunnableLambda把普通函数包装成流水线可执行组件
square_run = RunnableLambda(calc_square)
cube_run = RunnableLambda(calc_cube)
add10_run = RunnableLambda(calc_add10)

# ====================== 定义并行任务 ======================
# RunnableParallel：接收字典，key是结果别名，value是要并行执行的组件
parallel_chain = RunnableParallel({
    "平方": square_run,
    "立方": cube_run,
    "加十": add10_run
})

# 执行并行链路，输入数字 5
result = parallel_chain.invoke(5)

# 打印最终合并后的结果字典
print(result)
