# 2026-09-23 16：43：05
# 自己写的
# from datetime import datetime
# import time
# while True:
#     time.sleep(1)
#     date_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
#     print(f"\r{date_time}",end="")


import time

while True:
    # 暂停一秒 每隔一秒钟执行一次后面的代码
    time.sleep(1)
    # 获取系统时间 时间元组对象---->字符串
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    now_time = time.strftime("%Y-%m-%d %H:%M:%S") # 和上面一样，
    # 原文strftime第二个默认参数就是time.localtime()
    # print(now_time)
    print(f"\r{now_time}", end="")










