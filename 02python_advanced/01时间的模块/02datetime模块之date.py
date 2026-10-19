"""
datetime 模块是处理日期和时间的标准库，包含以下几个核心类

date    只有日期（年-月-日）
time
datetime



"""

# 1.创建自定义日期---指定日期
from datetime import date
dd = date(2020, 10, 1)
# 自定义日期的date对象
print(dd, type(dd))

# 2.获取系统当前日期
day1 = date.today()
print(day1)

# 3.按照自定义格式 返回字符串
print(day1.strftime("%Y年%m月%d日"))


# 4.将date对象 转为time_struct_time 对象
print(day1.timetuple())

# 5.返回星期几
print(day1.weekday()) # 0-星期一 1-星期二 2-星期三 .... 6-星期日
print(day1.isoweekday()) # 1-星期一 2-星期二 .... 7-星期日

# 6.iso获取日历格式  返回一个包含 年份 第几周 周几的元组
print(day1.isocalendar())

# 7.替换日期中的某些值
new_date = day1.replace(year=2020)

print(new_date)





