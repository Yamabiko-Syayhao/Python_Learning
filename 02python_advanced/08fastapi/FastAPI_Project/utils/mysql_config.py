from sqlalchemy import create_engine
# 引入ORM基类 所有的数据表模型必须继承它
from sqlalchemy.orm import declarative_base,sessionmaker
# ================ 数据库配置 ================
DB_USER = "root" # 用户名
DB_PASSWORD = "352130789Slh" # 密码
DB_HOST = "127.0.0.1" # 地址
DB_PORT = 3306 # 端口号
DB_NAME = "test" # 数据库
DB_CHARSET = "utf8" # 编码格式
DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"

# ================ 1.数据库连接 ================
# 格式 mysql + pymysql://用户名:密码@地址:端口号/数据库名称?charset=uft8
# 数据库一定要存在
engine = create_engine(DB_URL)
# ================ 2.创建会话工厂 ================
sess = sessionmaker(bind=engine)
# ================ 3.创建会话 ================
db = sess()
# orm操作对象 创建ORM
Base = declarative_base()

# 操作数据库提交事务




