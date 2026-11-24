"""
专门针对 markdown 文档的结构化分割器
适合文件： README.md 产品手册 一些用 md 格式的文档 知识库文件等等
按照 # 号标题的层级去切割 并且会把各级标题保存到 metadata 的元数据中，每个分片自带
文档目录和溯源信息
"""
from langchain_text_splitters import MarkdownHeaderTextSplitter,RecursiveCharacterTextSplitter

markdown_text = """
## 第一部分：AI大模型应用开发核心基础名词

这些名词按“从基础到应用”的顺序排列，后面的名词会依赖前面的概念，大家跟着节奏来，不要跳读。

### 一、基础核心名词（模型本身相关）

#### 1\. AI大模型（Large Language Model, LLM）

「定义」：简单说，就是“能理解人类语言、生成人类语言，还能完成复杂任务的‘超级大脑’”。它是通过海量文本数据（书籍、网页、对话等）训练出来的，具备“举一反三”的能力，能处理文字相关的几乎所有任务（问答、创作、翻译、总结等）。

「小白案例」：大家平时用的ChatGPT、豆包、文心一言，都是AI大模型；校园里的“智能答疑机器人”（比如问“选修课怎么选”“图书馆开馆时间”），背后也是大模型在支撑；甚至你们写论文时用的“论文润色工具”，核心也是大模型。

「关键补充」：我们做“应用开发”，不是自己训练大模型（成本太高、技术难度太大），而是“调用已有的大模型”（比如调用豆包API、ChatGPT API），让它帮我们完成具体任务——这也是我们后续学习的核心：如何“指挥”大模型做事。

#### 2\. 模型训练（Training）

「定义」：大模型“学习”的过程，就像人类小时候“读书识字、积累知识”的过程。工程师会给模型输入海量的文本数据（比如所有中文书籍、互联网上的合法对话、专业文献等），让模型从数据中总结规律（比如“‘你好’的回应通常是‘你好呀’‘您好’”“数学题1\+1=2”）。

「小白案例」：相当于老师给你布置10000道语文题、数学题，让你反复做，直到你能熟练掌握“题目和答案的对应规律”——模型训练就是这个过程，只不过它处理的是亿级、万亿级的“题目”（文本数据）。

「铺垫重点」：我们不做“训练”，但要知道：模型的能力是“训练出来的”，它能做什么、不能做什么，取决于训练数据。比如，没学过“大学生选修课规则”的模型，就无法准确回答“选修课挂科了怎么办”。

#### 3\. 模型微调（Fine\-tuning）

「定义」：在已训练好的大模型基础上，再用“小范围、针对性的数据”重新训练，让模型更贴合某个具体场景（比如校园场景、医疗场景、法律场景）。相当于“给大模型做‘专项培训’”。

「小白案例」：豆包本身能回答各种通用问题，但如果我们想让它变成“校园专属助手”，就可以用“校园规章制度、常见学生问题、校园活动信息”这些数据，对豆包进行微调——微调后，它回答“校园相关问题”会更准确，比如能精准说出“本校选修课报名时间是每年3月和9月”，而不是通用的“一般选修课报名在学期初”。

「铺垫重点」：微调是“高级操作”，而我们后续学的「提示词」，是“不用微调，也能让通用大模型适配具体场景”的低成本方法——这也是提示词的核心价值：高效、低成本地“指挥”大模型。
"""

# 配置要切割的标题层级 Header1标记名称---->会存储到metadata中
headers_to_split_on = [("#","Header1"),("##","Header2"),("###","Header3"),("####","Header4")]
# =============== 写法1 默认模式 strip_headers=True 正文标题放在 metadata 里面了
# 初始化分割器
# headers_to_split_on 定义要识别切割的标题标记
# splitter = MarkdownHeaderTextSplitter(
#     headers_to_split_on=headers_to_split_on,
# )
# docs = splitter.split_text(
#     markdown_text
# )
# for doc in docs:
#     print(doc.metadata)
#     print(doc.page_content)
#     print("*"*100)

# =============== 写法2 默认模式 strip_headers=False 正文保留标题
# splitter = MarkdownHeaderTextSplitter(
#     headers_to_split_on=headers_to_split_on,strip_headers=False
# )
# docs = splitter.split_text(
#     markdown_text
# )
# for doc in docs:
#     print(doc.metadata)
#     print(doc.page_content)
#     print("*"*100)

# =============== 写法3 正文逐行拆分成独立文档（超细颗粒度）
# splitter = MarkdownHeaderTextSplitter(
#     headers_to_split_on=headers_to_split_on,strip_headers=False,return_each_line=True
# )
# docs = splitter.split_text(
#     markdown_text
# )
# for doc in docs:
#     print(doc.metadata)
#     print(doc.page_content)
#     print("*"*100)

# 结构分割+长度约束
# MarkdownHeaderTextSplitter 按章节划分 带
# RecursiveCharacterTextSplitter 控制分片的最大长度

# 第一步 按照标题进行拆分
splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on,
    strip_headers=False
)
docs = splitter.split_text(
    markdown_text
)
# 第二步 对过长的章节再次分割 控制 chunk 大小
final_splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=20,
)
chunks = final_splitter.split_documents(docs)
for chunk in chunks:
    print(chunk.metadata)
    print(chunk.page_content)
    print("*"*100)