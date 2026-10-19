# 闭包函数简单来说就是在函数体内部又定义了一个函数,并且将函数内部的函数返回出去
def say_hello(name):
    # 定义在函数内部的函数
    def say(msg):
        # 告诉解释器 name是外部函数的变量
        nonlocal name
        name = "arl"
        print(f"对着{name}说:{msg}")
    print(name,"第一次打印name") # 第一个name拿的是外面传入的name
    say("hello") # 第二个name是被修改之后的name
    print(name,"第二次打印name") # 第三个name还是被修改之后的name
    # 把内部函数返回出去 形成闭包函数
    return say

if __name__ == "__main__":
    # 将内部的函数say返回出去 给sa使用
    sa = say_hello("藤都子")
    sa("你画画吗?")
    sa("你唱歌吗?")