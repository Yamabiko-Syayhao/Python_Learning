# 普通函数
# def fn1():
#     return 66
# result = fn1()
# print(result)

"""
普通函数:def定义, 立即执行 按顺序执行
"""
#协程函数
async def fn2():
    return 33
# result2 = fn2()
# print(result2) # <coroutine object fn2 at 0x000001632D5631C0>

"""
1.普通函数:def定义 调用后立即执行 按顺序去执行
2.协程函数:用async def 定义的函数,直接调用协程函数不执行,返回一个协程对象
    async def 函数名():
        pass
需要用await或者asyncio.run才能拿到结果
3.await:停下来等这件事做完,等待期间去干别的工作
    await只能写在async def函数名()里面
    await后面是需要等待的任务(网络请求,协程)
4.事件循环asyncio 一个包
    asyncio.fun(协程函数()) 工作开始启动
"""

# 想拿到结果
# 引入事件循环模块,asyncio用于编写并发代码的库
import asyncio

# 方法一 asyncio.run()
re = asyncio.run(fn2())
print(re)

# 方法二 在另一个协程里面用await
async def fn3():
    result2 = await fn2() # 等待fn2完成 然后拿到返回值33
    return result2
print(asyncio.run(fn3())) # 最后会打印两次33 fn2本身返回的33，fn3返回的result2
# 里面拿到的33













