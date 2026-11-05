# 由flask搭建的一个ai聊天接口后端服务
# 前端发个问题--》后端拿到前端传进来的数据（那个问题） 调阿里云百炼（通义千问）大模型---》把模型给的回复返回给前端
import os
from openai import OpenAI
# 引入flask -- 写接口
from flask import Flask,jsonify,request
# 引入cors -- 解决跨域
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://ws-wfyce58gddl4lglu.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

@app.route("/")
def home():
    return "hello word"

@app.route("/api/user",methods=['GET'])
def userfn():
    # 参数字段 content
    con = request.args.get("content")
    completion = client.chat.completions.create(
        model="qwen3.8-flash",
        messages=[
            {'role': 'system', 'content': '你是青岛百杉的一名讲师，帮助学员积累项目经验。'},
            {'role': 'user', 'content': con}
        ]
    )
    return jsonify({
        "msg":"请求成功",
        "data":completion.choices[0].message.content,
        "code":200
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)