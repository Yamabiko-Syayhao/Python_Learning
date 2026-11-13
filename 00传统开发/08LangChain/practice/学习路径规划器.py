"""
学习路径规划器（Learning Path Planner）
=========================================
这是一个综合小练习，把 LangChain 的几块知识串起来：

    通用模板 -> partial 预设方向 -> FewShot 示例增强 -> LCEL 串联模型 -> 输出解析

它和 language.py 的翻译器是同一个套路，只是把"翻译"换成了"制定学习路径"。

整条流水线的数据流：
    用户输入(基础/时间) -> 模板拼出提示词 -> 大模型生成规划 -> 解析成纯字符串

涉及知识点：
    01 chat_model          ChatOpenAI 调用
    02 PromptTemplate      ChatPromptTemplate / partial / FewShotPromptTemplate / save / load_prompt
    03 OutputParser        StrOutputParser
    04 LCEL               用 | 把模板、模型、解析器串起来
"""

from pathlib import Path

from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    FewShotPromptTemplate,
    load_prompt,
)
from langchain_core.output_parsers import StrOutputParser

from config import DASHSCOPE_API_KEY, DASHSCOPE_BASE_URL
from langchain_openai import ChatOpenAI


# ============================================================
# 1. 初始化大模型
# ============================================================
# ChatOpenAI 走的是 OpenAI 兼容协议：
#   只要目标模型提供兼容接口，换一个 api_key + base_url 就能对接不同厂商的模型。
# 这里接的是阿里云百炼的 qwen 模型。
llm = ChatOpenAI(
    model="qwen3.8-flash",
    api_key=DASHSCOPE_API_KEY,
    base_url=DASHSCOPE_BASE_URL,
)


# ============================================================
# 2. 通用学习规划模板（ChatPromptTemplate）
# ============================================================
# from_messages 接收一个"消息列表"，每个元素是 (角色, 内容)：
#   system -> 给模型设定身份和任务（它的"人设"）
#   human  -> 用户给出的需求
# 花括号 {xxx} 是占位符（变量），调用时再填具体值。
#
# 这里留了三个变量：
#   current : 学员当前基础
#   months  : 可投入的月数
#   target  : 想学习的目标方向
planner_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一名经验丰富的学习规划师。请根据学员的{current}基础和{months}个月的可用时间，"
            "为 ta 制定一份循序渐进的{target}学习路径。要求分阶段，每个阶段写清学习目标和产出成果。",
        ),
        ("human", "请为我制定学习计划。"),
    ]
)


# ============================================================
# 3. 用 partial 预设三个目标方向
# ============================================================
# partial 的含义：先把模板的一部分变量"钉死"，返回一个剩变量更少的新模板。
# 原模板 planner_template 不会被修改。
#
# 这样三个方向共用同一套人设和格式，只在 target 上不同，
# 避免了复制粘贴三份几乎一样的模板。
python_backend = planner_template.partial(target="Python 后端开发")
data_analysis = planner_template.partial(target="数据分析")
frontend = planner_template.partial(target="前端开发")


# ============================================================
# 4. FewShot 示例增强（只给 Python 后端方向加示例）
# ============================================================
# FewShot 的思路：先给模型看几组"输入 -> 期望输出"的范例，
# 让它照着范例的格式和粒度来回答当前问题。
#
# example_prompt 决定"单个示例长什么样"，
# 其中的变量名(current / months / path)必须和 examples 里每个 dict 的 key 完全一致。
example_prompt = PromptTemplate.from_template(
    "基础: {current}\n时间: {months} 个月\n路径: {path}"
)

# 至少准备 3 组示例，覆盖不同基础、不同时长的场景。
# 真实、具体的示例比占位符更能约束模型的输出质量。
examples = [
    {
        "current": "零基础",
        "months": "3",
        "path": (
            "第1阶段(1个月)：掌握 Python 语法、变量、循环、函数；产出：能写小脚本。"
            "第2阶段(1个月)：学习 Flask/FastAPI、HTTP、REST；产出：完成一个待办 API。"
            "第3阶段(1个月)：学习数据库与部署；产出：上线一个带数据库的博客接口。"
        ),
    },
    {
        "current": "会一点 Python",
        "months": "2",
        "path": (
            "第1阶段(1个月)：补强面向对象、异常处理、常用标准库；产出：重构一个小项目。"
            "第2阶段(1个月)：学习 FastAPI + MySQL + Docker；产出：部署一个完整 CRUD 服务。"
        ),
    },
    {
        "current": "有其他语言基础",
        "months": "1",
        "path": (
            "第1阶段(2周)：快速过 Python 语法与生态差异；产出：完成 20 道语法练习。"
            "第2阶段(2周)：直接上手 FastAPI + 数据库；产出：一个可运行的 API 项目。"
        ),
    },
]

# FewShotPromptTemplate 的五个核心参数：
#   examples        : 示例列表
#   example_prompt  : 单个示例的排版模板
#   prefix          : 所有示例前面的话（身份 / 任务说明）
#   suffix          : 所有示例后面的话，通常留一个占位符接收"当前要处理的内容"
#   input_variables : 最终调用 invoke 时需要传入的变量名（来自 suffix）
python_backend_fewshot = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="你是一名学习规划师，请参考下面的示例格式，为学员制定 Python 后端开发学习路径。",
    suffix="基础: {current}\n时间: {months} 个月\n路径:",
    input_variables=["current", "months"],
)


# ============================================================
# 5. LCEL 串行管道
# ============================================================
# 模板、模型、解析器都实现了统一的 Runnable 接口，所以可以用 | 依次连接。
# 数据像流水线一样传递：
#   dict -> 提示词 -> AIMessage -> str
#
# StrOutputParser 的作用：
#   大模型直接返回的是 AIMessage 对象，还要 .content 才能取正文；
#   加上它以后，整条链的最终输出直接就是纯字符串，用起来更干净。
#
# 注意：链的输入 key 必须和该链模板里的变量名一致。
#   - python_backend_chain 用的是 FewShot 模板，变量是 current / months
#   - data_analysis_chain / frontend_chain 用的是通用模板，变量是 current / months
#     （target 已被 partial 钉死，不用再传）
python_backend_chain = python_backend_fewshot | llm | StrOutputParser()
data_analysis_chain = data_analysis | llm | StrOutputParser()
frontend_chain = frontend | llm | StrOutputParser()


# ============================================================
# 6. 保存 / 加载模板
# ============================================================
# 把模板存成 JSON 文件，下次不用重新写代码就能直接加载复用。
# 用 Path(__file__).parent 拿到脚本所在目录，避免受运行目录影响。
BASE_DIR = Path(__file__).resolve().parent
SAVE_PATH = BASE_DIR / "python_backend_planner.json"


def save_and_verify():
    """保存 FewShot 模板为 JSON，再用 load_prompt 读回来验证一致性。"""
    # save() 会根据后缀决定格式：.json 存 JSON，.yaml 存 YAML
    python_backend_fewshot.save(str(SAVE_PATH))

    # load_prompt 从文件重建 Prompt 对象
    loaded = load_prompt(str(SAVE_PATH))

    sample = {"current": "零基础", "months": "3"}
    same = loaded.invoke(sample).to_string() == python_backend_fewshot.invoke(sample).to_string()

    print(f"模板已保存到: {SAVE_PATH}")
    print(f"加载后与原模板拼装结果一致: {same}")
    return loaded


if __name__ == "__main__":
    # ---- 方向一：零基础转 Python 后端（使用 FewShot 增强模板）----
    print("=== Python 后端开发（FewShot 增强）===")
    print(python_backend_chain.invoke({"current": "零基础", "months": "3"}))

    # ---- 方向二：有基础转数据分析 ----
    print("\n=== 数据分析 ===")
    print(data_analysis_chain.invoke({"current": "会 Python 基础语法", "months": "2"}))

    # ---- 方向三：转前端开发 ----
    print("\n=== 前端开发 ===")
    print(frontend_chain.invoke({"current": "零基础", "months": "3"}))

    # ---- 保存并加载模板 ----
    print("\n=== 保存与加载验证 ===")
    loaded_prompt = save_and_verify()

    # ---- 用加载回来的模板真实跑一次，证明功能可用 ----
    print("\n=== 用加载后的模板生成一次学习路径 ===")
    loaded_chain = loaded_prompt | llm | StrOutputParser()
    print(loaded_chain.invoke({"current": "会一点 Python", "months": "2"}))
