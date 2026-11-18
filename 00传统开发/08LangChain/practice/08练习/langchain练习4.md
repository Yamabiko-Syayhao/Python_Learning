## 综合练习四：学习路径规划器（含容错机制）

### 需求描述
构建一个学习路径规划器，要求：

1. **Pydantic 数据模型**：定义如下 `StudyPlan` 模型：

```python
from pydantic import BaseModel, Field, model_validator
from typing import Literal

class DayPlan(BaseModel):
    day: int = Field(description='第几天', ge=1, le=30)
    focus: str = Field(description='当天学习重点')
    tasks: list[str] = Field(description='具体任务列表，至少2个', min_length=2)

class StudyPlan(BaseModel):
    tech_name: str = Field(description='技术名称')
    level: Literal['初级', '中级', '高级'] = Field(description='难度级别')
    duration_days: int = Field(description='学习天数', ge=1, le=30)
    daily_plan: list[DayPlan] = Field(description='每日计划')
    tips: list[str] = Field(description='学习建议', min_length=1)

    @model_validator(mode='after')
    def check_days_match(self):
        if len(self.daily_plan) != self.duration_days:
            raise ValueError(f'每日计划条数({len(self.daily_plan)})与学习天数({self.duration_days})不一致')
        return self
```

2. **LCEL 串行管道**：使用 `prompt_template | llm` 构建基础链。

3. **三层容错机制**：
   - 第一层：使用 `PydanticOutputParser` 正常解析模型输出
   - 第二层：如果解析失败，使用 `OutputFixingParser.from_llm()` 让 LLM 自动修复格式问题
   - 第三层：如果仍然失败，使用 `RetryWithErrorOutputParser.from_llm()` 带上原始 prompt 让模型重新生成

4. **模拟错误场景**：手动构造一个包含以下错误的输出字符串，验证容错流程：
   - 单引号替代双引号
   - 缺少某字段
   - `daily_plan` 条目数与 `duration_days` 不匹配

5. **正常流程测试**：让模型根据用户输入"我想在7天内入门 Python 爬虫，我会 Python 基础语法，但没接触过爬虫框架"生成学习计划。

