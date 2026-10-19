# 整个流程就像"去图书馆借书"：
# 进门(connect) -> 找管理员(cursor) -> 递纸条提要求(execute) -> 看结果(row) -> 道谢走人(close)
# 顺序不能乱，一环扣一环。

# 1.导入pymysql包 uv add pymysql
from pymysql import *
# 2.创建数据库链接
# 就像"走到图书馆门口，刷卡进门"：不进门就摸不到书
"""
host：数据库地址 有可能是ip地址也可能是域名 localhost/127.0.0.1
      就像"图书馆在哪儿"（本机或某个IP）
user：数据库的用户名
     就像你的学生卡号
password：数据库的密码
     就像你学生卡的密码
database：连接哪个数据库的名称
     就像你要进哪个书库（图书馆有很多个书库）
charset：编码格式 防止乱码
     就像"说普通话"，不然管理员听不懂你在讲什么
"""

conn = connect(host='localhost', port=3306, user='root', password='352130789Slh', database='user',charset='utf8')

# 3.打开游标--打开数据库
# 就像"请一个管理员帮你拿书"：你不能自己乱翻书架，得有个中间人替你取书、放书
cur = conn.cursor()
# 4.指定sql语句
try:
    sql = "insert into test values (null, %s, %s, %s)"
    params = [
        ("经纪人","66666","38"),
        ("viola","66666","16"),
        ("koharu","2323","16")
    ]
    # cur.execute(sql, params1) # 单挑添加用这个没有many
    # params1 = ("koharu","2323","false") # (1366, "Incorrect integer value: 'false' for column 'age' at row 1")
    cur.executemany(sql, params) # 批量多条有many
    conn.commit() # 最后需要确认添加
    print("数据新增成功！")
except Exception as e:
    print("添加失败了！",e)
    conn.rollback()

# 5.关闭游标--关闭数据库
cur.close()
# 6.关闭连接
conn.close()





