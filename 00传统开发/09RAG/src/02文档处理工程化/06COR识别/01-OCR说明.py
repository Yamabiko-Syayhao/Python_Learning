"""
OCR 是企业 RAG 绕不过去的一道坎

为什么？因为企业里大量"扫描件"根本没有文本层：
    合同（盖章后扫描）
    发票、报销单
    营业执照、身份证
    银行流水、财务凭证
    历史档案（纸质扫描成 PDF）
    手写单据

这些文件本质就是"图片"，PyPDF / python-docx 一个字都提取不到。
必须靠 OCR（Optical Character Recognition，光学字符识别）把图片变成文字。

本节目标：
- OCR 的本质与流程
- Tesseract（老牌、通用）
- PaddleOCR（中文最强、企业首选）
- RapidOCR（轻量、无依赖、易部署）
- 扫描版 PDF → 图片 → OCR 全流程
- 表格 OCR / 版面分析
- 大模型 OCR（VLM，2026 新趋势）
- 企业级 OCR Pipeline

一、OCR 的本质
图片
↓
图像预处理（灰度/二值化/去噪/纠偏）
↓
文本检测（找出文字在哪）
↓
文本识别（认出是什么字）
↓
结构还原（按坐标拼成段落/表格）

二、企业 OCR 选型（先记结论）
    中文场景        → PaddleOCR（首选）
    英文/多语言      → Tesseract
    轻量化部署/边缘   → RapidOCR
    复杂版面/手写    → 大模型 VLM（Qwen-VL / GPT-4o）

三、安装依赖
    uv add paddlepaddle paddleocr
    uv add pytesseract pillow
    uv add rapidocr-onnxruntime
    uv add pdf2image
    # Tesseract 还需安装系统软件 + 中文语言包
    # macOS:  brew install tesseract tesseract-lang
    # Ubuntu: apt install tesseract-ocr tesseract-ocr-chi-sim
"""