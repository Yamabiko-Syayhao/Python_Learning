"""
拷贝的逻辑：
    1.打开原图片
    2.创建新图片
    3.循环：每次读取512个字节，读完之后写入新文件。当读取到文件末尾，循环结束
    4.with关键字 自动关闭文件
"""
# # 打开一个原图（读二进制）
# with open(file = "utils/06格式化输出.png", mode = "rb") as pictureOld:
#     # 创建一个新图片（写二进制） 加b是读取二进制
#     with open("utils/06格式化输出copy.png", "wb") as pictureNew:
#         data = pictureOld.read(512)
#         while data: # 如果data取不到内容，也就是data为空，就无法进入while循环
#             # 把读取到的内容写入新文件中
#             pictureNew.write(data)
#             # 继续读取512字节
#             data = pictureOld.read(512)
#         print("文件拷贝成功！")

# 引入自定义模块
# import copys
# # 如果什么参数都不写，就是使用函数的默认值
# copys.file_copy("utils/practice.txt", "utils/practiceNew.txt")

# shutil
import shutil
# shutil.copy("源文件路径","目标路径") 会拷贝源文件到目标路径
# shutil.copy("utils/06格式化输出.png", "utils/06格式化输出_1.png")

# 目标拷贝路径如果是个文件夹，那么要拷贝的文件会被拷贝到这个文件夹中 被拷贝后的文件名不变
shutil.copy("utils/06格式化输出.png", "copyimg/")

# copy2 不仅会把文件单纯拷贝，还会把文件的信息属性全部拷贝过来，还带着修改时间
shutil.copy2("utils/06格式化输出.png", "utils/06格式化输出_2.png")

# 这个方法目标路径必须是完整文件名 不能只写一个文件夹
shutil.copyfile("utils/06格式化输出.png", "utils/06格式化输出_03.png")



