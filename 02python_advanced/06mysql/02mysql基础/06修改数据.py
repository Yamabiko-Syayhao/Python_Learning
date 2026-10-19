# 1.导入pymysql包 uv add pymysql
from pymysql import *
# 2.创建数据库链接
conn = connect(host='localhost', port=3306, user='root', password='352130789Slh', database='user',charset='utf8')

# 3.打开游标--打开数据库
cur = conn.cursor()
# 4.指定sql语句
# 需求找到test表中 id为2的那条数据 把用户名改为htr 年龄改为14
try:
    sql = "update test set userName=%s, age=%s where id=2"
    params = ("htr",14) # params 必须传元组或者列表
    cur.execute(sql, params)
    conn.commit() # 最后需要确认添加
    print("数据修改成功！")
except Exception as e:
    print(e,"修改失败了！")
    conn.rollback()


# 5.关闭游标--关闭数据库
cur.close()
# 6.关闭连接
conn.close()