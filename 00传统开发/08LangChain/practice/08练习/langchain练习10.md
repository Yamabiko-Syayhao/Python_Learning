
## 综合练习10：Token 级精确切分 + 记忆对话

### 练习目标
综合运用 **TextLoader + TokenTextSplitter + ChatPromptTemplate + InMemoryChatMessageHistory + RunnableWithMessageHistory + PydanticOutputParser** 构建一个精确控制 token 预算的知识问答系统。

### 需求描述
1. **文档加载**：使用 `TextLoader` 加载 `exercise_data_ai_intro.txt`。
2. **Token 级切分**：使用 `TokenTextSplitter` 对文档进行切分，配置 `encoding_name='cl100k_base'`，`chunk_size=100`，`chunk_overlap=30`。
3. **打印 token 数**：切分后，对每个 chunk 使用 `tiktoken.get_encoding('cl100k_base').encode()` 计算实际 token 数，打印每个 chunk 的 token 数和前50个字符。
4. **结构化提取**：使用 `PydanticOutputParser` 定义以下数据模型，从用户问题中提取关键信息：

```python
from pydantic import BaseModel, Field
from typing import Literal

class AIQuestion(BaseModel):
    topic: Literal['LLM', 'LangChain', 'RAG', 'Embedding', 'Token', 'Other'] = Field(description='话题分类')
    difficulty: Literal['入门', '进阶', '高级'] = Field(description='问题难度')
    keywords: list[str] = Field(description='问题中的关键词列表，至少1个', min_length=1)
    need_example: bool = Field(description='是否需要举例说明')
```

5. **对话流程**：使用 `RunnableWithMessageHistory` 实现 3 轮对话：
   - 第1轮："LangChain中的Chain是什么概念？请举例说明"
   - 第2轮："那和Runnable有什么区别？"
   - 第3轮："刚才你说到的那个概念，能再详细解释一下吗？"
6. **解析输出**：每轮对话后，用 `PydanticOutputParser` 从问题文本中提取 `AIQuestion` 结构化信息并打印。


### 提示
- 获取编码器
- 获取 token 数
- 数据集文件：`人工智能简介.txt`
