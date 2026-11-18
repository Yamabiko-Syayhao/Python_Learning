# LangChain 综合练习

> 所有练习均使用 `utils.llm` 中的 `chat_utils()` 作为底层大模型调用。

---

## 综合练习6：客服知识库问答系统

### 练习目标
综合运用 **TextLoader + RecursiveCharacterTextSplitter + ChatPromptTemplate + InMemoryChatMessageHistory + RunnableWithMessageHistory** 构建一个基于本地知识库的客服问答系统。

### 需求描述
1. **文档加载**：使用 `TextLoader` 加载 `exercise_data_knowledge_base.txt` 文件。
2. **文本切分**：使用 `RecursiveCharacterTextSplitter` 对加载的文档进行切分，设置 `chunk_size=200`，`chunk_overlap=50`。
3. **对话模板**：使用 `ChatPromptTemplate.from_messages` 创建对话模板，模板包含：
   - system 消息：告诉模型它是客服助手，并将切分后的知识库内容作为参考上下文
   - `MessagesPlaceholder` 用于存放历史对话
   - human 消息：接收用户问题
4. **历史记忆**：使用 `InMemoryChatMessageHistory` + `RunnableWithMessageHistory` 实现多轮对话记忆功能。
5. **多轮对话测试**：模拟 3 轮对话，要求：
   - 第1轮：用户问"退货政策是怎样的？"——模型应能参考知识库内容回答
   - 第2轮：用户问"那退款需要多久到账？"——模型应能结合上下文和知识库回答
   - 第3轮：用户追问"如果超过时间没收到退款怎么办？"——模型应记住前两轮对话并参考知识库
6. **验证**：打印完整会话历史，验证记忆功能正常。

### 涉及知识点
| 序号 | 课件章节 | 知识点 |
|------|----------|--------|
| 01 | chat_model | `ChatOpenAI` 模型调用 |
| 02 | PromptTemplate | `ChatPromptTemplate.from_messages`、`MessagesPlaceholder` |
| 05 | Memory | `InMemoryChatMessageHistory`、`RunnableWithMessageHistory`、`get_session_history` |
| 06 | Document | `TextLoader` 加载 txt 文件 |
| 07 | Splitter | `RecursiveCharacterTextSplitter` 切分文档 |

### 提示
- 加载文档后使用 `splitter.split_documents(docs)` 进行切分
- 将切分后的所有 chunk 的 `page_content` 拼接成知识库字符串，放入 system prompt
- 课件参考：`02-TextLoader.py`、`02-通用文本处理.py`、`03-ChatMessageHistory.py`、`04-RunnableWithMessageHistory.py`
- 数据集文件：`智能客服平台知识库.txt`
