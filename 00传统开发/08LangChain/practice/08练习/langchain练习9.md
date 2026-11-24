## 综合练习9：AI知识库对话系统（含数据库持久化）

### 练习目标
综合运用 **TextLoader + RecursiveCharacterTextSplitter + ChatPromptTemplate + SQLChatMessageHistory + RunnableWithMessageHistory + StrOutputParser** 构建一个将对话记忆持久化到数据库的知识库问答系统。

### 需求描述
1. **文档加载与切分**：使用 `TextLoader` 加载 `exercise_data_ai_intro.txt`，用 `RecursiveCharacterTextSplitter`（`chunk_size=250`，`chunk_overlap=60`）进行切分，将切分后的内容拼接为知识库上下文。
2. **数据库记忆**：使用 `SQLChatMessageHistory`（SQLite 数据库）存储对话历史。数据库文件名为 `exercise_chat_history.db`。创建 `get_session_history` 函数返回 `SQLChatMessageHistory` 实例。
3. **对话模板**：创建带 `MessagesPlaceholder` 的对话模板，system 包含 AI 知识库上下文。
4. **LCEL 管道**：使用 `prompt | llm | StrOutputParser` 构建链。
5. **多用户测试**：模拟 2 个用户 `user_ai_001` 和 `user_ai_002` 的独立会话：
   - `user_ai_001` 连续问："什么是大语言模型？" → "LangChain的核心概念有哪些？" → "RAG是什么？"
   - `user_ai_002` 连续问："什么是Embedding？" → "Token是什么意思？"
6. **验证**：使用 `show_history` 函数分别打印两个用户的数据库历史消息，确认会话隔离。

### 提示
- 数据集文件：`人工智能简介.txt`
