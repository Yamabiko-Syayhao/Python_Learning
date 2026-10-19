# 闭包函数简单来说就是在函数体内部又定义了一个函数,并且将函数内部的函数返回出去
def say_hello(name):
    # 定义在函数内部的函数
    def say(msg):
        print(f"对着{name}说:{msg}")
    print(name,"第一次打印name")
    say("hello")
    print(name,"第二次打印name")
    # 把内部函数返回出去 形成闭包函数
    return say

if __name__ == "__main__":
    # 将内部的函数say返回出去 给sa使用
    sa = say_hello("藤都子")
    sa("你画画吗?")