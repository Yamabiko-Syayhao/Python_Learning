from docx import Document

def get_tables(path):
    doc = Document(path)
    # doc.tables 获取文档当中的所有表格
    for index, table in enumerate(doc.tables, start=1):
        print(f"第{index}个表格")
        # 定义空列表 用于存储表格的数据
        table_data = []
        # 遍历表格当中的所有行
        for row in table.rows:
            row_data = []
            # 遍历行当中的所有单元格
            for cell in row.cells:
                # 获取到单元格的内容 添加到行中
                row_data.append(cell.text)
            # 将行的内容添加到表格数据中
            table_data.append(row_data)
        print(table_data)

get_tables("../../dataset/DOCX素材.docx")