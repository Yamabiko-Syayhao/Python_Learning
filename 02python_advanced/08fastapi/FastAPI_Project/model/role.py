from utils.mysql_config import Base, engine
from sqlalchemy import Column, String, Integer, func, TIMESTAMP, text


class RoseModel(Base):
    # 表名
    __tablename__ = 'RoseModel'
    id = Column(Integer, primary_key=True, autoincrement=True)
    roleName = Column(String(20), nullable=False, comment="用户名")
    role = Column(String(20), nullable=False, default=0, comment="角色")
    create_time = Column(TIMESTAMP, server_default=func.now(), comment="创建时间")
    update_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),comment="修改时间")

    def to_dict(self):
        return {
            "id": self.id,
            "roleName": self.roleName,
            "role": self.role
        }

Base.metadata.create_all(engine)
print("执行成功_3!")