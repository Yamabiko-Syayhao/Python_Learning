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
# 用户输入账户密码
userName = input("输入用户名：")
passWord = input("输入密码：")
# 编写sql语句
# 就像"写张纸条给管理员"：帮我找 userName 是 xxx、passWord 是 xxx 的人
# 用 %s 占位而不是直接拼字符串，就像"填表格的空格"：
#   表格上印好"我叫＿＿，今年＿＿岁"，你再把答案填进去。
#   如果直接把内容拼进去，坏人可能输入一段"假命令"骗过管理员，偷走所有书（SQL注入）。
#   用 %s 填格子，管理员会先看清楚这是"名字"不是"命令"，安全。
sql = "select * from test where userName=%s and passWord=%s"
params = (userName, passWord)
# 将用户输入的账号和密码  通过execute联系在一起
# 就像"把纸条递给管理员"，管理员翻完书架后只告诉你"找到了几本"
# execute() 的返回值是受影响的行数，不是查询到的具体的数据行
#   （只告诉你数量，不会把书的内容直接递给你）
row = cur.execute(sql,params)


if row != 0:
    print("成功！")
else:
    print("失败！")
# 5.关闭游标--关闭数据库
# 就像"跟管理员说：我拿好了，你可以下班了"
cur.close()
# 6.关闭连接
# 就像"走出图书馆大门"：不还书、不关灯就走，图书馆会乱；
#   连接不关会把位置占满，别人就进不来了
conn.close()





