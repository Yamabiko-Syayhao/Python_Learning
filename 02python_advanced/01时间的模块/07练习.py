"""
需求：
    请输入日期（格式如下20201002）后回车
    请输入您需要往后延迟几天：用户输入
    最终输出结果 您推算的日期是---时间
"""

from datetime import datetime,timedelta
# 我写的
# enter_time_str = input("请输入日期（格式例为20201002）：")
# enter_days = int(input("请输入你需要往后延迟几天："))
# # 转成时间对象
# enter_time = datetime.strptime(enter_time_str, "%Y%m%d")
# timedelta_days = timedelta(days=enter_days)
# last_date = enter_time + timedelta_days
# print(f"您推算的日期是：{last_date}")


# 老师写的
date_str = input("请输入日期（格式为20201002）后回车：")
days_str = int(input("请输入您需要往后延迟几天："))

# 进行格式转换 字符串--->
start_time = datetime.strptime(date_str, "%Y%m%d")

# 时间计算 往后推迟days_str天
end_time = start_time + timedelta(days=days_str)
print(end_time,type(end_time)) # datetime对象
end_time_str = end_time.strftime("%Y-%m-%d")
print(f"您推算的日期是---{end_time_str}",type(end_time_str))  # 转换输出后的类型和格式

# 优化一下 捕获异常 用户如果输入不符合要求的时间不至于崩溃



