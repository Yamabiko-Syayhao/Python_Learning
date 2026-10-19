"""
python最具有特色的是利用空格缩进表示代码块

单分支语句
    if 条件成功时执行：
        执行体

双分支语句
    if 条件成功时执行:
        逻辑
    else:
        条件失败时执行的逻辑

多分支语句
    if 条件成功时执行:
        逻辑
    elif 条件成功时执行：
        逻辑
    。。。一片elif
    else:
        上边的条件都不成立执行的逻辑
"""
a = 1
b = 2
# 单分支语句
# if a < b:
#     print("666")

# 双分支语句
# if a > b:
#     print('条件成立')
# else:
#     print("条件不成立")

# 多分支语句
# if a > b:
#     print('a比b大')
# elif a == b:
#     print('a与b相等')
# else:
#     print('a小于b')

# 输入一个年龄 0~18 输出未成年回家喝奶去，18~65之间 输出天选的牛马  65-85 输出老登一个 85以上牛坚强
age = int(input("请您输入您的年龄："))
if age >=0 and age < 18:
    print("未成年回家喝奶去")
elif 18 <= age < 65:
    print("天选的牛马")
elif 65 <= age < 85:
    print("老登一个")
else:
    print("牛坚强一个")


# 学校教务系统分为三类角色 超管  管理员  普通用户  你需要根据用户输入的账号密码去匹配角色进行不一样的输出
userName = input("请您输入您的账号：")
passWord = input("请输入您的密码：")
if userName == "admin" and passWord == "123456":
    print("欢迎你 优秀的超级管理员大佬")
    print("您看到的是别人看不到的界面")
elif userName == "lxl" and passWord == "xlaichijiaozi":
    print("欢迎你 小小的管理员")
elif userName == "byesame" and passWord == "666666":
    print("你就是最卑微的普通用户")
else:
    print("big胆，账号密码都不对，登录失败")