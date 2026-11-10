# 根据用户输入的题目生成10个标题,然后让用户选择其中的某个标题,根据这个标题再生成文章,最周把生成的内容放在txt文件
import os
from openai import OpenAI

# 系统提示词
system_prompt = """
    # 角色: 爆款标题生成器
    ## 简介
    - 你是一个爆款标题生成器，主要工作，是帮助公众号,小红书,头条文章产出能够刺激用户打开的爆款标题。

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
"""

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 调用的时候将{WorkspaceId} 替换为真实的业务空间id
    base_url="https://ws-wfyce58gddl4lglu.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
# 模型
MODEL = "glm-5.3"


def chat(messages):
    # 封装了一次模型调用 返回文本内容
    res = client.chat.completions.create(model=MODEL, messages=messages)
    return res.choices[0].message.content


def main():
    # 1.收集一下用户的主题
    topic = input("请输入你的小红书主题: ").strip()
    # 判断用户输入的主题是否为空
    if not topic:
        print("主题不能为空!!,退出")
        return
    # 组装消息列表  维护完整上下文
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"我的主题是{topic}\n,请按照流程帮我创作10个标题"},
    ]
    # 2.根据用户输入的主题 生成10个标题
    try:
        titles_text = chat(messages)
    except Exception as e:
        print(f"模型调用失败,{e}")
        return

    print(f"为你生成的10个标题: \n")
    print(titles_text)

    # 将模型的回复 写入历史  保证后续 可以"记住"标题
    messages.append({"role": "assistant", "content": titles_text})

    # 3.用户选择标题
    while True:
        choice = input("\n请选择你要创作的正文的标题(输入序号,输入q表示退出): ").strip()
        if choice.lower() == "q":
            print("已退出!")
            return
        if not choice:
            print("序号还没选择呢老六,请重新输入")
            continue
        # choice.isdigit() 判断字符串是否是纯数字  测试一下！！！
        if choice.isdigit() and 1 <= int(choice) <= 10:
            break
        # 上边的choice 用户输入的不符合要求  给用户提示一下  让用户直接输入选择的标题序号
        print("请输入1-10之间的序号(或者输入q直接示退出)")

    # 4.根据用户选择的标题生成正文
    messages.append({"role": "user",
                     "content": f"我选择第{choice}个标题，请严格按照这个标题创作跟他相关的内容，遵循原文创作原则（100-500字之间）"})
    try:
        body_text = chat(messages)
    except Exception as e:
        print(f"模型调用失败,{e}")
        return

    print(f"正文: \n")
    print(body_text)

    # 5.保存结果
    save = input("\n是否要保存文件？(Y/N): ").strip().lower()
    if save == "y":
        fileName = f"xiaohongshu_{topic[:10]}.txt"
        with open(fileName, "w", encoding="utf-8") as f:
            f.write(f"主题：{topic}\n\n 标题\n{titles_text}\n\n 选中标题的序号\n{choice}\n\n 正文内容\n{body_text}\n")
        print(f"文件已经保存到{fileName}")


if __name__ == "__main__":
    main()