from config import DASHSCOPE_API_KEY,DASHSCOPE_BASE_URL
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate, load_prompt
# dumpd load
from langchain_core.load import dumpd, load
# ChatOpenAI走的是openAI兼容协议 一个模型只有有对应的openai兼容接口的时候才能使用

#  ======= 1创建提示词模板 =======
prompt = PromptTemplate.from_template("你是一名{goods}鉴定师，帮我识别它的{function}")
print(prompt,type(prompt),"提示词模板")
# ======= 2模板对象 ---> 字典 =======
dict_res = dumpd(prompt)
print(dict_res,type(dict_res),"对象转字典")

# 3存入本地文件夹text/t1.json
import os
import json
# 确保text目录是存在的， 因为open不会去自动创建目录
os.makedirs("text", exist_ok=True)
with open("text/t1.json", mode = "w", encoding="utf-8") as f:
    # json.dump 字典--->写入json文件
    # false 中文原样保存
    # indent用于缩进 ，2缩进两个空格，4缩进4个空格
    json.dump(dict_res, f, ensure_ascii=False, indent=4)

print("文件已存入")

# 4读取json文件 还原成普通的字典
with open("text/t1.json", mode = "r", encoding="utf-8") as f:
    json_data = json.load(f)

# 5把字典转为langchain对象 allowed_objects是一个安全白名单 防止构造出任意对象
loaded_prompt = load(json_data,allowed_objects=[PromptTemplate])
print(loaded_prompt,"提示词模板")

# 6根据提示词模板填充变量
final_prompt = loaded_prompt.invoke(
    {
        "goods":"汉堡",
        "function":"成分"
    }
)


# 初始化客户端
# 设置初始化 后续调大模型
llm = init_chat_model(
    # qwen3.8-flash
    model = "qwen3.8-flash",
    api_key = DASHSCOPE_API_KEY,
    base_url = DASHSCOPE_BASE_URL,
    model_provider = "openai"

)

res = llm.invoke(final_prompt)
print(res.content)
