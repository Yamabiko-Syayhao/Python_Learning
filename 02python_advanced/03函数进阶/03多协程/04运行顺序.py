import asyncio
async def work(name,delay):
    print(f"{name}开始")
    await asyncio.sleep(delay)
    print(f"{name}结束")
    return f"{name}-over"
async def main():
    t1 = asyncio.create_task(work("A",2))
    t2 = asyncio.create_task(work("B",1))

    await asyncio.sleep(0.1)

    print("主协程继续干别的...")

    r1 = await t1
    r2 = await t2

    print("结果",r1,r2)
asyncio.run(main())


# 事件循环是单线程的，任何时刻只有一个协程在跑


