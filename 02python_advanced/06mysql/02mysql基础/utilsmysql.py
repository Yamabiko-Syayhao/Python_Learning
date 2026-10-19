# 基于DBUtils 连接池 的 mysql 操作封装模块 目的是让数据库操作更高效 更简洁
# DBUtils 核心作用是管理数据库的连接，让程序更高效的安全的去复用连接，而不是每
# 次操作都重新建立和关闭连接
# DBUtils 需要uv add DBUtils
# 当你的程序需要频繁访问数据库的时候，反复执行步骤 建立连接-->执行操作-->断开连接，
# 会带来不小的开销
import pymysql
from  dbutils.pooled_db import PooledDB
pool = PooledDB(
    creator=pymysql, # 底层驱动
    maxconnections=6, # 最大连接数
    mincached=2, # 启动时先建两个空闲连接 初始化的时候最小空闲连接数
    maxcached=5,  # 最多保留5个闲着的
    host='127.0.0.1',
    port=3306, # 端口号
    user='root',
    password='352130789Slh',
    database='test',
    blocking=True, # True作用是连接池满的时候阻塞等待 不报错
    charset='utf8mb4', # 字符编码
    cursorclass=pymysql.cursors.DictCursor # 设置游标字典格式
)
# 连接数据库
def connect():
    # 取出链接
    conn = pool.connection() # 从池子里面借一个连接
    cursor = conn.cursor() # 创建游标（数据库）
    return conn, cursor
# 关闭 对于pooleddb来说 conn.close() 不是真正的断开 而是把连接归还到池子里面供复用
# 所以在这 仅仅是 归还
def close_conn(conn, cursor):
    cursor.close() # 关闭游标
    conn.close() # 关闭连接

# 增/修改 数据
def insert_data(sql,query=None):
    # 为啥要预设 因为finally会判断他俩有没有值 防止还没链接成功就报错
    conn, cursor = None, None # 两个值的预设
    try:
        conn, cursor = connect()
        # 判断传进来的数据query是不是个列表
        if isinstance(query,list):
            cursor.executemany(sql,query)
        else:
            cursor.execute(sql,query)
        conn.commit()
        close_conn(conn, cursor)
        return cursor.rowcount # 影响力多少行数据
    except Exception as e:
        if conn:
            conn.rollback()
        print(e,"失败信息")
    finally: # 一定执行
        # 无论成功还是失败都要执行finally
        # 两个都有值 才能证明创建成功 才关
        if conn and cursor:
            close_conn(conn, cursor)

# 查询数据
def fetch_data(sql,query=None):
    conn, cursor = connect()
    cursor.execute(sql,query)
    result = cursor.fetchall()
    # for i in result:
    #     print(i)
    # print("查询成功！")
    close_conn(conn, cursor)
    return result



