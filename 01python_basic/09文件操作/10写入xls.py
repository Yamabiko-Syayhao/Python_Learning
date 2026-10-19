# 引入xlwt
import random

import xlwt

# 1.创建workbook对象
wb = xlwt.Workbook()
# 2.创建一个sheet对象
ws = wb.add_sheet("期末考试")

# 3.写入单元格的标题
# 假设是 姓名 语文 数学 英语
# ws.write(行，列，值)
# ws.write(0, 0, "姓名")
# ws.write(0, 1, "语文")
# ws.write(0, 2, "数学")
# ws.write(0, 3, "英语")
#
#
# # 保存数据
# wb.save("utils/学生期末成绩.xls")
# print("写入结束")

# 循环写入标题 第一行的标题
title = ["姓名", "语文", "数学", "英语"]
for i, v in enumerate(title):
    # 给第一行的 第0 1 2 3列加内容
    ws.write(0, i, v)

# 循环写入第一列的姓名
names = ["小田","小白","小盖","小岳","小 牛"]
for i, v in enumerate(names):
    # 给每一行的第一列写入姓名
    ws.write(i + 1, 0, v)
    # 按列循环三次 写入成绩
    for j in range(1, 4):
        # 给每一行的第2 3 4列写入成绩
        ws.write(i + 1, j, random.randint(0, 100))
# 保存数据
wb.save("utils/学生期末成绩.xls")
print("写入结束")
