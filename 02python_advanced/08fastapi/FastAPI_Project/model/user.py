from utils.mysql_config import Base,engine
from sqlalchemy import Column, String, Integer, func, TIMESTAMP, text
class UserModel(Base):
    # 表名
    __tablename__ = 'UserModel'
    id = Column(Integer,primary_key=True,autoincrement=True)
    userName = Column(String(20),nullable=False,unique=True,comment="用户名")
    age = Column(Integer,nullable=False)
    role_id = Column(Integer,nullable=False,default=1,comment="角色id")
    create_time = Column(TIMESTAMP, server_default=func.now(), comment="创建时间")
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),comment="修改时间")

    def to_dict(self):
        return {
            "id":self.id,
            "userName":self.userName,
            "age":self.age,
            "role_id":self.role_id
        }
Base.metadata.create_all(engine)
print("执行成功_2!")