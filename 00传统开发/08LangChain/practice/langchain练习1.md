# LangChain 基础课程 —— 综合练习

> 所有练习均使用 `utils.llm` 中的 `chat_utils()` 或 `chat_prompt()` 作为底层大模型调用。

---

## 综合练习一：智能客服工单系统

### 练习目标
综合运用 **ChatPromptTemplate + MessagesPlaceholder + ChatMessageHistory + RunnableWithMessageHistory + PydanticOutputParser + RunnableBranch** 构建一个带历史记忆的智能客服工单系统。

### 需求描述
搭建一个客服对话系统，要求：

1. **多用户会话管理**：使用 `RunnableWithMessageHistory` 维护不同用户（不同 `session_id`）的独立对话上下文。
2. **对话中自动分类**：当用户描述问题时，系统在给出客服回复的同时，使用 `RunnableBranch` 将问题分流到三个队列：
   - `REFUND_QUEUE`（退款类：包含"退款/退货/重复扣款"等关键词）
   - `TECHNICAL_QUEUE`（技术类：包含"报错/无法登陆/闪退/bug"等关键词）
   - `GENERAL_QUEUE`（普通咨询，默认）
3. **工单结构化提取**：使用 `PydanticOutputParser` 从用户描述中提取以下结构化工单信息：

```python
from pydantic import BaseModel, Field
from typing import Literal

class SupportTicket(BaseModel):
    ticket_id: str = Field(description='工单编号，格式如 TK-20260520-001')
    priority: Literal['low', 'medium', 'high'] = Field(description='优先级')
    category: Literal['refund', 'technical', 'general'] = Field(description='问题类别')
    summary: str = Field(description='问题摘要，不少于10个字', min_length=10)
    contact: str = Field(description='用户联系方式')
```

4. **完整对话流程**：模拟 3 轮对话，第一轮用户描述问题，第二轮追问进度，第三轮用户确认 — 每一轮都能看到之前的对话上下文。

### 涉及知识点
| 序号 | 课件章节 | 知识点 |
|------|----------|--------|
| 01 | chat_model | `ChatOpenAI` 模型调用、`invoke` 方法 |
| 02 | PromptTemplate | `ChatPromptTemplate.from_messages`、`MessagesPlaceholder` |
| 03 | OutputParser | `PydanticOutputParser`、`get_format_instructions`、`Field` 约束 |
| 04 | LCEL | `RunnableBranch` 条件分支、`|` 管道串联 |
| 05 | Memory | `InMemoryChatMessageHistory`、`RunnableWithMessageHistory`、`get_session_history` |

### 提示
- `RunnableWithMessageHistory` 需要指定 `history_messages_key`、`input_messages_key` 和 `get_session_history`
- `RunnableBranch` 用法：`RunnableBranch((条件1, 链1), (条件2, 链2), 默认链)`
