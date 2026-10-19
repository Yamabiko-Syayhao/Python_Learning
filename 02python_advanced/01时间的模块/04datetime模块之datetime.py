# datetime模块中的datetime既能处理时间也能处理日期
from datetime import datetime



# 1.创建datetime对象
dt = datetime(2026,10,1,12,13,14)
print(dt)
print(dt,type(dt),"datetime时间对象")

ss = "2026-10-01 12:13:14"
print(ss,type(ss),"字符串类型")

# 2.获取系统当前日期+时间
dt2 = datetime.now()
print(dt2)



# 3.转换成时间元组对象
print(dt2.timetuple())
# 月份
print(dt2.timetuple().tm_mon)

# 4.格式化时间 时间对象-->字符串
dt3 = dt2.strftime("%Y年%m月%d日 %H:%M:%S")
print(dt3)

# 5.格式化时间 字符串--->时间对象
# 字符串 被转换成了时间对象
dt4 = datetime.strptime("2026-10-01 17:00:05","%Y-%m-%d %H:%M:%S")
print(dt4,type(dt4))



# 6.获取当前时间的时间戳
print(dt2.timestamp())




