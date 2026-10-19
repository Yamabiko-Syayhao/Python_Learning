from sqlalchemy import create_engine,Column,String,Integer,func,TIMESTAMP,text
# 引入ORM基类 所有的数据表模型必须继承它
from sqlalchemy.orm import declarative_base,sessionmaker
import json
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
# 等价于 原生的 select * from stu
test_list = session.query(TestModel).all()
#  转为字典列表
dict_list = [item.to_dict() for item in test_list]
# print(test_list)
# print(dict_list)

# 将列表的数据转为json字符串
# 如果列表数据当中存在时间对象，那么转换会报错 所以需要将时间对象转为字符串

json_str = json.dumps(dict_list,default=str,ensure_ascii=False) # ensure_ascii是处理编码用的，false后就能正确显示中文字符了
print(json_str,"json字符串",type(json_str))



# ================ 4.表不存在创建 ================
if __name__ == '__main__':
    # 根据提供的字段自动创建表格
    Base.metadata.create_all(engine)
    print("执行成功！")



