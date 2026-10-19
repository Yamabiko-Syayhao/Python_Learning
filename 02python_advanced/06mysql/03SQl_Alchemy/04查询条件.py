from sqlalchemy import create_engine,Column,String,Integer,func,TIMESTAMP,text,and_,or_
# 引入ORM基类 所有的数据表模型必须继承它
from sqlalchemy.orm import declarative_base,sessionmaker
# ================ 1.数据库连接 ================
# 格式 mysql + pymysql://用户名:密码@地址:端口号/数据库名称?charset=uft8
# 数据库一定要存在
engine = create_engine('mysql+pymysql://root:352130789Slh@localhost:3306/test?charset=utf8')
# ================ 2.创建会话工厂 ================
sess = sessionmaker(bind=engine)
# ================ 3.创建会话 ================
session = sess()
# ================ 4.ORM操作数据库 ================
# 4.1创建orm基类Base 所有的数据模型必须继承这个基类 这样才能被sqlalchemy管理
Base = declarative_base()
# 4.2 创建数据库模型必须继承Base
# 定义一个Stu类 继承Base
class TestModel(Base):
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

    # 定义一个工具方法 将orm对象改为字典格式 方便接口返回json数据
    def to_dict(self):
        return {
            "id":self.id,
            "userName":self.userName,
            "passWord":self.passWord,
            "age":self.age,
            "create_time":self.create_time,
            "update_time":self.update_time
        }
# 4.3 使用orm查询所有数据
# 4.3.1 按照条件查询 过滤 filter().all() 所有的数据 ----适合绝大多数复杂的查询
# 等价于 SELECT * FROM stu WHERE userName = "arl"
# test_list = session.query(TestModel).filter(TestModel.userName=="arl").all()
# test_list = session.query(TestModel).filter(TestModel.age>=16).all()
# dict_list = [item.to_dict() for item in test_list]
# print(dict_list,"列表数据")

# 4.3.2 按照条件查询 filter_by() 简单的相等的查询
# test_list = session.query(TestModel).filter_by(age=16).all()
# dict_list = [item.to_dict() for item in test_list]
# print(dict_list,"列表数据")

#4.3.3 按照条件查询 filter_by() 简单相等的查询 查第一条 所以即使目前表里面有两条符合要求的数据，也是
# 只出现第一条
# test_list = session.query(TestModel).filter_by(age=16).first()
# # 单个数据 单个对象
# dict_data = test_list.to_dict()
# print(dict_data)

# 4.3.4 多条件 and/or
# 并且
# test_list = session.query(TestModel).filter((TestModel.age > 12)&(TestModel.passWord==21312)).all()
# test_list = session.query(TestModel).filter(and_(TestModel.age > 12,TestModel.passWord==21312)).all()
# 或
# test_list = session.query(TestModel).filter((TestModel.age > 12)|(TestModel.passWord==21312)).all()
# test_list = session.query(TestModel).filter(or_(TestModel.age > 12,TestModel.passWord==21312)).all()

# 4.3.5 模糊查询
# 范围查询 id为1 2 4 7的内容
# in_ 是id下的 而上面的and_ or_是单独的方法
# test_list = session.query(TestModel).filter(TestModel.id.in_([1,3])).all() # 查询id为1和3的
# test_list = session.query(TestModel).filter(TestModel.id.between(2,4)).all() # 查询id在2到4之间的
test_list = session.query(TestModel).filter(TestModel.userName.like("%u%")).all() # 查询名字里面有"u"的



dict_list = [item.to_dict() for item in test_list]
for i in dict_list:
    print(i,"列表数据")


# ================ 4.表不存在创建 ================
if __name__ == '__main__':
    # 根据提供的字段自动创建表格
    Base.metadata.create_all(engine)
    print("执行成功！")


# ================ 5.提交事务 ================
# 如果在执行新增，修改，删除操作，必须提交事务才能生效
# 仅查询 可以不用提交
#   session.commit()
# ================ 6.关闭会话 ================
    session.close()