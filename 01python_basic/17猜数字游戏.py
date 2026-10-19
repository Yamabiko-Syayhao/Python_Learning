"""
    计算机自动生成一个1-100之间的随机数，用户输入自己猜的数字，计算机会给出对应的提示，
    如果用户输入的数字大了就提示【小一点】，
    如果用户输入的数字小了就提示【大一点】，
    如果用户猜对了就输出【恭喜你猜对了】，
    如果你七次都没猜对，给出温馨提示【你是个呆瓜吧】
"""

# random 系统内置的随机函数----可以生成随机数
import random

# 生成随机整数
# random.randint(a,b)   [a,b]
# random.randrange(a,b)   [a,b)

# 生成一个1-100之间的随机整数
a = random.randint(1, 100)

# 定义一个累加器 猜测的次数
num = 0
max_times = 7
# 判断条件
while True:
    # 累加器 需要+1
    num += 1
    shengyu = max_times - num

    # 用户输入数字
    b = int(input("请输入你猜的数字："))
    # 将用户输入的数字和计算机生成的随机数比较大小
    if a > b:
        if num != 7:
            print(f"你输入的数字有点小，大一点再试试,还剩下{shengyu}次机会")
    elif a < b:
        if num != 7:
            print(f"你输入的数字有点大，小一点再试试,还剩下{shengyu}次机会")
    else:
        print("恭喜你猜对了！")
        # 猜对了 就直接跳出整个循环就可以了
        break

    if num == 7:
        print('你是个呆瓜吧，这么多机会都猜不中！')
        # 给了你七次机会都没猜对  也直接跳出整个循环
        break
