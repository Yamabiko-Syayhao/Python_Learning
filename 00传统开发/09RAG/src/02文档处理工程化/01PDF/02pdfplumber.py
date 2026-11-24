# ================ 提取纯文本的方式二 pdfplumber ================
import pdfplumber

def parse_pdf_pdfplumber():
    text = []

    with pdfplumber.open("../../dataset/内科学知识库.pdf") as pdf:
        print(len(pdf.pages),"页码")
        #
        for page in pdf.pages:
            # 提取当前页的文本
            text.append(page.extract_text())
    # 将列表转为字符串
    text_str = "\n".join(text)
    print(text_str[:300])

# 调用函数
parse_pdf_pdfplumber()