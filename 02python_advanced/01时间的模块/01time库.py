# time时间模块 处理时间 时间戳 时间格式化等操作
# 时间戳：从1970-01-01 00：00：00 到今天的毫秒数


# 1.获取当前系统时间的时间戳
import time
# for i in range(10):
#     time.sleep(1)
print("系统时间-时间戳",time.time())
print("系统时间-时间戳-纳秒",time.time_ns())


# 2.获取当前时间
# 格式：星期几 月份 日期 时分秒 年份
print(time.ctime())

# 3.根据指定的时间戳 转换成日期格式的字符串
print("时间戳转日期",time.ctime(1790343215.0364976)) # 括号里面是时间戳

# 4.获取一个当前时间的结构化时间
# struct_time 一个时间元组对象
# 年 时 分 秒 星期（0 = 星期一） 一年当中的第几天 令时
print(time.localtime())


# 5.UTC世界时间（全世界共用的标准基准时间，是所有时区计算的参考物）
print("当前的utc时间",time.gmtime())

# 6.单独获取年月日字段
localT = time.localtime()
print(localT.tm_year,"year")
print(localT.tm_mon,"month")
print(localT.tm_mday,"day")

# 7.时间元组对象struct_time --- > 字符串
print("当前的北京时间",time.strftime("%Y年%m月%d日 %H：%M：%S",time.localtime()))
print("当前的utc时间",time.strftime("%Y年%m月%d日",time.gmtime()))

# 8.字符串--->时间元组对象
print("字符串转时间元组对象",time.strptime("2021-10-01","%Y-%m-%d"))

# 9.封装执行1秒
time.sleep(1)








