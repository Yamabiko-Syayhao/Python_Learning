"""import asyncio
async def work(name):
    try:
        # 模拟耗时五秒 是可被打断的等待 如果在这五秒内有人调用cancel()，
        # sleep会立刻抛出CancelledError，不会真等待五秒
        await asyncio.sleep(5)
        print(f"{name}执行完毕")
    except asyncio.CancelledError:
        print(f"{name}被取消")
        raise # 必须重新抛出异常 如果捕获到CancelledError后不重新抛出，
        # await task就不知道任务被取消了，会破坏asyncio的取消传播机制

async def main():
    # 创建task对象的一瞬间就被加入了事件循环队列了，等待当前协程（main）让出控制权
    # （也就是遇到了await），它们才会被调度执行
    task_list = [
        asyncio.create_task(work("任务A")),
        asyncio.create_task(work("任务B")),
        asyncio.create_task(work("任务C"))

    ]
    await asyncio.sleep(2)
    for i,task in enumerate(task_list):
        # 如果下标为1就取消任务 任务B
        if i == 1:
            task.cancel() # 发起取消任务

    # for task in task_list:
    #     try:
    #         # 等待单个任务完成
    #         await task
    #     except asyncio.CancelledError:
    #         pass
    # gather 等待所有的任务结束 return_exceptions = True 让被取消的异常不打断
    # 整体"""
#     await asyncio.gather(*task_list,return_exceptions=True)
#
#     # await asyncio.gather(*task_list)
# asyncio.run(main())

# 执行输出顺序 重点


"""
run(main())  执行三个create_task ---> 就绪队列：[main,A,B,C]
main的await asyncio.sleep(2) -->让出 -->跑A
A的await asyncio.sleep(5) -->让出 -->跑B
B的await asyncio.sleep(5) -->让出 -->跑C
C的await asyncio.sleep(5) -->让出 -->队列清空没东西了，等待
2秒之后
main开始了 B.cancel()      -->B 进就绪序列（因为B被取消了）
main await task(A)      --> 让出 --> 跑B
B抛出CanceledError raise  -->B结束
五秒之后
A到点了 -->跑A 任务A执行完毕
C到点了 -->跑C 任务C执行完毕
"""





import asyncio
async def work(name):
    try:
        await asyncio.sleep(5)
        print(f"{name}执行完毕")
    except asyncio.CancelledError:
        print(f"{name}被取消")
        raise

async def main():
    # 把三个协程交给gather
    gather_future = asyncio.gather(
        work("任务A"),
        work("任务B"),
        work("任务C")
    )
    # 主线程main 等待两秒后 把整个gather取消（三个任务全被取消了）
    await asyncio.sleep(2)
    gather_future.cancel()

    try:
        await gather_future
    except asyncio.CancelledError:
        print("gather已被取消，程序正常退出")

asyncio.run(main())

