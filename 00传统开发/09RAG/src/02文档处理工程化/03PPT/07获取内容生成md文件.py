from pptx import Presentation

def parse_content_to_md():
    prst = Presentation('../../dataset/标题提取.pptx')
    md_lines = []
    # 遍历每一页幻灯片
    for slide in prst.slides:
        # 提取标题
        title = slide.shapes.title
        # 判断标题是否为空
        if title:
            # 一个 # 代表一个标题
            md_lines.append(f"# {title.text}")
        for shape in slide.shapes:
            # 判断是否是文本
            if hasattr(shape, "text"):
                text = shape.text.strip()
                if text:
                    # 当文本存在 也就是非空 才能放到列表当中
                    md_lines.append(text)
    # 将列表转为字符串 根据段落拼接
    markdown = "\n\n".join(md_lines)
    with open(f"../../dataset/ppt_md/ppt_md.md", "w", encoding='utf-8') as f:
        f.write(markdown)
        print("写入成功")

parse_content_to_md()