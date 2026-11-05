# 由fastapi搭建的一个ai聊天接口后端服务
# 前端发个问题--》后端拿到前端传进来的数据（那个问题） 调阿里云百炼（通义千问）大模型---》把模型给的回复返回给前端
# 导入操作系统模块  在此用于读取环境变量（存放api_key密钥的）
import os
# 导入OpenAI客服端  阿里百炼兼容openai接口
from openai import OpenAI
# 引入FastAPI -- 写接口
from fastapi import FastAPI,HTTPException
# 引入跨域中间件  解决前端浏览器访问后端接口跨域问题
from fastapi.middleware.cors import CORSMiddleware
# 用于定义post接口请求体的数据模型 自动做参数校验
from pydantic import BaseModel
# 导入uvicorn 用来运行fastapi程序
import uvicorn

# 创建一个fastapi应用实例  设置接口文档标题和版本号
app = FastAPI(title="AI聊天接口",version="1.0")
# 添加跨域中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 实例化OpenAI客户端
client = OpenAI(
    # 读取环境变量中存放的api密钥
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 业务空间id要准确
    base_url="https://ws-wfyce58gddl4lglu.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

@app.get("/api/user")
def userfn(content:str):
    # try捕获异常  调用大模型时可能会有网络错误，key错误，模型错误等
    try:
        # 调用阿里百炼大模型对话接口
        completion = client.chat.completions.create(
            # 指定使用的模型名称deepseek-v4.1-flash-1017
            model="deepseek-v4.1-flash-1017",
            # 对话消息列表 system系统  user用户提问
            messages=[
                {'role': 'system', 'content': '你是青岛百杉的一名讲师，帮助学员积累项目经验。'},
                {'role': 'user', 'content': content}
            ]
        )
        # 返回json格式
        return {
            "msg": "请求成功",
            "data": completion.choices[0].message.content,
            "code": 200 #自定义状态码
        }
    except Exception as e:
        print(f"错误：{e}")
        # 抛出异常  返回500状态码 携带错误详情
        raise HTTPException(status_code=500,detail={"msg":f"AI调用失败{str(e)}","code":500})

# 定义post接口的请求体数据模型  校验传入的json参数
class chatReq(BaseModel):
    # content字段 用户输入的提问文本  fastapi会自动校验不为空
    content: str

@app.post("/api/chat")
def chat(req:chatReq):
    # try捕获异常  调用大模型时可能会有网络错误，key错误，模型错误等
    try:
        # 调用阿里百炼大模型对话接口
        completion = client.chat.completions.create(
            # 指定使用的模型名称deepseek-v4.1-flash-1017
            model="deepseek-v4.1-flash-1017",
            # 对话消息列表 system系统  user用户提问
            messages=[
                {'role': 'system', 'content': '你是青岛百杉的一名讲师，帮助学员积累项目经验。'},
                {'role': 'user', 'content': req.content}
            ]
        )
        # 返回json格式
        return {
            "msg": "请求成功",
            "data": completion.choices[0].message.content,
            "code": 200 #自定义状态码
        }
    except Exception as e:
        print(f"错误：{e}")
        # 抛出异常  返回500状态码 携带错误详情
        raise HTTPException(status_code=500,detail={"msg":f"AI调用失败{str(e)}","code":500})


if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=5000)