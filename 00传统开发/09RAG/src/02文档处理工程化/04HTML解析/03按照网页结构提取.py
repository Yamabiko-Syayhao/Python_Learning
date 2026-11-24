from bs4 import BeautifulSoup
from htm import html

soup = BeautifulSoup(html, 'lxml')

# 获取所有 h 系列标签的内容
def get_h1_h6():
    # find_all() 获取所有标签的内容 里边可以是列表也可以是字符串
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        print(tag.get_text(strip=True))

def get_p():
    for tag in soup.find_all('p'):
        print(tag.get_text(strip=True))

def get_ul_li():
    for ul in soup.find_all('ul'):
        for li in ul.find_all('li'):
            print(li.get_text(strip=True))

def get_table():
    tableList = []
    table_html = """
    <table>
        <tr>
            <th>套餐</th>
            <th>价格</th>
            <th>并发</th>
        </tr>
        <tr>
            <td>基础版</td>
            <td>999/年</td>
            <td>100</td>
        </tr>
        <tr>
            <td>企业版</td>
            <td>9999/年</td>
            <td>不限</td>
        </tr>
    </table>
    """
    soup2 = BeautifulSoup(table_html, 'lxml')
    for table in soup2.find_all('table'): # table 表格
        for tr in table.find_all('tr'): # tr 行
            cells = tr.find_all(['td', 'th']) # td th 单元格      th 是表格内的表头 相比 td 来说自带加粗
            row_data = [cell.get_text(strip=True) for cell in cells]
            tableList.append(row_data)
    print(tableList)

get_table()
get_h1_h6()
get_p()
get_ul_li()