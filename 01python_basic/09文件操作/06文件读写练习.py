"""
需求：
    将用户的输入内容写入到文件中，并且将文件中的数据读出来



"""
import time

while True:
    data = input("请输入内容：")
    # 输入q就终止循环
    if data == "q":
        break
# 将输入的内容写道文件里面 追加
    with open("utils/practice.txt", "a+", encoding = "utf-8") as f:
        f.write(f"{data}\n")
        print("写入成功")


    print("现在内容正在读取中，请稍后")
    time.sleep(2)

    # 读取内容
    with open("utils/practice.txt", "r", encoding = "utf-8") as f:
        print(f"读取内容是：\n{f.read()}")




