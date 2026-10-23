# 纯展示 不操作数据库 post/get/delete/put
from typing import Annotated
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

# ========== get请求有参数 ==========
@router.get("/getList")
def get_List(page:str,pageSize:str,user:str = Depends(verify_token)):
    return {
        "code": 200,
        "msg": "请求成功",
        "page": page,
        "pageSize": pageSize
    }


# ========== get请求有参数 路劲参数 ==========
@router.get("/list/{name}")
def get_List(name:str,user:str = Depends(verify_token)):
    return {
        "code": 200,
        "msg": "请求成功",

    }

# ========== post请求form形式 ==========
# 表单想用模型接收 必须写成Annotated[模型, Form()]
# 不能写data:Form() 那样Form()会被当成类型注解 启动直接报错
@router.post("/post_form")
def post_form(data:Annotated[UserData,Form()],user:str = Depends(verify_token)):
    userName = data.userName
    passWord = data.passWord
    if userName == "admin" and passWord == "1234":
        return {
            "code": 200,
            "msg":"请求成功",
            "userName":userName
        }
    else:
        return {
            "code": 200,
            "msg":"请求失败"
        }
# ========== post请求json形式 ==========
# json请求体直接用模型接收 不需要Annotated和Form()
@router.post("/post_json")
def post_json(data:UserData,user:str = Depends(verify_token)):
    userName = data.userName
    passWord = data.passWord
    if userName == "admin" and passWord == "1234":
        return {
            "code": 200,
            "msg":"请求成功",
            "userName":userName
        }
    else:
        return {
            "code": 200,
            "msg":"请求失败"
        }


# ========== put请求 ==========
# 定义put请求的json请求体模型 前端用application/json传参
# 注意id在模型里是str 前端必须传字符串"1" 传数字1会校验失败(422)
class PutData(BaseModel):
    id:str
    userName:str
@router.put("/put")
def put_List(data:PutData,user:str = Depends(verify_token)):
    # data是json请求体 不是查询参数
    # id为空给出提示 否则返回成功
    if not data.id:
        return {
            "code": 200,
            "msg":"缺少参数"
        }
    else:
        return {
            "code": 200,
            "msg": "成功",

        }


# ========== put请求-form写法 ==========
# 另一种写法：参数放在表单请求体里 不是json也不是查询参数
# 前端请求头必须是application/x-www-form-urlencoded
@router.put("/put_form")
def put_form(id:str = Form(),userName:str = Form(),user:str = Depends(verify_token)):
    if not id:
        return {
            "code": 200,
            "msg":"缺少参数"
        }
    else:
        return {
            "code": 200,
            "msg": "成功",

        }


# ========== delete请求有参数 ==========
# delete不用Form()取请求体 直接用查询参数 ?id=1
# 前端请求时把id拼在url上 请求头只需带token
@router.delete("/delete")
def del_form(id:str,user:str = Depends(verify_token)):
    if not id:
        return {
            "code": 200,
            "msg": "缺少必要参数",

        }
    else:
        return {
            "code": 200,
            "msg":"删除成功"
        }


# ========== delete请求有参数-form写法 ==========
# 参数放在表单请求体里 不再拼在url查询参数上
# 注意：DELETE带body部分浏览器/代理会丢弃 这里只为演示form写法
@router.delete("/delete_form")
def del_form_body(id:str = Form(),user:str = Depends(verify_token)):
    if not id:
        return {
            "code": 200,
            "msg": "缺少必要参数",

        }
    else:
        return {
            "code": 200,
            "msg":"删除成功"
        }
