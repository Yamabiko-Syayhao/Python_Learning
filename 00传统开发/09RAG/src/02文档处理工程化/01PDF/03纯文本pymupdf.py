# ================ 提取纯文本的方式三 pymupdf ================
import pymupdf
# import fitz 这种引入其实就是引入 pymupdf
def parse_pdf_pymupdf():
    # 打开pdf文档

    text = []
    pdf = pymupdf.open("../../dataset/内科学知识库.pdf")
    print(len(pdf),"页码")

    for page in pdf:
        # 提取当前页的文本 添加到列表当中
        text.append(page.get_text())
    # 将列表转为字符串
    text_str = "\n".join(text)
    print(text_str[:300])

# 调用函数
parse_pdf_pymupdf()