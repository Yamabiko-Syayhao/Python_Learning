# 循环  就是把一件事重复的去做
"""
    for 变量 in range(参数1,参数2,参数3):
        循环体--重复执行的那段代码

    range()函数  生成整数序列
        参数1：起始数字  数字从几开始循环 默认是0，非必填
        参数2：结束数字 循环到第几个数字结束 不包含结束数字  必填
        参数3：步长 默认是1  非必填  步长就是每次循环跳几个数
                如果步长为1    0 1 2 3 4 5。。。。
                如果步长为2    0 2 4 6 8 10。。。
                如果步长为3    0 3 6 9 12。。。
"""

# for i in range(3):
#     # 0 1 2
#     print(i)

# 从1开始循环  到10结束，默认步长为1  不换行
# for i in range(1,10):
#     print(i,end="")

# 从10开始循环 到15结束 步长为2   10  12  14
# for i in range(10,15,2):
#     print(i,end="---")


# break 和 continue
# break 跳出整个循环
# continue  跳出当前循环 开始执行下一次循环

for i in range(12,22):
    # 当i等于18的时候 跳出整个循环  18后边的循环不执行
    # if i == 18:
    #     break

    # 如果i等于18  那么就跳出当前循环  执行下一次循环19 20 21
    if i == 18:
        continue
    print(i)
print('我跑出来了哈哈')


# 练习  求1-100之间的偶数和
# 1-100之间的偶数和是xxx

# 方式1
# 放和
sum1 = 0
for i in range(0,101,2):
    # print(i)
    sum1 += i
    # print(f"每次的结果{sum1}")
print(f"1-100之间的偶数和是{sum1}")

# 方式2
sum2 = 0
for i in range(1,101):
    # 能被2整除的数==偶数
    if i % 2 == 0:
        sum2 += i
print(f"1-100之间的偶数和是{sum2}")

# 方式3
sum3 = 0
for i in range(1,101):
    # 奇数  跳出本次循环
    if i % 2 != 0:
        continue
    sum3 += i
print(f"1-100之间的偶数和是{sum3}")

# 找100-1000之间的水仙花数  个位数的立方+十位数的立方+百位数的立方=这个数本身
# 比如153=1+125+27
for num in range(100,1000):
    gw = num % 10
    sw = num // 10 % 10
    bw = num // 100
    if gw ** 3 + sw **3 + bw **3 == num:
        print(f"{num}是水仙花数")