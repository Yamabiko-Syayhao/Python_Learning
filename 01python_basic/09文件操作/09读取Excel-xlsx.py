"""
openpyxl 是现代处理Excel(.xlsx)的主流python库 是xlrd/xlwt/xlutils
同时支持 读取 修改 和写入，并且格式兼容性更好

uv add openpyxl
"""

# 引入
import openpyxl
# 打开文件
wb = openpyxl.load_workbook("utils/新版本成绩.xlsx")
# 获取所有sheet
print(wb.sheetnames)
# 获取指定sheet
print(wb.sheetnames[0]) # 单纯打印名字
print(wb["python基础"]) # 打印这个表格
sheet = wb["python基础"]
print(sheet)

# 获取行和列
print(sheet.max_row)
print(sheet.max_column)

# 获取指定的单元格的数据
print(sheet.cell(2, 2).value)
print(sheet["B2"].value)



