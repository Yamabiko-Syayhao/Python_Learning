# 导入python-pptx库 uv add python-pptx
from pptx import Presentation


def get_tables():
    prst = Presentation('../../dataset/苦糖果.pptx')
    # 遍历 ppt 中的每一页幻灯片
    for index, slide in enumerate(prst.slides, start=1):
        for shape in slide.shapes:
            # 判断是否有表格
            if shape.has_table:
                table = shape.table
                # 定义空列表 用于存储表格的数据
                table_data = []
                # 遍历表格当中的所有行
                for row in table.rows:
                    # 空列表
                    row_data = []
                    # 遍历行当中的所有单元格
                    for cell in row.cells:
                        # 获取到单元格的内容 添加到行中
                        row_data.append(cell.text)
                    # 将行的内容添加到表格数据中
                    table_data.append(row_data)
                print(table_data)



get_tables()
