# 导入pdf解析器  表格提取能力强
import pdfplumber

def parse_by_pdfplumber():
    # 定义了一个空列表 存放所有页面提取出来的表格
    table_list = []
    # 打开pdf文档  with自动释放资源
    with pdfplumber.open("../../dataset/内科学知识库.pdf") as pdf:
        # 遍历循环每一页的内容
        for page in pdf.pages:
            # 提取当前页面中的所有表格
            page_tables = page.extract_tables()
            # 如果当前页有数据
            if page_tables:
                # 循环将每个表格加入到表格列表中
                for table in page_tables:
                    table_list.append(table)
    # 判断整个pdf文档中 是否提取到了表格
    if table_list:
        print(f"总共解析到{len(table_list)}个表格\n")
        for table_idx,table_data in enumerate(table_list,start=1):
            print(f"============第{table_idx}个表格============")
            print(table_data)

# 调用函数
parse_by_pdfplumber()