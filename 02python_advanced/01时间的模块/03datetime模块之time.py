# datetime 中time类 ---专门处理时间的 时分秒
from datetime import time

# 1.创建time时间对象
# t1 = time(10,20,30)
t1 = time(12, 20, 30,20)
print(t1)

# 2.获取time对象里面的时分秒
print(t1.hour,t1.minute,t1.second)


# 3.替换time时间对象中部分属性的值
t2 = t1.replace(hour=11,minute=3,second=30) # t1里面的值被替换了
print(t2)

print(t1.strftime("%H时%M分%S秒"))
print(t1.strftime("%H:%M %p")) # 加 %p 会多输出一个am 或者 pm








