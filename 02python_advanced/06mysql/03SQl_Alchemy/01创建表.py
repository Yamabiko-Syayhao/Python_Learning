"""
SQLAlchemy 操作mysql的一个框架 企业用的多一些
uv add sqlalchemy 如果下载失败可能是因为更新太快 下载最新版本可能会因为更新太快失败
可以用下载指定版本 如 uv add sqlalchemy==2.0.54
"""
# create_engine 创建数据库连接
from sqlalchemy import create_engine,Column,String,Integer,DateTime,func,TIMESTAMP,text
# 引入ORM基类 所有的数据表模型必须继承它
from sqlalchemy.orm import declarative_base
# ================ 1.数据库连接 ================
# 格式 mysql + pymysql://用户名:密码@地址:端口号/数据库名称?charset=uft8
# 数据库一定要存在
engine = create_engine('mysql+pymysql://root:352130789Slh@localhost:3306/test?charset=utf8')
# 如果密码里面有@特殊符号 用上边的写法会连接失败 那么就用下面的连接方法 这两个方法是等价的
"""url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="lhj@119898",  
    host="localhost",
    port=3306,
    database="test",
    query={"charset": "utf8"}
)
engine = create_engine(url)
"""

# ================ 2.ORM基类 ================
Base = declarative_base()
# ================ 3.创建表结果 ================
# 定义一个Stu类 继承Base
class Stu(Base):
    # 数据库的表名
    __tablename__ = 'stu'
    # 字段1 int类型 主键 自增
    id = Column(Integer,primary_key=True,autoincrement=True)
    # 字段2 字符串类型 长度不能超过20 不能为空（必填）  唯一
    userName = Column(String(20),nullable=False,unique=True)
    # 字段3 字符串类型 长度不能超过20 不能为空（必填）
    passWord = Column(String(20),nullable=False)
    # 字段4 int类型 默认值为0
    age = Column(Integer,server_default='0')
    # 字段5 时间日期类型 自动填充时间 注释
    create_time = Column(TIMESTAMP,server_default=func.now(),comment="创建时间")
    # 当你去修改数据的时候 自动填充时间
    update_time = Column(TIMESTAMP,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))



# ================ 4.表不存在创建 ================
if __name__ == '__main__':
    # 根据提供的字段自动创建表格
    Base.metadata.create_all(engine)
    print("执行成功！")










