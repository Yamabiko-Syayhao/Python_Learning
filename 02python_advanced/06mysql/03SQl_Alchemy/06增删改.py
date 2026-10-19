from openpyxl.styles.builtins import total
from sqlalchemy import create_engine, Column, String, Integer, func, TIMESTAMP, text, and_, or_, null, except_all
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
# =============== 新增 ===============
def text_add():
    # 要新增的数据
    new_stu = TestModel(userName="白承飞",passWord="123123",age=36)
    # 将它添加到会话当中存储起来
    session.add(new_stu)
    session.commit()
    print("新增成功")
# text_add()

# =============== 修改 ===============
def text_update():
    try:
        # 查询要修改的数据----查询
        update_stu = session.query(TestModel).filter_by(age=40).first()
        # 如果数据存在就修改
        if update_stu:
            update_stu.passWord = "wwwwww385"
            update_stu.age = 40
            session.commit()
            print("修改成功")
    except Exception as e:
        print("修改失败",e)
# text_update()

# =============== 删除 ===============
def text_delete():
    try:
        # 查询要删除的数据----查询
        delete_stu = session.query(TestModel).filter_by(userName="白承飞").first()
        # 如果数据存在就修改
        if delete_stu:
            session.delete(delete_stu)
            session.commit()
            print("删除成功！")
        else:
            print("根本没有这样的人")
    except Exception as e:
        session.rollback()
        print("修改失败",e)
# text_delete()
# =============== 批量新增 ===============
add_list = [
            TestModel(userName="viola",passWord="",age=16),
            TestModel(userName="sayo",passWord="",age=18),
            TestModel(userName="mhr",passWord="",age=16)
            ]
def text_add1():
    # 将它添加到会话中存储起来
    session.add_all(add_list) # 批量新增是add_all
    session.commit()
    print("批量新增成功")
# text_add1()
# =============== 批量删除 ===============
# delete_id = [9,10,11]
# def delete_all():
#     try:
#         delete_all_stu = session.query(TestModel).filter(TestModel.id.in_(delete_id)).all()
#         if delete_all_stu:
#             for stu in delete_all_stu:
#                 session.delete(stu)
#         session.commit()
#         print("删除成功！")
#     except Exception as e:
#         session.rollback()
#         print("删除失败",e)
# delete_all()

delete_id = [13,14,15]
def delete_all():
    try:
        count = session.query(TestModel).filter(TestModel.id.in_(delete_id)).count()
        if count == 0:
            print("未查询到该数据")
        else:
            # synchronize_session = False
            session.query(TestModel).filter(TestModel.id.in_(delete_id)).delete(synchronize_session = False)
            session.commit()
            print("删除成功")
    except Exception as e:
        session.rollback()
        print("程序出错",e)
delete_all()
# ================ 5.提交事务 ================
# 如果在执行新增，修改，删除操作，必须提交事务才能生效
# 仅查询 可以不用提交
# session.commit()
# ================ 6.关闭会话 ================
session.close()