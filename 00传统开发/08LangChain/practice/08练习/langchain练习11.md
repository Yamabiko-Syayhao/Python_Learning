## 综合练习11：文档对比分析系统

### 练习目标
综合运用 **TextLoader（多文件） + RecursiveCharacterTextSplitter + ChatPromptTemplate + MessagesPlaceholder + InMemoryChatMessageHistory + RunnableWithMessageHistory + RunnableBranch** 构建一个多文档对比分析系统。

### 需求描述
1. **多文档加载**：使用 `TextLoader` 分别加载 `exercise_data_report_A.txt` 和 `exercise_data_report_B.txt` 两份工作总结。
2. **分别切分**：对两个文档分别使用 `RecursiveCharacterTextSplitter`（`chunk_size=300`，`chunk_overlap=50`）进行切分，并为每个文档的 metadata 添加 `source` 字段（分别标记为"技术研发部"和"产品运营部"）。
3. **对话模板**：将两份文档内容拼接，构建带 `MessagesPlaceholder` 的对话模板，system 消息中明确告知模型这是两个部门的 Q1 季度报告。
4. **问题分流**：使用 `RunnableBranch` 根据用户问题关键词分流：
   - 包含"技术/研发/系统/代码"关键词 → 偏向技术研发部视角回答
   - 包含"运营/用户/活动/GMV"关键词 → 偏向产品运营部视角回答
   - 默认 → 综合分析两个部门的报告
5. **记忆对话测试**：使用 `RunnableWithMessageHistory` 模拟 4 轮对话：
   - 第1轮（技术类）："技术研发部在上季度完成了哪些主要工作？"
   - 第2轮（运营类）："产品运营部的GMV目标完成情况如何？"
   - 第3轮（综合分析）："两个部门各自存在哪些问题？"
   - 第4轮（追问）："刚才说的技术部系统迁移问题，具体是什么？"

### 涉及知识点
| 序号 | 课件章节 | 知识点 |
|------|----------|--------|
| 01 | chat_model | `ChatOpenAI` 调用 |
| 02 | PromptTemplate | `ChatPromptTemplate.from_messages`、`MessagesPlaceholder` |
| 04 | LCEL | `RunnableBranch` 条件分支 |
| 05 | Memory | `InMemoryChatMessageHistory`、`RunnableWithMessageHistory` |
| 06 | Document | `TextLoader` 多文件加载 |
| 07 | Splitter | `RecursiveCharacterTextSplitter` 带 metadata |

### 提示
- 为不同文档设置不同 metadata 的方法：`splitter.split_documents([doc_a, doc_b])`，需要先构造带 source 的 Document 对象
- `RunnableBranch` 语法：`RunnableBranch((条件, 链), (条件, 链), 默认链)`
- 课件参考：`02-TextLoader.py`、`02-通用文本处理.py`、`06-RunnableBranch.py`
