from utils.mysql_config import Base,engine
from sqlalchemy import Column, String, Integer, func, TIMESTAMP, text, and_, or_, null, except_all
class StuModel(Base):
    # 数据库的表名
    __tablename__ = 'StuModel'
    # 字段1 int类型 主键 自增
    id = Column(Integer,primary_key=True,autoincrement=True)
    # 字段2 字符串类型 长度不能超过20 不能为空（必填）
    userName = Column(String(20),nullable=False,comment="学生姓名")
    # 字段3-5 整数类型 不能为空（必填）
    english = Column(Integer,nullable=False,comment="英语成绩")
    python = Column(Integer,nullable=False,comment="python成绩")
    java = Column(Integer,nullable=False,comment="java成绩")
    # 字段6 时间日期类型 自动填充时间 注释
    create_time = Column(TIMESTAMP,server_default=func.now(),comment="创建时间")
    # 字段7 当你去修改数据的时候 自动填充时间
    update_time = Column(TIMESTAMP,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),comment="修改时间")

    # 定义一个工具方法 将orm对象改为字典格式 方便接口返回json数据
    def to_dict(self):
        return {
            "id":self.id,
            "userName":self.userName,
            "english":self.english,
            "python":self.python,
            "java":self.java,
            "create_time":self.create_time,
            "update_time":self.update_time
        }
# 根据提供的字段创建表 有表就不创建
Base.metadata.create_all(engine)
print("执行成功！")