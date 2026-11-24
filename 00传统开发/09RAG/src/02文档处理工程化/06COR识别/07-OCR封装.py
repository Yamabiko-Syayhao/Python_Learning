# 企业级 OCR Pipeline
"""
输入文件
↓
类型判断（图片 / 扫描PDF）
↓
PDF → 图片
↓
图像预处理（灰度/二值化/纠偏）
↓
OCR 识别（PaddleOCR）
↓
按坐标还原阅读顺序
↓
清洗（去页眉页脚/水印噪音） # TODO::
↓
Chunk → Embedding → VectorDB
"""
from paddleocr import PaddleOCR
from pdf2image import convert_from_path

class OCRProcessor:
    """企业级 OCR 处理器"""
    def __init__(self, lang="ch"):
        # 初始化PaddleOCR实例
        self.ocr = PaddleOCR(use_angle_cls=True, lang=lang)

    def ocr_image(self, image_path):
        """单张图片 OCR 单张图片识别
        :param image_path: 图片路径
        :return: 识别文本
        """
        # 执行图片识别
        result = self.ocr.ocr(image_path)
        # 识别结果为空，返回空字符串
        page_text = ""
        # 检查结果是否为空
        if result and result[0]:
            # rec_texts 直接就是所有识别文字的列表
            text_list = result[0]['rec_texts']
            # 将列表转为字符串输出
            page_text = "\n".join(text_list)
        print(f"【纯文本】\n{page_text}")
        # 增加 return 返回结果
        return page_text

    def ocr_pdf(self, pdf_path, dpi=200):
        """扫描 PDF OCR
        :param pdf_path: pdf文件路径
        :param dpi: 图片分辨率
        :return: 全部页面文本
        """
        # 将PDF分页转为图片对象
        images = convert_from_path(pdf_path, dpi=dpi)
        # 保存每页OCR结果
        pages = []
        # 遍历每一页图片，i页码从1开始
        for i, image in enumerate(images, 1):
            # 设置临时图片路径
            tmp = f"/tmp/_ocr_page_{i}.jpg"
            # 保存图片
            image.save(tmp, "JPEG")
            # 调用图片OCR方法识别，存入列表
            pages.append(self.ocr_image(tmp))
        # 合并所有页面文本返回 每页之间空一行 方便区分

        return "\n\n".join(pages)

    def process(self, file_path):
        """统一入口：自动区分图片/PDF
        :param file_path: 文件路径
        :return: OCR识别后的完整文本
        """
        # 判断后缀是否为pdf
        if file_path.lower().endswith(".pdf"):
            return self.ocr_pdf(file_path)
        # 否则按图片处理
        return self.ocr_image(file_path)

if __name__ == "__main__":
    processor = OCRProcessor(lang="ch")
    text = processor.process("docs/1.png")
    print(text[:500])