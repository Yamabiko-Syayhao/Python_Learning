"""
try 是python中用于异常处理的核心语法，让程序在遇到错误的时候不会直接奔溃，而是可以优雅的处理

语法
    try:
        # 可能出错的代码
        代码块
    except 异常类型:
        # 出错的时候执行的代码 捕获到异常之后继续执行
        异常处理代码
    else:
        # 没有出错时可以执行，（可选）
        正常逻辑
    finally:
        # 程序无论是否报错都会执行（可选）
        pass


"""


"""
try:
    # 可能会出现的错误代码
    num = int("abc")
# 这种except后边不写类型的写法，叫做裸except，意思是捕获所有类型的异常 不建议写，因为太宽泛了
except:
    print("代码出错了")
"""



"""
常见异常类型
    ValueError 值不对
    TypeError 类型不对
    KeyError 字典的键不存在
    FileNotFoundError 文件不存在
    IndexError 下标越界（找不到）
    Exception 通用异常 大多数错误都能被捕获到 建议用这种

"""

try:
    # int("abc")
    # 1 + "aabc"
    ssada
    num = int("123")
except ValueError as e:
    print(f"报错原因1：{e}")
except TypeError as e:
    print(f"报错原因2：{e}")
except KeyError as e:
    print(f"报错原因3")
except Exception as e:
    print(f"报错原因4：{e}")
else:
    print("成功走到了else",num)
finally:
    print("无论是否报错都会执行")
