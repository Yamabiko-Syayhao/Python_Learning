# PDF ---> 图片 OCR识别 ---> 纯文本
import os
# 下面这些是 paddle 这个框架的经典保命操作
# 是关闭 paddleOCR 中的 OneDNN 加速
# 关闭目的：防止老一点的电脑或者程序崩溃
os.environ["FLAGS_enable_pir_api"] = "0"
os.environ["FLAGS_use_onednn"] = "0"
os.environ['FLAGS_use_mkldnn'] = '0'
os.environ['ONEDNN_VERBOSE'] = '0'
os.environ['PADDLEOCR_DOWNLOAD_TIMEOUT'] = '3000'  # 5分钟
# pdf2image
from pdf2image import convert_from_path
# paddleocr 专门做文字识别的
from paddleocr import PaddleOCR

def pdf_ocr():
    os.makedirs('../../dataset/orc', exist_ok=True)
    # 初始化一个 ocr 模型 ocr 模型是经过大量文字图片训练的模型
    # use_textline_orientation=True 自动矫正倾斜文字角度 双保险修复奔溃
    ocr = PaddleOCR(
        lang="ch",
        device="cpu",
        use_textline_orientation=False,
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        enable_mkldnn=False
    )
    # 本身不包含 pdf 解析器 它依赖于外部的 Poppler 工具 这个工具专门把 pdf 的每一页转为图片
    imgs = convert_from_path('../../dataset/内科学知识库.pdf', poppler_path="../../poppler-26.02.0/Library/bin")

    for index, img in enumerate(imgs, start=1):
        imgPath = f'../../dataset/orc/{index}.png'
        img.save(imgPath)
        result = ocr.predict(imgPath)
        page_text = ""
        if result:
            try:
                text_list = result[0]['rec_texts']
                page_text = "\n".join(text_list)
            except (KeyError, TypeError):
                text_list = getattr(result[0], 'rec_texts', [])
                page_text = "\n".join(text_list)

        print(f"【第{index}页纯文本】\n{page_text}")

pdf_ocr()