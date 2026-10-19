"""
大乐透
    蓝色球前区号码  01-35中任选5个不重复号码  从小到大排列
    黄色球后区号码  01-12 中任选2个不重复号码，从小到大排列     形成号码组合进行投注
双色球
    红色球 01-33 中任选6个  从小到大排列
    蓝色球 01-16 中任选1个  形成号码组合进行投注
"""
import random
# 接收用户输入的注数
n = int(input("请您输入要下注的数量："))

def fn(a,b,c):
    """
    生成彩票号码
    :param a: 彩票类型（大乐透/双色球）
    :param b: 大乐透的前区/双色球的红球的最大值（大乐透35 双色球33）
    :param c: 大乐透后区/双色球的篮球的最大值（大乐透12 双色球是16）
    """
    # 用户下了几注  循环几次生成
    for i in range(n):
        # 生成1-35的列表/1-33的列表
        balls1 = [i for i in range(1,b+1)]
        # 生成1-12的列表/1-16的列表
        balls2 = [i for i in range(1,c+1)]
        if a == "大乐透":
            #随机抽取5个前区号码 以及 2个后区号码
            select_balls1 = random.sample(balls1,5)
            select_balls2 = random.sample(balls2,2)
        else:
            # 双色球  随机抽取6个红色球 以及1个蓝色球
            select_balls1 = random.sample(balls1, 6)
            select_balls2 = random.sample(balls2, 1)
        # 默认正序 从小到大
        select_balls1.sort()
        if a == "大乐透":
            select_balls2.sort()
        # 合并列表
        select_balls1.extend(select_balls2)
        # 非两位数 前边补0
        # print(select_balls1)
        # 不足两位整数  前边补0
        output = [f"{i:02d}" for i in select_balls1]
        print(output)
fn("大乐透",35,12)
print("=="*20)
fn("双色球",33,16)
