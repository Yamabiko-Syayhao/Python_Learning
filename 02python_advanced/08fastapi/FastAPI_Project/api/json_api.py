# 纯展示 不操作数据库 post/get/delete/put
from fastapi import APIRouter,Form,Depends
from pydantic import BaseModel
# 引入jwt验证
from utils.jwt import create_access_token
from utils.jwt import verify_token

# =========================== 路由配置 ===========================
# 创建一个路由实例 统一定义一些公共属性和行为
router = APIRouter(
    prefix="/api", # 接口前缀 所有的接口前边都要加上/api
    tags=["业务接口"], # 接口文档的分组标签   接口文档是为了给前端看
    responses={404: {"description": "找不到服务"}} # 统一定义一下默认的响应说明
    # 会给这个路由下的所有接口自动加上一个404的状态码说明
)

# =========================== 接口定义区域 ===========================
# post请求 form格式 需要uv add python-multipart
# 这个包下好了，不需要引入就能使用
# 请求头必须是application/x-www-form-urlencoded
@router.post("/login")
def post_login(userName: str = Form(),passWord: str = Form()): # 此处必须放Form进行接收
    if userName == "admin" and passWord == "1234":
        return {
            "code": 200,
            "msg":"登录成功",
            # 生成token
            "token": create_access_token({"sub": userName}), # 根据jwt里面定义的
            "userName":userName
        }
    else:
        return {
            "code": 201,
            "msg":"登陆失败！"
        }



# 定义json请求体模型 用于校验传进来的json格式
class UserData(BaseModel):
    userName: str
    passWord: str
# post请求 json格式 需要uv add python-multipart
# 这个包下好了，不需要引入就能使用

@router.post("/login_json")
def json_login(data:UserData):
    if data.userName == "admin" and data.passWord == "1234":
        return {
            "code": 200,
            "msg":"登录成功",
            "token": create_access_token({"sub": data.userName}),
            "userName":data.userName
        }
    else:
        return {
            "code": 201,
            "msg":"登陆失败！"
        }



# ========== 无参数的get请求 ==========
# 想给谁加上token的验证那么就给哪个函数加上参数user:str = Depends(verify_token)
@router.get("/site")
def get_site(user:str = Depends(verify_token)):
    return {
        "code": 200,
        "msg": "请求成功"
    }

# 退出登录
@router.get("/logout")
def logout(user:str = Depends(UserData)):
    return {
        "code": 200,
        "msg":"请求成功,登录状态已退出"
    }