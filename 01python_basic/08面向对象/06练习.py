'''
 定义一个动物类 有动物名字 年龄 体重 有行走能力
再定义一个狗类 继承动物类 并且额外拥有毛色属性，还有看家的本领

设计一个类银行账户类
要求：
    1.属性： 账户id，账户拥有者姓名，余额
    2.余额不能在外部直接修改，只能通过方法操作
    3.方法：
        存款
        取款
        查询余额
    4.存款取款金额必须为整数 否则提示错误
'''



class Animal:
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight
    def walk(self, val):
        print(f"小狗{self.name},正在{val}散步")

class Dog(Animal):
    def __init__(self, name, age, weight, color):
        super().__init__(name, age, weight)
        self.color = color
    def see_home(self):
        print(f"小狗{self.name}，正在帮你看家。它的颜色是{self.color}")

dog1 = Dog("旺财","7","33kg","橘黄色")
dog1.see_home()
dog1.walk("公园")


print("=="*30)


class Bank_account:
    def __init__(self, account_id, name, balance= 0):
        self.account_id = account_id
        self.name = name
        # 私有属性
        self.__balance = balance
    def cunkuan(self, money):
        # money必须是整数
        if type(money) != int or money < 0:
            print("存款金额不是整数")
            return
        self.__balance += money
        print(f"存款成功，当前余额{self.__balance}")

    def qukuan(self, money):
        if money > self.__balance:
            print("余额不足")
            return
        if money <= 0:
            print("取款金额必须为正数")
            return
        self.__balance -= money
        print(f"取款成功，当前余额是{self.__balance}")
    def get_balance(self):
        return self.__balance

    

#     def deposit(self, amount):
#         if amount % 100 == 0:
#             self.__balance += amount
#             print(f"存款成功，存入{amount}元")
#         else:
#             print("请输入100倍数的整数！")
#
#     def withdraw(self, amount):
#         if self.__balance <= 0:
#             print("取款失败！你的余额已不足！")
#         elif amount % 100 == 0:
#             self.__balance -= amount
#             print(f"取款成功，取出{amount}元")
#         else:
#             print("请输入100倍数的整数！")
#
#     def check_balance(self):
#         return f"你的余额为{self.__balance}"
#
# account1 = Bank_account("385", "tdz", 100)
# # account1.deposit(300)
# # account1.deposit(100)
# # print(account1.check_balance())
# # account1.withdraw(200)
# # print(account1.check_balance())
# account1.withdraw(100)
# account1.deposit(500)
# account1.withdraw(100)
# print(account1.check_balance())
