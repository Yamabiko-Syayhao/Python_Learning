## 综合练习15：企业知识库全链路系统

### 练习目标
综合运用 **多格式 Document Loader + 多种 Splitter + SQLChatMessageHistory + RunnableWithMessageHistory + JsonOutputParser + StrOutputParser + RunnableBranch** 全方位构建企业级知识库问答系统。

### 需求描述
1. **多源文档加载**：
2. **分类切分**：
   - AI 知识文档用 `RecursiveCharacterTextSplitter`（`chunk_size=200`, `chunk_overlap=50`）
   - CSV 数据保留原始格式不切分（每条数据作为一个完整 chunk）
   - Markdown 文档用 `MarkdownHeaderTextSplitter` + `RecursiveCharacterTextSplitter` 两段式切分（`chunk_size=200`, `chunk_overlap=50`）
3. **统一标记 metadata**：为不同来源的文档设置不同的 `source` metadata（`ai_knowledge` / `customer_data` / `product_manual`）。
4. **对话模板**：将三种来源的知识拼接，构建带 `MessagesPlaceholder` 的综合对话模板。
5. **数据库持久化**：使用 `SQLChatMessageHistory` 存储对话历史，数据库文件 `exercise_full_chain.db`。
6. **结构化提取**：使用 `JsonOutputParser` 让模型在回答后，额外输出一个 JSON，包含：
   - `answer_source`：回答依据的来源（ai_knowledge / customer_data / product_manual / combined）
   - `confidence`：置信度（high / medium / low）
   - `referenced_count`：引用的 chunk 数量
7. **多用户多轮测试**：模拟 2 个用户、各 3 轮对话：
   - `user_001`：问 AI 知识类问题（如"LangChain的核心组件有什么？" → "RAG的工作原理是什么？" → "我之前问的LangChain组件，再总结一下"）
   - `user_002`：问产品+客户类问题（如"智能门锁怎么录入指纹？" → "有多少钻石会员？" → "北京的钻石会员有几个？"）
8. **验证**：分别展示两个用户的数据库对话历史，验证多用户会话隔离和知识覆盖。


### 提示
- 数据集文件：`极速通智能门锁-产品手册.md`、`客户数据表.csv`、`人工智能简介.txt`