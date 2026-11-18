## 综合练习12：CharacterTextSplitter + FewShot 增强记忆问答

### 练习目标
综合运用 **TextLoader + CharacterTextSplitter + FewShotPromptTemplate + ChatPromptTemplate + MessagesPlaceholder + InMemoryChatMessageHistory + RunnableWithMessageHistory** 构建带 FewShot 示例的客服问答系统。

### 需求描述
1. **文档加载与切分**：使用 `TextLoader` 加载 `智能客服平台知识库.txt`，用 `CharacterTextSplitter`（`separator='\n\n'`，`chunk_size=150`，`chunk_overlap=30`）进行切分。
2. **切分结果对比**：分别使用 `split_text()` 和 `create_documents()` 两种方法展示切分结果，比较两者的区别。
3. **FewShot 示例**：创建一个 `FewShotPromptTemplate`，提供至少 3 组客服问答示例（包含"退货"、"配送"、"会员"三个场景），`example_prompt` 使用 `PromptTemplate.from_template("用户: {question}\n客服: {answer}")` 格式。
4. **对话模板**：将 FewShot 示例拼接到对话模板中，同时 system 消息包含知识库上下文。
5. **记忆对话测试**：模拟 4 轮对话验证 FewShot 效果和记忆功能：
   - 第1轮："我的订单还没收到，能帮我查一下吗？"
   - 第2轮："如果我要退货，需要满足什么条件？"
   - 第3轮："金卡会员有什么优惠？和钻石会员比差多少？"
   - 第4轮："刚才说的金卡会员权益，还有没有其他我没注意到的？"
