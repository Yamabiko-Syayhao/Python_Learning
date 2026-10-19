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
# 4.指定sql语句
# 用户输入账户密码
userName = input("输入用户名：")
passWord = input("输入密码：")
# 编写sql语句 % 是字符串格式化 在python层面 把值拼接进字符串
# 拼接完毕之后sql已经是一条完整的sql字符串 参数被当成sql代码的一部分
# === 危险点就是这一行！用户输入会被原样拼进sql，当成sql代码执行 ===
sql = "select * from test where userName='%s' and passWord='%s'" % (userName, passWord)

# ------------------------------------------------------------------
# 下面演示什么是sql注入：在"用户名"里输入一段特殊字符，改变sql的原意
#
# 假设用户名输入： ' or 1=1 #   （# 是mysql的注释符，后面内容全部注释掉）
# 密码随便输，比如 xxx
#
# 拼接时会变成下面这样（输入的引号和注释符都被直接拼进去了）：
# sql = "select * from test where userName='' or 1=1 #' and passWord='xxx'"
#
# 在mysql里 # 后面是注释，所以真正执行的sql只剩：
# sql = "select * from test where userName='' or 1=1"
# 其中 1=1 永远成立，整个条件就永远成立，密码判断被注释掉了
# 结果：不管密码对不对，都能查出行 => 登录绕过成功，这就是sql注入
#
# 【小坑】也可以用 -- 当注释符，但mysql要求 -- 后面必须跟一个空格才算注释：
#   错误： ' or 1=1 --'   （-- 后面直接是引号，不构成注释，会报语法错误1064）
#   正确： ' or 1=1 -- '  （-- 后面有一个空格）
# 而输入框末尾的空格很容易被终端/粘贴吞掉，所以这里用 # 更省心
# ------------------------------------------------------------------

# 对比一下最初那个不严谨的例子（用户名输入 " or '1'='1 密码123456）：
# sql = "select * from test where userName='' or '1'='1' and passWord='123456'"
# and 的优先级高于 or，等价于：
# sql = 'select * from test where (userName="") or ("1"="1" and passWord="123456") '
# 因为 "'1'='1' and passWord='123456'" 还要求密码必须真是123456
# 所以这个例子其实绕不过登录，密码输错照样失败，演示不出注入效果
# 真正能绕过的是上面用 -- 把密码判断整段注释掉的那种写法

# params = (userName, passWord)
# 将用户输入的账号和密码  通过execute联系在一起
# execute() 的返回值是受影响的行数，不是查询到的具体的数据行
row = cur.execute(sql)
# 如果查到了行(row不等于0)，就当成登录成功
# 注意：这里用"查到的行数"判断登录，本身也不严谨，正常登录应该取出数据再校验
# 这里只是为了演示注入，才用行数判断
if row != 0:
    print("成功！")
else:
    print("失败！")
# 5.关闭游标--关闭数据库
cur.close()
# 6.关闭连接
conn.close()

# 不要用字符串拼接 防止sql注入，参数会被当成代码的一部分-->会被注入，危险

# 正确的做法（对照 01python操作mysql步骤.py）：
# 用 %s 占位符（注意这里不能自己用 % 去格式化），把值当成参数传给execute
#   sql = "select * from test where userName=%s and passWord=%s"
#   params = (userName, passWord)
#   row = cur.execute(sql, params)
# 这样 pymysql 会把用户输入当成"数据"处理，输入里的引号、-- 都不会被当成sql代码
# 也就注入不进去了




