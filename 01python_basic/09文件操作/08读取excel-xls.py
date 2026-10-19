"""
excel表格：.xls/.xlsx
.xls 是2003年之前的老格式
.xlsx 是2007年之后的新格式

第三方模块 需要先下载
xlrd 只读   2.0.1+
xlwt 写入
xlutils 读 修改 保存
 c
uv add xlrd
"""

# 引入第三方库
import xlrd
# 读取excel文件 工作薄对象
wb = xlrd.open_workbook("utils/老版本学生成绩.xls")
# 获取所有sheet
print(wb.sheet_names())

# 获取指定名称的sheet
sheet1 = wb.sheet_by_name("python基础")
print(sheet1)

# 获取指定名称的sheet表
sheet2 = wb.sheet_by_index(1)
print(sheet2)

# print(sheet1.nrows) # 打印行的数量
# print(sheet1.ncols) # 打印列的数量

# 获取第一行数据
# print(sheet1.row_values(0))

# 获取第一列数据
# print(sheet1.col_values(0))

# 获取指定行和列的数据
# sheet1.row_slice(行索引，从第几列开始，截取到哪一列) （左右截取）
print(sheet1.row_slice(1, 2, 4), "12")
# 以上会从下标为1的行，也就是第二行，然后从这一行的第三列（下标为2）开始往后截取到第五列
# （下标为4）不包括第五列本身

# sheet1.col_slice(列索引，从第几行开始，截取到哪一行) （上下截取）
print(sheet1.col_slice(1, 2, 4))



# 获取某个单元格的内容、
# 获取了第一行第三个单元格的数据
print(sheet1.row_values(0)[2])
print(sheet1.cell(0, 2).value)

# 获取第二行第一列的单元格内容
print(sheet1.cell(1, 0).value)

print("=="*30)

# 需求 遍历所有的单元格 把他们全部打印出来
for i in range(0, sheet1.nrows):
    for j in range(0, sheet1.ncols):
        print(sheet1.cell(i, j).value, end=" ")
    print("")