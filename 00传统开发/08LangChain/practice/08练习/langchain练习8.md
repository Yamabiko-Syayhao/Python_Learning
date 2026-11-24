## 综合练习8：产品手册智能助手

### 练习目标
综合运用 **UnstructuredMarkdownLoader + MarkdownHeaderTextSplitter + RecursiveCharacterTextSplitter + ChatPromptTemplate + InMemoryChatMessageHistory + RunnableWithMessageHistory** 构建产品手册智能问答系统。

### 需求描述
1. **文档加载**：使用 `UnstructuredMarkdownLoader` 加载 `exercise_data_product_manual.md` 文件。
2. **结构切分**：首先使用 `MarkdownHeaderTextSplitter` 按标题层级（`#` → `Header1`，`##` → `Header2`，`###` → `Header3`）进行结构切分，设置 `strip_headers=False` 保留标题。
3. **长度控制**：对结构切分后的文档，再使用 `RecursiveCharacterTextSplitter`（`chunk_size=300`，`chunk_overlap=50`）进行长度控制切分。
4. **显示切分结果**：遍历最终切分的文档，打印每个 chunk 的 metadata（包含 Header1/Header2/Header3 信息）和 content 前80个字符。
5. **对话模板**：将切分后的文档内容拼接为知识库上下文，构建带 `MessagesPlaceholder` 的对话模板。
6. **记忆对话测试**：使用 `RunnableWithMessageHistory` 实现 3 轮对话：
   - 第1轮："如何录入指纹？"
   - 第2轮："电池能用多久？没电了怎么办？"
   - 第3轮："刚才说的临时密码功能，具体怎么设置？"
7. **验证**：打印对话历史和每个 chunk 的 metadata。

### 涉及知识点
| 序号 | 课件章节 | 知识点 |
|------|----------|--------|
| 02 | PromptTemplate | `ChatPromptTemplate.from_messages`、`MessagesPlaceholder` |
| 05 | Memory | `InMemoryChatMessageHistory`、`RunnableWithMessageHistory` |
| 06 | Document | `UnstructuredMarkdownLoader` 加载 Markdown |
| 07 | Splitter | `MarkdownHeaderTextSplitter` + `RecursiveCharacterTextSplitter` 两段式切分 |

### 提示
- 两段式切分："先保结构，再控长度"
- 数据集文件：`极速通智能门锁-产品手册.md`
