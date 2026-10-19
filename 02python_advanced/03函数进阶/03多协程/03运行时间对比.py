# 同步运行时间
# import time
# def work(name:str,delay:int):
#     print(f"同步任务{name}开始,等待{delay}s")
#     time.sleep(delay)
#     print(f"同步任务{name}结束")
#     return f"{name}结果"
#
# def run():
#     start = time.time()
#     print("====开始同步执行====")
#     #逐个运行 串行排队
#     work("A",2)
#     work("B",1)
#     work("C",4)
#     end = time.time()
#     print(f"同步总耗时{end-start:.1f}s")
#
# if __name__ == "__main__":
#     run()

# 异步运行时间 create_task 用于并发调度协程的核心函数,可以把一个协程包装成task对象,并立即
# 排入时间循环

# import time
# import asyncio
# async def work(name:str,delay:int):
#     print(f"异步任务{name}开始,等待{delay}s")
#     await asyncio.sleep(delay) # 异步等待几秒 让出执行权可以调度别的任务
#     print(f"异步任务{name}结束")
#     return f"{name}结果"
#
# async def run():
#     start = time.time() # 获取开始时间
#     print("====开始异步执行====")
#     #创建task 协程会
#     task1 = asyncio.create_task(work("A",2))
#     task2 = asyncio.create_task(work("B",1))
#     task3 = asyncio.create_task(work("C",4))
#     # 需要自己去await 需要结果再去await
#     await task1
#     await task2
#     await task3
#     # 没有await 直接往下走
#     end = time.time() # 获取结束时间
#     print(f"异步总耗时{end-start:.1f}s")
#
# if __name__ == "__main__":
#     asyncio.run(run())
#


import time
import asyncio
async def work(name:str,delay:int):
    print(f"异步任务{name}开始,等待{delay}s")
    await asyncio.sleep(delay) # 异步等待几秒 让出执行权可以调度别的任务
    print(f"异步任务{name}结束")
    return f"{name}结果"

async def run():
    start = time.time() # 获取开始时间
    print("====开始异步执行====")
    task_list = [
       work("A",2),
       work("B",1),
       work("C",4)
   ]
    # gather并发执行所有的协程
    result = await asyncio.gather(*task_list)
    print(result,"结果666")
    # 没有await 直接往下走

    end = time.time() # 获取结束时间
    print(f"异步总耗时{end-start:.1f}s")

if __name__ == "__main__":
    asyncio.run(run())


"""
gather和create_task区别
    返回结果：
        gather 一次给所有任务的列表，按照传入顺序返回
        create_task 每个 Task 各自给结果，返回的是一个task对象
    启动时间：
        create_task 立刻执行
        gather 执行到await才能启动
    灵活度：
        create_task 分散创建，可以随时取消某个任务 task.cancel()
        gather 一次性启动一批任务 同时启动，灵活度上有欠缺

    create_task：把任务一个个安排出去，得到每个任务自己的“句柄”
    gather：把一组可等待对象交给它安排并统一等待、收集结果
    
    gather底层是由create_task封装来的，它内部会自动把协程包装成task，所以传协程
    或者task，都可以
    
    gather(work("a"),work("b")) 其中work()是协程函数
        内部自动转换：create_task("a") + create_task("b") + await两个都完成
        等价于：
        taskA = create_task(work("a"))
        taskB = create_task(work("b"))
        await gather(taskA,taskB)
"""







