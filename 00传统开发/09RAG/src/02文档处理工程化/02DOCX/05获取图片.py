from docx import Document
import os

def get_images(path):
    # 1.创建文档对象
    doc = Document(path)
    # 2.获取文档资源
    rels = doc.part.rels
    # 循环遍历文档当中所有的资源
    for rel in rels.values():
        # 3.筛选图片资源
        if "image" in rel.target_ref:
            # 4.获取图片的二进制流
            image_blob = rel.target_part.blob
            # 5.提取图片名称 设置保存路径
            # basename 截取文件名 剔除路径信息 图片原始名称
            image_name = os.path.basename(rel.target_ref)
            image_path = f'../../dataset/docx_img/{image_name}'
            # 6.将二进制流 写入文件
            with open(image_path, "wb") as f:
                f.write(image_blob)
                print(f"{image_name}保存成功")

get_images("../../dataset/DOCX素材.docx")