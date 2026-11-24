import os

import pymupdf
import pdfplumber
from paddleocr import PaddleOCR
from pdf2image import convert_from_path

pdf_path = r'../../dataset/产品手册_v2.pdf'

# 只负责处理扫描件（把pdf文档转为图片）
class OCRPDFParser:
    def __init__(self, lang='ch'):
        self.ocr = PaddleOCR(
            lang=lang,
            use_textline_orientation=True, # 倾斜文字识别
            enable_mkldnn=False # 防止崩溃
        )

    def parse_pdf(self, pdf_path, save_temp=False):
        images = convert_from_path(pdf_path, poppler_path="../../poppler-26.02.0/Library/bin")
        # 定义一个列表存放将来识别出来的所有文本
        full_text = []
        for idx, image in enumerate(images, start=1):
            temp_img = f"temp_{idx}.png"
            image.save(temp_img)

            result = self.ocr.predict(temp_img)

            for line in result:
                for word in line['rec_texts']:
                    full_text.append(word)

            if not save_temp and os.path.exists(temp_img):
                os.remove(temp_img)

            return '\n'.join(full_text)

# 类似于路由中心 负责检测 pdf 的类型（扫描件?表格?图片?纯文本）
# 然后分发给对应的处理函数
class PDFProcessor:
    def __init__(self, lang='ch'):
        # 实例化了自己写的类
        self.ocr = OCRPDFParser(
            lang=lang
        )

    def is_scan_pdf(self, pdf_path, sample_pages=2):
        try:
            pdf = pymupdf.open(pdf_path)
            for i in range(min(sample_pages, len(pdf))):
                # 抽取当前页的文本
                text = pdf[i].get_text().strip()
                if len(text) > 50:
                    return False
            return True

        except Exception as e:
            print(e)
            return True
    # 判断 pdf 中是否包含表格
    def has_tables(self, pdf_path):
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    if page.extract_tables():
                        return True
            return False
        except Exception as e:
            print(e)
            # 如果上边的读取文件异常 就保守的判断为扫描件即可
            return False

    def has_images(self, pdf_path):
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    if page.extract_images():
                        return True
            return False
        except Exception as e:
            print(e)
            return False
    # 文本清洗
    def clean_text(self, text):
        # 文本按照换行分割 每行去掉前后空格
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return '\n'.join(lines)
    # 统一处理函数 根据不同类型匹配不同的处理方法
    def process(self, pdf_path):
        print(f"开始解析{pdf_path}")
        result = []

        if self.is_scan_pdf(pdf_path):
            print(f"启动扫描型pdf处理逻辑")
            result = self.ocr.parse_pdf(pdf_path)
        elif self.has_tables(pdf_path):
            print("启动表格解析逻辑")
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text().strip()
                    tables = page.extract_tables()
                    result.append(text)
                    result.append(str(tables))
                result = '\n'.join(result)
        elif self.has_images(pdf_path):
            print("此处可以复用pdf_img函数保存图片逻辑")
        else:
            print("开启纯文本解析逻辑")
            pdf = pymupdf.open(pdf_path)
            result = '\n'.join([page.get_text() for page in pdf])

        return self.clean_text(result)


if __name__ == '__main__':
    processor = PDFProcessor(lang='ch')
    result_text = processor.process(pdf_path)
    print("解析完成，提取文本=================")
    print(result_text)

    with open("pdf-res.md", 'w', encoding='utf-8') as f:
        f.write(result_text)

    print("结果已保存")