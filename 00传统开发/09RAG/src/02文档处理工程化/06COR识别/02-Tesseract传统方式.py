"""
Tesseract：Google 维护的开源 OCR 引擎。
优点：免费、多语言、社区大。
缺点：中文/复杂版面效果一般，需要预处理。

下载地址： https://github.com/UB-Mannheim/tesseract/wiki
如果部分电脑安装exe程序一直失败，可以在课件中拿取压缩包 Tesseract-OCR.zip解压到D盘。
配置环境变量，在系统环境变量PATH中添加D:\Tesseract-OCR文件夹。
然后CMD中输入 tesseract -v 验证程序和变量配置的是否正确
最后重启pycharm后运行代码即可。
"""
# 你需要安装两类东西：Python 包和系统级的 Tesseract OCR 引擎（以及中文语言包）
# uv add pytesseract pillow
from PIL import Image
import pytesseract
# lang="chi_sim" 简体中文；"eng" 英文；可组合 "chi_sim+eng"
# 打开图片
image = Image.open("../../dataset/pdf_img/page15_img1.png")
# 识别图片
text = pytesseract.image_to_string(image, lang="chi_sim+eng") # 同时识别中英文
print("Tesseract 识别结果：\n", text)

