# 1.导入pymysql包 uv add pymysql
from pymysql import *
# 2.创建数据库链接
conn = connect(host='localhost', port=3306, user='root', password='352130789Slh', database='user',charset='utf8')

# 3.打开游标--打开数据库
cur = conn.cursor()
# 4.指定sql语句
# 需求删除数据为2的那条数据
try:
    cur.execute("delete from users where id = 2")
    conn.commit() # 必须要有这个提交，要不然最后实际没有执行
    print("删除成功！")
except Exception as e:
    print(e,"删除失败！")
    conn.rollback()
# for row in cur.execute("select * from users"):
#     print(row)
# 5.关闭游标--关闭数据库
cur.close()
# 6.关闭连接
conn.close()