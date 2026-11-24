

## 综合练习二：多语种翻译工作流

### 练习目标
综合运用 **PromptTemplate + ChatPromptTemplate + PartiallyPromptTemplate + FewShotPromptTemplate + StrOutputParser + LCEL 串行** 构建一个灵活的多语种翻译器。

### 需求描述
构建一个翻译工作流，要求：

1. **通用翻译模板**：使用 `ChatPromptTemplate.from_messages` 创建翻译模板，包含 `source`（源语言）、`target`（目标语言）、`text`（待翻译文本）三个变量。

2. **方向预设**：使用 `partial()` 方法将通用翻译模板预设为三个专用方向：
   - `en2zh`：英语 → 中文
   - `zh2en`：中文 → 英文
   - `zh2ja`：中文 → 日文

3. **FewShot 示例增强**：为 `zh2en` 方向创建一个 `FewShotPromptTemplate`，至少提供 3 组中英对照示例，覆盖日常用语和专业术语场景。示例模板使用 `PromptTemplate.from_template("中文: {chinese}\n英文: {english}")` 格式。

4. **LCEL 串行管道**：使用 `|` 将 `prompt | llm | StrOutputParser` 串成一个完整链条，对以下三句话分别调用三个方向进行翻译：
   - 英译中：`"Artificial intelligence is reshaping every industry at an unprecedented pace."`
   - 中译英：`"今天天气真好，我们一起去公园散步吧。"`（使用 FewShot 增强模板）
   - 中译日：`"感谢您的耐心等待，您的订单已发货。"`

5. **保存和加载模板**：将 `zh2en` 方向的 FewShot 翻译模板用 `save()` 方法保存为 JSON 文件，再用 `load_prompt()` 重新加载并验证功能一致。

### 涉及知识点
| 序号 | 课件章节 | 知识点 |
|------|----------|--------|
| 01 | chat_model | `ChatOpenAI` 调用 |
| 02 | PromptTemplate | `PromptTemplate`、`ChatPromptTemplate`、`partial`、`FewShotPromptTemplate`、`save`/`load_prompt` |
| 03 | OutputParser | `StrOutputParser` |
| 04 | LCEL | `|` 管道运算符串联 prompt + llm + parser |

### 提示
- `PromptTemplate.from_template()` 可以直接用字符串创建模板
- `FewShotPromptTemplate` 需要指定 `examples`、`example_prompt`、`prefix`、`suffix`、`input_variables`
- `load_prompt()` 加载后需要用 `invoke()` 传入变量
- 课件参考：`01-StringPromptTemplate.py`、`02-ChatPromptTemplate.py`、`04-FewShotPromptTemplate.py`、`05-LoadPrompt.py`、`06-PartiallyPromptTemplate.py`、`01-StrOutParser.py`

---
