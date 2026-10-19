"""try:

with不能当成变量名，是py中的一个关键字用于处理文件操作
它的核心作用：自动管理资源Z（创建-用完-自动关闭）
代码结束之后会自动释放资源，不用手动写close()

with open("文件.格式". "mode模式", encoding = "utf-8") as 变量名:
    使用变量读取内容写自己的逻辑

"""

# 假设要使用with，上边的代码就可以简化成
#     with open("utils/wenben.txt", "r") as f:
#         print(f.read()) # read()读取
# except Exception as e:
#     print("读取失败了！", e)

# 读取文件---自动关闭释放资源
with open(file = "utils/wenben.txt", mode = "r", encoding = "utf-8") as f:
    print(f"读取的内容是{f.read()}")
    print("==== 文件自动关闭，资源主动释放 ====")

# 写入文件
# w 如果有文件 就覆盖原本文件之前有的内容 没有会自动创建一个新文件
# a+ 追加 无限在末尾追加内容
with open(file = "utils/233.txt", mode = "w", encoding = "utf-8") as f:
    f.write("hello no net\n")
    f.write("惨！\n")

