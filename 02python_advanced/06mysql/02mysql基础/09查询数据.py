# 1.导入pymysql包 uv add pymysql
from pymysql import *
# 2.创建数据库链接
conn = connect(host='localhost', port=3306, user='root', password='352130789Slh', database='user',charset='utf8')

# 3.打开游标--打开数据库
cur = conn.cursor()
# 4.指定sql语句
# 需求 查询users表中年龄大于12的数据
sql = "select userName,age from users where age > %s"
params = (12,)
cur.execute(sql,params)
conn.commit()

result = cur.fetchall()
# fetchall 获取所有数据
# fetchone 获取第一个数据
print(result)
for row in result:
    print(row)


# 5.关闭游标--关闭数据库
cur.close()
# 6.关闭连接
conn.close()