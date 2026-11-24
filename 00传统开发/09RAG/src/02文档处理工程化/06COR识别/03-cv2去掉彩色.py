# 图像预处理（提升 OCR 准确率的关键）
"""
    OCR 准确率 = 60% 看预处理，40% 看模型。
    企业实践：先把图片处理"干净"，再喂给 OCR。
"""
# OCR 引擎只关心黑白，去掉颜色后可以减少颜色的计算干扰
# 导入cv2库
import cv2
def preprocess(image_path):
    # 读取图片
    img = cv2.imread(image_path)
    # 1. 转灰度图,去掉彩色 黑白灰
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 2. 自适应二值化（黑白分明，文字更清晰 也就是去掉了灰色）自动适配图片明暗不均的情况
    binary = cv2.adaptiveThreshold(
        gray,  # 输入：灰度图
        255,  # 大于阈值的像素设置为255（白色）
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # 高斯加权计算局部区域阈值，抗光影效果更好
        cv2.THRESH_BINARY,  # 二值模式：超过阈值变白，低于阈值变黑
        15,  # 块大小：15×15像素为一个局部窗口，单独计算阈值，必须是奇数
        10  # 常数C：从局部计算出的阈值减去这个值，用来微调明暗
    )
    # 3. 去掉杂质，保留文字,越小越清晰
    denoised = cv2.medianBlur(binary, 1) # 必须是大于1的基数
    return denoised
# 调用预处理函数,目标图片
processed = preprocess("./docs/1.png")
# 保存处理后的图片
cv2.imwrite("./docs/1-1.png", processed)