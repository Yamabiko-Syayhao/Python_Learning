"""
同步:执行这件事的同时要等上面执行完之后再执行,期间什么也不做.总共耗时是包括等待的时间加起来
异步:执行这件事的同时也去执行其他的事情,执行上一个事情的同时不等,总耗时是其中耗时最长的一件事

同步属于我亲自盯着,做完一件事再去做下一件事
异步属于我发起任务,不盯着,去干别的事情,完成了通知我
"""


"""
# 同步
import time
def task():
    time.sleep(5) # 阻塞等待五秒
    return "结束"
print("开始")
result = task()
print("结果",result)
print("结束")
"""
# 执行顺序:开始--->调用函数task[等待五秒]---->结果:结束----->结束
# 在其等待的五秒内,什么都干不了,这就是同步

# 异步
# import asyncio
# async def task():
#     # time.sleep(5) # 阻塞等待五秒
#     await asyncio.sleep(5) # 非阻塞等待五秒 挂起来本协程五秒,把控制权交还给事件循环,
#     # 在这期间可以执行其他任务
#     return "结束"
# async def main():
#     print("开始")
#     result = await task() # 执行task 交出控制器,但不阻塞事件循环,等待task返回结果
#     print("结果",result)
#     print("结束")
# 从这开始执行代码
# asyncio.run(main())
# 从这行看效果基本一样 原因是因为现在是单个任务



"""
并发
    "同时处理"多个任务的能力,不一定同时执行,通过任务切换,让多个任务交替执行推进,宏观上
    看起来类似"同时".一个人同时应付多件事   
并行:
    真正的同时执行多个任务,需要多核cpu
    多个人同时干不同的事

"""
# 并发多协程任务
import asyncio,time
async def task(name,delay):
    """
    描述函数是干什么的
    :param name: 任务的名称
    :param delay:  任务需要的时间
    :return:
    """
    await asyncio.sleep(delay)
    print(f"任务{name}好了")
async def main():
    start = time.time()
    # await asyncio.gather 让多个任务并发执行总耗时取决于时间最长的那一个
    await asyncio.gather(
        task("A",2),
        task("B",1),
        task("C",4)

    )

    print(f"总耗时{time.time() - start:.1f}")
asyncio.run(main())

