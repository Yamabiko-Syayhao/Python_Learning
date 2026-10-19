from sqlalchemy import create_engine,Column,text
from sqlalchemy.orm import sessionmaker
# ================ 1.数据库连接 ================
# 格式 mysql + pymysql://用户名:密码@地址:端口号/数据库名称?charset=uft8
# 数据库一定要存在
engine = create_engine('mysql+pymysql://root:352130789Slh@localhost:3306/test?charset=utf8')
# ================ 2.创建会话工厂 ================
sess = sessionmaker(bind=engine)
# ================ 3.创建会话 ================
session = sess()
# sad = sess()
# ================ 4.执行sql ================
try:
    conn = engine.connect()
    print("连接成功")
    conn.close()
except Exception as e:
    print("连接失败",e)

# 查询 stu表中的所有的数据
# 方法一 直接写sql语句 text把原生的sql包装成SQLAlchemy能识别的对象
sql = text("select * from stu")
# 执行sql语句获取查询结果
result = session.execute(sql)
print(result.fetchall(),"所有结果")



# ================ 5.提交事务 ================
# 如果在执行新增，修改，删除操作，必须提交事务才能生效
# 仅查询 可以不用提交
# session.commit()
# ================ 6.关闭会话 ================
session.close()



