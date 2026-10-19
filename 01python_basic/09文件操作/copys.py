# 封装成一个函数，封装拷贝的代码
"""
x：你要拷贝的文件
y：拷贝之后的文件
"""
# 打开一个原文件
def file_copy(x:str = "utils/copyold.txt", y:str = "utils/copynew.txt"):
    with open(file=x, mode="rb") as pictureOld:
        # 创建一个新图片（写二进制）
        with open(y, "wb") as pictureNew:
            data = pictureOld.read(512)
            while data:  # 如果data取不到内容，也就是data为空，就无法进入while循环
                # 把读取到的内容写入新文件中
                pictureNew.write(data)
                # 继续读取512字节
                data = pictureOld.read(512)
            print("文件拷贝成功！")

# 说明当前模块被直接运行，那么去执行以下代码
if __name__ == "__main__":
    file_copy()


