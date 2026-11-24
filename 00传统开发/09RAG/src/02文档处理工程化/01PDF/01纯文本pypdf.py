# 基础文本解析工具 uv add pypdf pdfplumber pymupdf
# pypdf 适合进行 PDF 的基础操作 如合并 拆分 简单的文字提取
# pdfplumber 更适合处理复杂的表格数据提取，或者是需要获取字符坐标信息的场景
# pymupdf 通常作为默认的首选 速度快精度高，适合常规文本提取和图像处理

# ================ 提取纯文本的方式一 pypdf ================

# PdfReader 是 pypdf 提供的读取 PDF 文件的核心类
from pypdf import PdfReader

def parse_pdf_pypdf():
    reader = PdfReader(r"../../dataset/内科学知识库.pdf")
    # pdf 文件的总页数
    print(len(reader.pages),"总页数")
    text = []
    # 遍历循环每一页的内容
    for page in reader.pages:
        # 提取当前页的文本
        text.append(page.extract_text())
    # 将列表转为字符串
    text_str = "\n".join(text)
    # print(text_str[:300])

# 调用函数
parse_pdf_pypdf()