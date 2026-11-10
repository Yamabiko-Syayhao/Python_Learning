# 核心链子: 前端发起提问--->查询数据库--->拼接提示词--->调大模型---->返回回答

# 导入操作系统模块  在此用于读取环境变量（存放api_key密钥的）
import os
# 导入OpenAI客服端  阿里百炼兼容openai接口
from openai import OpenAI
# 引入FastAPI -- 写接口
from fastapi import FastAPI
# 引入http状态码
from fastapi.responses import JSONResponse
# 引入跨域中间件  解决前端浏览器访问后端接口跨域问题
from fastapi.middleware.cors import CORSMiddleware
# 导入uvicorn 用来运行fastapi程序
import uvicorn
# 1.导入pymysql
from pymysql import *

# 创建一个fastapi应用实例  设置接口文档标题和版本号
app = FastAPI(title="AI聊天接口",version="1.0")
# 添加跨域中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # 允许所有来源域名访问，生产环境建议指定具体域名
    allow_credentials=True,       # 允许携带cookie凭证
    allow_methods=["*"],          # 允许所有http请求方法：GET POST PUT DELETE等
    allow_headers=["*"],          # 允许前端传递所有请求头
)
# 查询数据库 表  数据
def query_address_table():
    conn = None
    cur = None
    try:
        # 2.创建数据库连接
        conn = connect(host="localhost",port=3306, user="root", password="352130789Slh", database="fastapiwebadmin", charset="utf8")
        # 3.打开游标--打开数据库
        cur = conn.cursor()
        # 4.执行sql语句
        sql = "select * from mal_address"
        cur.execute(sql)
        # 5.获取全部查询结果
        result = cur.fetchall()
        return result
    except Exception as e:
        print(f"查询数据库异常:{str(e)}")
        # 如果查询出错 返回空数据
        return []
    finally:
        # 数据库连接成功
        if conn:
            # 关闭游标----关闭数据库
            cur.close()
            # 关闭连接
            conn.close()

# 实例化OpenAI客户端
client = OpenAI(
    # 读取环境变量中存放的api密钥
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 业务空间id要准确
    base_url="https://ws-bggm9k3qgbthz61a.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

#定义历史对话
messages = [{"role":"system","content":"你是basemall商城专属客服,你叫小base!"}]

#接口
@app.get("/api/ai")
def aiopen(content:str):
    # 全局变量
    global messages
    # 如果content没有  则说明前端没有发送该参数  那么报400状态码 并返回消息
    if not content:
        return JSONResponse(content={"error":"缺少content参数"},status_code=400)
    # 去掉前后空格
    content = content.strip()
    # 如果前端发送q/Q那么清空上下文
    if content.lower() == 'q':
        messages = [{"role":"system","content":"你是basemall商城专属客服,你叫小base!"}]
        return {"data":"对话已重置","code":200}
    # =======================核心逻辑=========================
    # 1.1查询数据库
    db_result = query_address_table()
    # 1.2拼接提示词
    prompt_template = f"""
    [参考数据]
    {db_result}
    [用户问题]
    {content}
    [要求]
    基于上边给的参考数据回答用户的问题,语气幽默一些,不要编造数据,如果数据里边没有相关信息要如实告知用户,输出的格式是纯文本格式,不要带***等特殊字符
    """
    # 3.去掉提示词前后空白
    final_user_prompt = prompt_template.strip()
    # 将对话列表备份一份 不要在原数据中操作
    original_messages = messages.copy()

    # try捕获异常  调用大模型时可能会有网络错误，key错误，模型错误等
    try:
        # 封装消息结构
        user_message = {"role":"user","content":final_user_prompt}
        # 将用户提示词添加到消息列表中
        messages.append(user_message)

        # 调用阿里百炼大模型对话接口
        completion = client.chat.completions.create(
            # 指定使用的模型名称deepseek-v4.1-flash-1017
            model="qwen3.8-flash",
            # 对话消息列表 system系统  user用户提问
            messages=messages
        )
        # 拿到AI返回的结果
        assistant_reply = completion.choices[0].message.content
        return {
            "data":assistant_reply,
            "status":200
        }
    except Exception as e:
        print(f"错误：{e}")
        # 返回给前端错误信息  返回500状态码 携带错误详情
        return JSONResponse(content={"error":f"AI调用失败{str(e)}"},status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)