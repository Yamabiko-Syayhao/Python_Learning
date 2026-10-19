# # 先建个表
# # 1.导入pymysql包 uv add pymysql
# from pymysql import *
# # 2.创建数据库链接
# conn = connect(host='localhost', port=3306, user='root', password='352130789Slh', database='user',charset='utf8')
#
# # 3.打开游标--打开数据库
# cur = conn.cursor()
# # 4.指定sql语句
# # cur.execute("""
# #     CREATE TABLE users1 (
# #         id INT PRIMARY KEY AUTO_INCREMENT,
# #         name VARCHAR(50),
# #         age INT,
# #         email VARCHAR(50),
# #         city VARCHAR(50)
# #     )
# # """)
# # 插入测试数据
# data = [
#     ("张三",22,"123@qq.com","北京"),
#     ("李四",23,"1234@qq.com","南京"),
#     ("王五",24,"qwe@qq.com","燕京")
# ]
# cur.executemany("insert into users1(name,age,email,city) values(%s,%s,%s,%s)",data)
# # cur.executemany("insert into users1 values(null,%s,%s,%s,%s)",data) 或者用这种插入
# conn.commit()
#
# # 5.关闭游标--关闭数据库
# cur.close()
# # 6.关闭连接
# conn.close()
# ==================== 以上是先建好了一个表 然后表里面插入数据 ====================

# 索引：索引类似于书的目录，没有目录的时候，如果你想去找内容就要一页一页翻（全表扫描）
# 有目录就可以快速定位
# 本质上就是一种排好的数据结构，存储“字段值--->行位置”的映射

# 1.导入pymysql包 uv add pymysql
from pymysql import *
# 2.创建数据库链接
conn = connect(host='localhost', port=3306, user='root', password='352130789Slh', database='user',charset='utf8')

# 3.打开游标--打开数据库
cur = conn.cursor()
# 4.指定sql语句
# ==================== 创建不同类型的索引 ====================
# 1.普通索引
# 给user1这个表的name上创建一个名字叫idx_name的普通索引，作用就是当执行where name=...
# 这类查询的话就会走索引，而不是进行全表扫描
# cur.execute("create index idx_name on users1(name)")

# 2.唯一索引 适合加载本身值就是唯一的列 比如身份证号、手机号、用户名、邮箱
# 给users1表的email列上一个名字叫idx_email的唯一索引 有unique关键字 所以不能重复
# 这个既能加速查询 也能保证数据的唯一性
# cur.execute("create unique index idx_email on users1(email)")

# 3.联合索引/复合索引（最常用）
# 给test表中的age和city两列上创建一个名字叫idx_age_city的复合索引
# 相当于一次性给两列建了索引 索引的顺序很重要 现在的顺序是age在前 会先按照age排
# 再按照city排
# cur.execute("create index idx_age_city on users1(age,city)")
# where age = 66
# where city = "北京" # 跳过左侧age列，直接到city 那就命中不了索引
# where age like "%6"  加了%也命中不了
# where city = "北京" and age = "66" # 这个就可以了 因为用的and

# conn.commit()

cur.execute("show index from users1")
for row in cur.fetchall():
    print(row)
# print(cur.fetchall()) fetchall方法可以打印对应数据表里面你想要的数据
# cur.execute("select * from users1")
# for row in cur.fetchall():
#     print(row)

# 5.关闭游标--关闭数据库
cur.close()
# 6.关闭连接
conn.close()


