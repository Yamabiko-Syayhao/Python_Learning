## 综合练习13：Markdown 文档结构切分 + 逐行分析

### 练习目标
综合运用 **UnstructuredMarkdownLoader + MarkdownHeaderTextSplitter（return_each_line=True） + RecursiveCharacterTextSplitter + ChatPromptTemplate + InMemoryChatMessageHistory + RunnableWithMessageHistory** 实现 Markdown 文档的精细结构化分析。

### 需求描述
1. **文档加载**：使用 `UnstructuredMarkdownLoader` 加载 `python311发行说明.md`。
2. **逐行结构切分**：使用 `MarkdownHeaderTextSplitter` 进行切分，设置 `headers_to_split_on=[('#', 'Header1'), ('##', 'Header2'), ('###', 'Header3')]`，`strip_headers=False`，`return_each_line=True`。
3. **显示切分结果**：遍历切分结果，打印每行的 metadata（包含 Header1/Header2/Header3 信息）和 content。
4. **长度控制**：对逐行切分后的文档，再用 `RecursiveCharacterTextSplitter`（`chunk_size=200`，`chunk_overlap=40`）进行长度约束切分。
5. **对话模板**：将最终切分后的文档内容作为知识库，构建带 `MessagesPlaceholder` 的对话模板。
6. **记忆对话测试**：模拟 3 轮对话：
   - 第1轮："Python 3.11有哪些性能改进？"
   - 第2轮："异常处理有什么新特性？"
   - 第3轮："刚才提到的类型系统改进，Self Type具体怎么用？"

### 提示

- 数据集文件：`python311发行说明.md`
