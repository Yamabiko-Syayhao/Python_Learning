import ollama

# 文本对话
# res2 = ollama.chat(
#     model="qwen3.5:4b",
#     messages= [
#         {
#             "role": "user",
#             "content": "你是谁"
#         }
#     ],
#     think=False  # 显式关闭思考模式
# )
# print(res2)

# 向量模型
res = ollama.embed(
    model="bge-m3",
    input="青岛是一座美丽的城市"
)

print(res)
