"""
文档入库 RAG 的标准流水线
任意格式文件 -》partition统一解析-》元素结构化（标题/正文等分类）-》智能分块-》langchian document
"""
from langchain_core.documents import Document
from unstructured.chunking.title import chunk_by_title
from unstructured.partition.auto import partition

class UnstructuredProcessor:
    # 统一识别读取文档
    def parse(self, file_path):
        # 调用partition自动识别文件类型并解析 返回的是element对象列表，每个元素带 category、text、metadata
        # 修改 1：添加 strategy="hi_res" 保证解析质量。
        # 修改 2：如果你的 Poppler 环境变量配好了，不需要加 poppler_path。
        # 如果一直报错，可以解开下面 poppler_path 的注释，换成你自己的实际路径（注意是 bin 文件夹的路径）。
        return partition(
            filename=file_path,
            languages=["chi_sim"],
            strategy="hi_res",
            # poppler_path="../../poppler-26.02.0/Library/bin"  # <--- 视你的 Poppler 安装情况决定是否解开注释
        )

    # 切片
    def chunk(self, elements, max_chars=1000):
        """

        :param elements: 解析得到的文本列表
        :param max_chars: 块最大字符数
        :return: 分好的结果
        """
        return chunk_by_title(
            elements,
            max_characters=max_chars,
            combine_text_under_n_chars=200 #小于200字的碎段自动并入相邻块，避免产生"一句话一块"的碎片。
        )
    # 转langchain document
    def to_doc(self, chunks):
        """
        :param chunks: 切片结果列表
        :return: doc列表
        """
        # 列表推导式 一次性构造所有 Document
        return [
            Document(
                page_content=c.text,
                metadata={
                    # 来源文件名 ---> 溯源
                    "source": c.metadata.filename,
                    # 页码 ---> 应用定位
                    "page": c.metadata.page_number,
                    # 元素类型 ---->可按类型过滤
                    "category": c.category,
                }
            ) for c in chunks
        ]

    def process(self, file_path):
        ele = self.parse(file_path) #第一步解析文档
        print(ele,"ele")
        chunks = self.chunk(ele) #第二部 语义分块
        print(chunks,"chunks")
        return self.to_doc(chunks) #转为lc文档


if __name__ == '__main__':
    pro = UnstructuredProcessor()
    docs = pro.process("../../dataset/产品手册_v2.pdf")
    print(docs)