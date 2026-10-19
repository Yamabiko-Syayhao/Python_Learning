"""
设计三张表
学生表 学生基本信息 id name sex age class_name 创建时间 修改时间    20
课程表 课程信息 id course_name teacher 创建时间 修改时间           9
成绩表 id 学生id 课程id 成绩 创建时间 修改时间                      180
"""
from pymysql import cursors

# 1.导入pymysql包 uv add pymysql

from utilsmysql import *

# 4.建表

# def createtable():
#     # 学生表
#     sql1 = """CREATE TABLE students
#               (
#                   id         INT PRIMARY KEY AUTO_INCREMENT comment "学生编号",
#                   name       VARCHAR(50) NOT NULL COMMENT "学生姓名",
#                   sex        CHAR(1) COMMENT "性别",
#                   age        INT COMMENT "年龄",
#                   class_id   INT COMMENT "班级",
#                   created_at datetime default NOW() COMMENT "创建时间",
#                   updated_at datetime default NOW() on update current_timestamp COMMENT "修改时间",
#               -- 普通索引
#               INDEX idx_name(name)
#               )
#            """
#
#     # 课程表
#     sql2 = """CREATE TABLE courses
#               (
#                   id           INT PRIMARY KEY AUTO_INCREMENT COMMENT "课程编号",
#                   name         VARCHAR(50) NOT NULL COMMENT "课程名",
#                   teacher      VARCHAR(10) COMMENT "老师",
#                   created_time datetime default NOW() COMMENT "创建时间",
#                   updated_time datetime default NOW() COMMENT "修改时间"
#               )
#            """
#
#     # 成绩表
#     sql3="""CREATE TABLE scores
#            (
#                id           INT PRIMARY KEY AUTO_INCREMENT COMMENT "成绩编号",
#                student_id    INT NOT NULL COMMENT "学生id",
#                course_id    INT NOT NULL COMMENT "课程id",
#                score        INT COMMENT "成绩",
#                created_time datetime default NOW() COMMENT "创建时间",
#                updated_time datetime default NOW() COMMENT "修改时间",
#                INDEX        idx_stu_course(course_id,student_id)
#            )
#         """
#
#     # 调用外部的方法
#     insert_data(sql1)
#     insert_data(sql2)
#     insert_data(sql3)
#
#
#
# if __name__ == "__main__":
#     createtable()
#       print("建立表格成功！")


# ai创建
# 用faker造测试数据 需要先安装 uv add faker
# from faker import Faker
#
# # 指定中文环境 这样生成的名字是中国人姓名
# fake = Faker("zh_CN")
#
# def addtestdata():
#     # ===== 学生表 20条 =====
#     students = []
#     for i in range(20):
#         name = fake.name()                        # 随机姓名
#         sex = fake.random_element(elements=("男", "女"))  # 随机性别
#         age = fake.random_int(min=15, max=18)     # 随机年龄 15-18
#         class_id = fake.random_int(min=1, max=6)  # 随机班级 1-6
#         students.append((name, sex, age, class_id))  # 一个元组就是一行数据
#     # 第二个参数就是utilsmysql里的query:传列表走executemany批量插入 传None(建表时)走execute只执行一次
#     insert_data("insert into students(name,sex,age,class_id) values(%s,%s,%s,%s)", students)
#
#     # ===== 课程表 9条 =====
#
#     # 课程名用固定列表更真实 老师姓名用faker随机生成
#     course_names = ["语文", "数学", "英语", "物理", "化学", "生物", "政治", "历史", "地理"]
#     courses = []
#     for cname in course_names:
#         teacher = fake.name()
#         courses.append((cname, teacher))
#     insert_data("insert into courses(name,teacher) values(%s,%s)", courses)
#
#     # ===== 成绩表 180条 = 20个学生 x 9门课 =====
#     # 前提:表是新建的 学生id是1-20 课程id是1-9
#     # 如果重复运行过 学生/课程会越插越多 id就不是这个范围了
#     scores = []
#     for stu_id in range(1, 21):               # 学生id 1~20
#         for cou_id in range(1, 10):           # 课程id 1~9
#             score = fake.random_int(min=0, max=100)  # 随机成绩 0-100
#             scores.append((stu_id, cou_id, score))
#     insert_data("insert into scores(student_id,course_id,score) values(%s,%s,%s)", scores)
#
#
# if __name__ == "__main__":
#     # 表已经建过了 每次运行都会重复插一套数据 想只插一次跑一次就行
#     addtestdata()
#     print("插入所有数据成功！")

# 老师创建
from faker import Faker
fake = Faker(locale='zh_CN')
def initStudent(num=20):
    # 为了存放 造假好的学生信息
    data_list = []
    for i in range(num):
        obj = (
            fake.name(),
            fake.random_element(elements=("男","女")),
            fake.random_int(12,40),
            fake.random_int(1, 5),
        )
        data_list.append(obj)
    # 写sql语句然后填充数据
    # 因为只有四列数据，所以必须在student后面固定要填充的字段
    # insert_data必须在循环外 只造好数据后批量插一次
    sql = "insert into students(name,sex,age,class_id) values(%s,%s,%s,%s)"
    res = insert_data(sql,data_list)
    print(f"添加了{res}条")

def initCourse(num=20):
    data_list = [
        ("语文","刘老师"),
        ("数学","李老师"),
        ("英语","五老师"),
        ("python","藤老师"),
        ("化学","岳老师"),
        ("生物","王老师"),
        ("历史","张老师"),
    ]
    sql = "insert into courses(name,teacher) values(%s,%s)"
    # 只调用一次 之前的第二次重复调用会把课程表数据翻倍
    res = insert_data(sql, data_list)
    print(f"添加了{res}条")

def initScore():
    data_list = []
    # 学生id从1开始(对应students表的真实id) 课程id从1到7(对应courses表的7门课)
    for i in range(1, 21):
        for j in range(1, 8):
            # 动态生成成绩
            grade = fake.random_int(0,100)
            tuple1 = (i,j,grade)
            data_list.append(tuple1)
    # insert_data必须在循环外 一次性批量插入 循环里每次会重复插整个列表
    sql = "insert into scores(student_id,course_id,score) values(%s,%s,%s)"
    res = insert_data(sql,data_list)
    print(f"添加了{res}条")

if __name__ == '__main__':
    # initStudent()
    # initCourse()
    initScore()