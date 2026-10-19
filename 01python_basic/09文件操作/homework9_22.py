"""
练习1：读取刚才生成的11期末成绩.xlsx所有数据到字典中
返回的结果希望是如此[{'姓名': '小王', '语文': 34, '数学': 53, '英语': 12}, 。。。。]
"""
from openpyxl.styles.builtins import total

# 自己的一种想法
# import xlrd
#
# wb = xlrd.open_workbook("utils/老版本学生成绩.xls")
# sheet1 = wb.sheet_by_name("python基础")
# lis1 = sheet1.row_values(0)
# lis3 = []
# for i in range(1, sheet1.nrows):
#     lis2 =  sheet1.row_values(i)
#     dict1 = dict(zip(lis1, lis2))
#     lis3.append(dict1)
# print(lis3)

# 老师的例子
# from openpyxl import load_workbook
# wb = load_workbook("utils/学生期末成绩ww.xlsx")
# ws = wb["期末考试工作表"]
# print(ws,ws.max_row)
# # print(type(ws))
# print(ws[1])
# headers = [c.value for c in ws[1]]
# records = []
# # 为了从第二行开始遍历 跳过表头那一行
# # values_only = True 直接获取单元格的值
# for row in ws.iter_rows(min_row=2, values_only=True):
#     records.append(dict(zip(headers, row)))
#     # print(row)
# print(records)
# print(headers) # 打印第一行表头






"""
练习2：学生成绩统计，有两个.xls表
    students.xls表中包含的列：姓名、语文、数学、英语，计算每个人的总分跟平均分
    将结果输出到新的result.xls表中,并且根据总分降序排列,新的表中语数英分数依旧要有
"""
# import xlrd
# import xlwt
# # 先去实现读取
# wb = xlrd.open_workbook("utils/students.xls")
# sheet = wb.sheet_by_index(0)
# records = []
# for r in range(1,sheet.nrows):
#     # 每一行的数据
#     # print(sheet.row_values(r))
#     name,chinese,math,english,python = sheet.row_values(r)
#     total = chinese + math + english + python
#     avg = total / 4
#     records.append([name,chinese,math,english,python,total,avg])
# print(records)
#
# # 排序 按照总分降序
# records.sort(key=lambda x:x[5],reverse=True)
# print(records,"排序之后")
#
# # 写入
# out_wb = xlwt.Workbook()
# out_sheet = out_wb.add_sheet("成绩排序结果")
# headers = ["姓名","语文","数学","英语","python","总分","平均分"]
# for i,v in enumerate(headers): # 写入表头 即第一行
#     out_sheet.write(0,i,v)
# for r,row in enumerate(records):
#     for c,val in enumerate(row):
#         # 行 列 值
#         out_sheet.write(r+1,c,val)
# out_wb.save("utils/result.xls")
# print("处理完毕！")









"""
练习3：写一个 Python 程序，在 utils/ 目录下生成一个名为"学生期末成绩.xlsx"的 Excel 文件，
里面有一张名为"期末考试成绩"的工作表，表头为"序号、姓名、语文、数学、英语、政治、历史、体育"，
并为小张，小刘，小李，小盖，小田5 位学生随机生成 0~100 的各科成绩；
如果文件已存在，先询问用户是否覆盖，若用户选择覆盖则覆盖，若用户选择不覆盖，则直接取消保存

"""
# 我自己的思路
import openpyxl
import random
import os
wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = "期末考试工作表"
title = ["序号","姓名","语文","数学","英语","政治","历史","体育"]
for i,v in enumerate(title):
    sheet.cell(1,i+1,v)
names = ["小张","小刘","小李","小盖","小田"]
for i,v in enumerate(names):
    sheet.cell(i+2,2,v)
    sheet.cell(i+2,1,i+1)
    for j in range(1,7):
        sheet.cell(i+2,j+2,random.randint(0,101))
path = "utils/学生期末成绩ww.xlsx"
if os.path.exists(path):
    x = input("文件存在，是否覆盖文件？Y/N")
    if x == "Y":
        wb.save(path)
    else:
        print("保存已取消")
else:
    print("新建文件成功！")
print("写完！")
