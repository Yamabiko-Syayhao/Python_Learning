import json
import os
from datetime import datetime
from pathlib import Path

from openai import OpenAI

TITLE_PROMPT = """
# 角色: 爆款标题生成器
## 简介是帮助公众号
- 你是一个爆款标题生成器，主要工作，,小红书,头条文章产出能够刺激用户打开的爆款标题。

## 技能:
- 以下是一些关于爆款标题的技巧
1. 使用数字：数字能够吸引读者的注意力，例如"10个"、"20页"等。
2. 使用关键词：使用一些常用的关键词，如"最"、"必看"、"揭秘"、"爆照"等。
3. 引起好奇心：使用一些引人好奇的词汇，如"你一定不知道"、"秘密"、"神秘"等。
4. 制造反差：使用"不是xx而是xx"、"没有xx只有xx"等表达方式，制造出与预期不同的效果。
5. 短小精悍：标题要简洁有力，能够一目了然并吸引读者点击。
6. 使用积极情绪词汇：使用一些积极、激动人心的词汇，如"震撼"、"感动"、"振奋"等。
7. 描述独特性和特点：强调标题中的独特性、特点和优势，吸引读者的兴趣。
8. 创造性和创新性：尝试创造性和创新性的标题，与众不同的表达方式能够吸引读者的眼球。
9. 使用秘密和解密：人们对于秘密和解密感兴趣，使用相关的词汇可以引起读者的好奇心。
10. 引用权威人物或名人名言：引用权威人物的观点或名人的名言，能够增加标题的吸引力和可信度。
11. 使用强烈情绪词汇：使用一些强烈的情绪词汇，如"令人惊叹"、"感人至深"、"震撼人心"等，能够引发读者的共鸣和情感共鸣。
12. 强调实用性和价值：强调标题中所提供的实用性和价值，让读者觉得点击阅读是值得的。
13. 使用疑问句：使用疑问句能够引起读者的思考和好奇心，激发他们点击进一步了解。

## 以下是一些爆款标题中常见的关键词：
最强、绝了、神级、神器、史无前例、独此一家、首发、重磅……

## 规则
    1. 借鉴上面的技巧、关键词生成爆款标题
    2. 贴合用户的主题
    3. 每个标题前面加上emoji表情
    4. 标题给完之后，结合你对爆款标题的理解进行打分（1-5☆ 满分5☆）

## 约束条件:
    1.每次生成10个标题；
    2.标题字数控制在30字左右
    3.temperature=1.2

## 工作流程
    1. 针对用户给定的主题，创爆款标题。

## 初始化
作为角色 <Role>, 严格遵守 <Rules>, 使用默认 <Language> 与用户对话，友好的欢迎用户。然后介绍自己，并告诉用户 <Workflow>。

## 输出格式
只输出一个包含 10 个对象的 JSON 数组，不加问候语、解释或 Markdown 代码围栏。
每个对象包含 title（含 emoji 的标题字符串）和 score（1 到 5 的整数）。
单个对象示例：{"title": "✨ 这里是标题", "score": 5}
"""

ARTICLE_PROMPT = """
你是一名小红书文案作者。围绕用户提供的主题和选定标题，写一篇完整的中文文章。
开头直接切入主题，正文分段清晰，尽量提供具体、有用的内容，并兑现标题中的承诺。
只输出正文，不重复标题，不添加写作说明。
"""


def generate_text(client, system_prompt, user_prompt):
    completion = client.chat.completions.create(
        model="qwen3.8-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    response = completion.choices[0].message.content
    if not response or not response.strip():
        raise SystemExit("模型返回了空内容，请重新运行脚本。")
    return response.strip()


def parse_titles(response):
    # 有些回复仍会把 JSON 放在 Markdown 代码围栏里。
    lines = response.splitlines()
    if lines and lines[0] in ("```json", "```") and lines[-1] == "```":
        response = "\n".join(lines[1:-1])

    try:
        candidates = json.loads(response)
    except json.JSONDecodeError:
        raise SystemExit("标题结果不是有效的 JSON，请重新运行脚本。") from None
    if not isinstance(candidates, list) or len(candidates) != 10:
        raise SystemExit("模型没有返回 10 个标题，请重新运行脚本。")

    titles = []
    seen_titles = set()
    for candidate in candidates:
        if not isinstance(candidate, dict):
            raise SystemExit("标题结果格式有误，请重新运行脚本。")
        title = candidate.get("title")
        score = candidate.get("score")
        if not isinstance(title, str) or not title.strip():
            raise SystemExit("模型返回了空标题，请重新运行脚本。")
        if type(score) is not int or not 1 <= score <= 5:
            raise SystemExit("标题评分必须是 1 到 5 的整数，请重新运行脚本。")
        title = title.strip()
        if title in seen_titles:
            raise SystemExit("模型返回了重复标题，请重新运行脚本。")
        seen_titles.add(title)
        titles.append((title, score))
    return titles


def main():
    topic = input("请输入小红书文案主题：").strip()
    if not topic:
        raise SystemExit("主题不能为空，请重新运行脚本。")

    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://ws-bggm9k3qgbthz61a.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
    )
    titles = parse_titles(generate_text(client, TITLE_PROMPT, f"主题：{topic}"))

    print("\n生成的 10 个标题")
    for number, (title, score) in enumerate(titles, start=1):
        print(f"{number}. {title}（{score}/5☆）")

    while True:
        try:
            choice = int(input("\n请输入要写成文章的标题编号（1–10）："))
        except ValueError:
            choice = 0
        if 1 <= choice <= len(titles):
            break
        print("请输入 1 到 10 之间的整数。")

    title, _ = titles[choice - 1]
    article = generate_text(client, ARTICLE_PROMPT, f"主题：{topic}\n选定标题：{title}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output_path = Path(__file__).resolve().parent / f"小红书文案_{timestamp}.txt"
    with output_path.open("x", encoding="utf-8") as file:
        file.write(f"{title}\n\n{ar/ticle}\n")
    print(f"文案已保存到：{output_path}")


if __name__ == "__main__":
    main()
