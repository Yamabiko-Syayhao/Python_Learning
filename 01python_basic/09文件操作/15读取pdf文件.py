# pdfplumber
from email.mime import text

import pdfplumber

def fs(file_path):
    text = ""
    # 通过pdfplumber打开pdf文件
    with pdfplumber.open(file_path) as pdf:
        # 循环去遍历每一页pdf文件
        for page in pdf.pages:
            # 提取当前页的文本
            page_text = page.extract_text()

            # 如果有内容就将内容追加拼接到text变量上
            if page_text:
                text += page_text

        # 返回结果
        return text

result = fs("utils/cs.pdf")
print(f"你取到的pdf内容是：{result}")











