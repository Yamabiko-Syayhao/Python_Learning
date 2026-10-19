# 1.导入pymysql包 uv add pymysql
from pymysql import *
# 2.创建数据库链接
"""
host：数据库地址 有可能是ip地址也可能是域名 localhost/127.0.0.1
user：数据库的用户名
password：数据库的密码
database：连接哪个数据库的名称
charset：编码格式 防止乱码
"""

conn = connect(host='localhost', port=3306, user='root', password='352130789Slh', database='user',charset='utf8')

# 3.打开游标--打开数据库
cur = conn.cursor()
# 4.执行sql语句
try:
    userName = input("请输入用户名：")
    passWord = input("请输入密码：")
    age = input("请输入年龄：")
    sql = "insert into test values (null,%s,%s,%s)" # id userName passWord age
    params = (userName, passWord, age)
    cur.execute(sql, params) # 把输入的userName passWord age通过execute方法联系到一起
    # 这里userName passWord age一块放到了一个元组params里面
    # 提交保存
    conn.commit()
    print("数据保存成功了")
except Exception as e:
    print(e,"程序出错了！")
    # 回滚 放弃本次所有改动 相当于啥也没干
    conn.rollback() # 出错了就回滚，不保存结果




# 5.关闭游标--关闭数据库
cur.close()
# 6.关闭连接
conn.close()





