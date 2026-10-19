# 第三方模块：别人开发好 发布到平台上的包
# 需要先安装第三方 库/模块


"""
    uv add 模块名
    下载速度可能会慢一些，可以切换镜像源
    清华：https://pypi.tuna.tsinghua.edu.cn/simple/
    阿里：https://mirrors.aliyun.com/pypi/simple/
    中科大：https://pypi.mirrors.ustc.edu.cn/simple/
    uv add 模块名 --default-index 镜像源的网址
"""
# 1.引入第三方模块/库
# 2.引入第三方模块 faker是一个专门用来生成“假数据”的第三方库
# 当你需要测试、填充数据
from faker import Faker
FAKER = Faker("zh_tw")
print(FAKER.name())
print(FAKER.address())
print(FAKER.city())
print(FAKER.company())
print(FAKER.phone_number())







