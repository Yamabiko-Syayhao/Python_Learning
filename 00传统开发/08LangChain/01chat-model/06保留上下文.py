"""
system:底层提示词
user:用户提示词
assistant:AI回复的内容
"""


messages = [
    {"role":"system","content":"你是一个过目不忘的记忆之神，跟你说一遍就能记住"},
    {"role":"user","content":"你是arl,是梦限大的主唱"},
    {"role":"assistant","content":"我叫阿拉蕾，是梦限大的主唱"},
    {"role":"user","content":"你是谁？"},

]

from utils.llm import chat_prompt
res = chat_prompt(messages)
print(res.content)