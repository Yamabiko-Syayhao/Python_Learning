## 综合练习14：Task 文档处理 + 知识库对话系统

### 练习目标
综合运用 **TextLoader + 三种 Splitter 对比 + RunnableWithMessageHistory + 条件分流** 构建一个知识库问答系统，重点理解三种 Splitter 的差异。

### 需求描述
1. **文档加载**：使用 `TextLoader` 加载 `智能客服平台知识库.txt`。
2. **三种切分器对比**：
   - 使用 `CharacterTextSplitter`（`chunk_size=150`, `chunk_overlap=30`, `separator='\n\n'`）切分，将结果存入变量 `chunks_char`
   - 使用 `RecursiveCharacterTextSplitter`（`chunk_size=150`, `chunk_overlap=30`）切分，结果存入 `chunks_recursive`
   - 使用 `TokenTextSplitter`（`chunk_size=60`, `chunk_overlap=15`, `encoding_name='cl100k_base'`）切分，结果存入 `chunks_token`
3. **对比打印**：分别打印三种切分器的 chunk 数量、第一个 chunk 的文本长度，以及第一个 chunk 的内容前80个字符。
4. **选用递归切分器**：选择 `RecursiveCharacterTextSplitter` 的切分结果作为知识库上下文。
5. **对话模板**：构建带 `MessagesPlaceholder` 的对话模板。
6. **记忆对话**：使用 `RunnableWithMessageHistory` 进行 3 轮对话测试：
   - 第1轮："会员等级有哪些？分别有什么权益？"
   - 第2轮："支付失败有哪些可能的原因？"
   - 第3轮："你刚才说的这些问题，哪些是我作为普通会员可能遇到的？"

### 涉及知识点
| 序号 | 课件章节 | 知识点 |
|------|----------|--------|
| 02 | PromptTemplate | `ChatPromptTemplate.from_messages`、`MessagesPlaceholder` |
| 05 | Memory | `InMemoryChatMessageHistory`、`RunnableWithMessageHistory` |
| 06 | Document | `TextLoader` |
| 07 | Splitter | `CharacterTextSplitter` vs `RecursiveCharacterTextSplitter` vs `TokenTextSplitter` |

### 提示
