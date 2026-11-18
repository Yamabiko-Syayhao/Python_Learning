## 综合练习五：多模型多用户智能问答系统

### 需求描述
构建一个多模型多用户问答系统，要求：

1. **多模型初始化**：使用 `init_chat_model` 初始化两种不同的模型（如 `qwen3.6-plus` 通过 `model_provider='openai'` 和 DeepSeek 等其他模型），能够通过简单修改模型名称切换底层模型。

2. **重试机制**：对 LLM 调用链配置 `.with_retry()`：
   - 失败时自动重试，最多重试 3 次
   - 使用指数退避策略
   - 自定义一个异常类 `LLMServiceError`，当第一次请求时抛出该异常模拟失败

3. **多用户会话隔离**：使用 `RunnableWithMessageHistory` 管理至少 2 个用户的独立会话：
   - `user_A`：连续问 3 个编程相关问题
   - `user_B`：连续问 3 个生活类问题
   - 验证两个用户各自的对话上下文独立、不会串扰

4. **问题分类路由**：使用 `RunnableBranch` 根据用户问题内容将请求分流到不同的处理链：
   - 编程类问题（含"代码/Python/编程/bug/算法"等关键词）→ 使用技术专家 system prompt
   - 生活类问题（含"天气/美食/旅游/购物"等关键词）→ 使用生活助手 system prompt
   - 其他问题 → 使用通用助手 system prompt

5. **ConfigurableField 动态配置**：定义一个继承 `RunnableSerializable` 的响应策略类，包含以下可配置字段并通过 `configurable_fields()` + `ConfigurableField` 暴漏出来：
   - `max_response_length`：最大回复字数，默认 100
   - `system_role`：系统角色描述
   
   然后用 `with_config()` 创建"简洁版"（max_response_length=50）和"详细版"（max_response_length=200）两个预设版本。

6. **完整流程验证**：
   - 对 `user_A` 发送一个编程问题，使用详细版配置
   - 对 `user_B` 发送一个生活问题，使用简洁版配置
   - 再次对 `user_A` 发送一个引用历史的问题（如"刚才提到的那个方法，再详细讲讲"），验证会话记忆正常

---
