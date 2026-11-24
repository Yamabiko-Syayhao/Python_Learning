# 搭配huggingface
# 设置huggingface缓存目录
import os
"""
官网:https://huggingface.co/
国内镜像站:https://hf-mirror.com/
huggingface 是全球最大的模型和数据集共享平台  ,被称为AI界的Github
可以在上面找模型,下载权重,跑在线演示.分享自己的模型/数据
"""
# huggingface 是ai模型界的Github托管平台
# huggingface 本地缓存目录 模型缓存目录 下载的模型权重存在这里
os.environ['HF_HOME'] = f"./hf-cache"
# 国内镜像 更改下载源 解决国内直连 huggingface.co 慢/超时的问题
# os.environ["HF_ENDPOINT"] = r"https://hf-mirror.com"
# 改用这种方式设置国内镜像，最稳妥
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
# 设置下载超时时间 单位秒
os.environ['HF_HUB_DOWNLOAD_TIMEOUT'] = '30000'

# 上边的这些设置必须要在引入其他库之前设置

# unstructured 是一个文档解析库 每种格式都一个 partition_xxx 函数
from unstructured.partition.docx import partition_docx
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.ppt import partition_ppt
from unstructured.partition.pptx import partition_pptx

# 调用pdf解析函数
"""
strategy 解析策略 
    hi_res 高精度解析模式：版面分析 + 表格识别（需要下载模型，慢但是准确）
    fast  纯文本 快 不做版面分析 准确度低
    ocr_only 纯ocr 适合扫描件
"""
pdf_elements = partition_pdf(
    languages=['chi_sim'],
    filename="../../dataset/标题提取.pdf",#带解析的pdf路径
    strategy='hi_res',#使用高精度解析模式 需要下载模型，托管在 huggingface 里面
    # 所以最上面要配置好缓存目录 以及国内镜像
    infer_table_structure=True,#开启表格结构识别
)
# 遍历打印 pdf_elements(元素列表) 每个元素都是一个 Element 对象 (Title,Table,.....)
for pdf in pdf_elements:
    # 会调用元素的 __str__ 输出文本内容
    print(pdf)
    # 数据类型和本文内容
    print(pdf.category,pdf.text)
    # 结果不准确 超大号字体干扰 并且不居中  诗词排版等等  可以调整 更好的方式是直接用多模态大模型（VLM），效果是 100% 完美的。

# 注意：hi_res 会自动下载模型到 hf-cache 第一次跑会比较慢 所以前边需要设置镜像和超时
# word
# docx = partition_docx(filename="")
# 解析ppt
# ppt = partition_pptx(filename="")