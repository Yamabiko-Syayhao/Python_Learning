# 导入fastapi模块
from fastapi import FastAPI
# 导入跨域中间件解决跨域报错
from fastapi.middleware.cors import CORSMiddleware
# 引入自定义的路由模块
from api.json_api import router as api_router

# 创建了一个fastapi实例，相当于启动了一个后端服务
app = FastAPI()

# 配置跨域中间件，允许前端页面访问后端接口，允许浏览器从其他的端口/域名的前端页面来请求
# 你的fastapi的后端
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 允许哪些来源来访问  *代表任何来源都允许
    allow_credentials=True, # 允许携带“凭证” 凭证指的是cookie token请求头等等
    # 能证明你身份的东西，设置为True就证明允许携带
    allow_methods=["*"], # 允许哪些http请求方法 *代表允许哪些请求方法
    allow_headers=["*"] # 允许前端带哪些 自定义 的请求头 （比如token请求头）
)

# 将定义好的路由文件 放在fastapi的实例上
# 将json_api中左右的接口放在主应用上
app.include_router(api_router)


# 下边俩就是要写的接口    "/" 就是默认打开的内容
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}



if __name__ == "__main__":
    # 引入异步的web服务器 用来运行fastapi框架
    import uvicorn
    # main:app 固定写法 代表的是当前文件的app实例
    # host = "0.0.0.0" 允许本机+局域网下其他设备访问
    # 访问不了就改成localhost
    # port = 8000 端口号
    # reload = True 修改代码自动重启服务
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)