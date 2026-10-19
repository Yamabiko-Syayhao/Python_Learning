# timedelta 表示的时间段/时间差 用于时间的加减运算
# datetime 表示的是日期+时间 用于获取当前时间，格式转换

from datetime import timedelta, datetime


# 1.创建一个时间差对象
# 天 小时 分钟 秒 毫秒
# td = timedelta(days=2,hours=3,minutes=5,seconds=30,microseconds=40)
# print(td,type(td)) # 时间差对象 <class 'datetime.timedelta'>

# 2.计算 当前时间+7天
# print(datetime.now()) # 获取当前时间
# + timedelta(days=7) # 往后推迟七天,这个时间差对象可以对时间对象进行加减 天数由自己设置
# print(datetime.now() + timedelta(days=7))

# 3.计算 当前时间-7天
# print(datetime.now() - timedelta(days=7))

# 4.将时间字符串转换成datetime对象
start_time_str = "2005/03/07 00:00:00"
end_time_str = "2026/9/24 10:10:15"
start_time = datetime.strptime(start_time_str, "%Y/%m/%d %H:%M:%S")
end_time = datetime.strptime(end_time_str, "%Y/%m/%d %H:%M:%S")
# format的输出格式必须和start_time_str的格式匹配，两边格式必须一样
print(start_time, type(start_time))
print(end_time, type(end_time))

# 两个datetime对象的差
t1 = end_time - start_time
print(t1, type(t1)) # t1就是一个时间差对象

# 5.从时间差对象中提取具体的数据
print(t1.days, type(t1.days)) # 从时间差对象t1 当中取出其中某个值


