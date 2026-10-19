from openpyxl.styles.builtins import total
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
# 根据年龄排序 order_by根据某个字段进行排序 asc正序 小到大    desc倒序 大到小
# .offset(0).limit(3)  跳过（偏移）0条 拿3条数据
# data = session.query(TestModel).order_by(TestModel.age.asc()).offset(0).limit(3).all()
# dict_list = [item.to_dict() for item in data]
# for i in dict_list:
#     print(i,"列表数据")


page = int(input("请输入页码数")) # 页码数 第几页数据
page_size = int(input("请输入每页展示多少条")) # 每页的条目个数 每页几条数据
# 构建基础查询
query = session.query(TestModel)
# 分页查询--动态计算
test_list = query.offset((page-1)*page_size).limit(page_size)
data_list = [item.to_dict() for item in test_list]
print(f"当前页：{page}")
print(f"每页条数：{page_size}")
print(f"第{page}页面的数据是：")
for i in data_list:
    print(f"{i}")

total = query.count()
print(f"当前页面总条数是{total}")



# ================ 4.表不存在创建 ================
if __name__ == '__main__':
    # 根据提供的字段自动创建表格
    Base.metadata.create_all(engine)
    print("执行成功！")