# 这组接口准备操作数据库
from fastapi import APIRouter,Form,Depends,HTTPException
from pydantic import BaseModel
# 数据库配置---> 连接数据库 ----> 导入模型类 ----> 事务 ---> 写接口 ---> 前端调接口
# 引入模型类
from model.student import StuModel
from model.user import UserModel
from model.role import RoseModel
# 引入事务
from utils.mysql_config import db
# 引入jwt验证
from utils.jwt import create_access_token
from utils.jwt import verify_token

# =========================== 路由配置 ===========================
# 创建一个路由实例 统一定义一些公共属性和行为
router = APIRouter(
    prefix="/apiServer", # 接口前缀 所有的接口前边都要加上/api
    tags=["业务接口"], # 接口文档的分组标签   接口文档是为了给前端看
    responses={404: {"description": "找不到服务"}} # 统一定义一下默认的响应说明
    # 会给这个路由下的所有接口自动加上一个404的状态码说明
)

# =========================== 写接口 ===========================
# 创建一个路由实例 统一定义一些公共属性和行为
# =========== 添数据form格式 ===========
@router.post("/add")
def add(userName:str = Form(),english:str = Form(),python:str = Form(),java:str = Form(),user=Depends(verify_token)):
    # 将用户提供的内容 添加数据库中
    # 构建ORM 实例化对象
    new_Stu = StuModel(
        userName=userName,
        english=english,
        python=python,
        java=java
    )
    try:
        # 添加到对话
        db.add(new_Stu)
        # 提交事务
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500,detail="添加失败")
    # 关闭连接
    db.close()
    return {
        "code": 200,
        "msg":"添加成功"
    }

# =========== 添数据json格式 ===========
class TableData(BaseModel):
    userName: str
    english: int
    python: int
    java: int
@router.post("/dataBase")
def add_table_data(data:TableData,user:str=Depends(verify_token)):
    # 构建ORM 实例化对象 pydantic模型不能直接加进数据库
    new_Stu = StuModel(
        userName=data.userName,
        english=data.english,
        python=data.python,
        java=data.java
    )
    try:
        # 添加到对话
        db.add(new_Stu)
        # 提交事务
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500,detail="添加失败")
    # 关闭连接
    db.close()
    return {
        "code": 200,
        "msg":"添加成功"
    }

# =========== 删表格json格式 ===========
class DeleteData(BaseModel):
    id:int
@router.delete("/delete_data")
def delete_data(data:DeleteData,user:str=Depends(verify_token)):
    stu = db.get(StuModel,data.id)
    if not stu:
        return {
            "code": 200,
            "msg": "数据不存在"
        }
    try:
        db.delete(stu)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500,detail="删除失败")
    db.close()
    return {
        "code": 200,
        "msg":"删除成功！"
    }

# =========== 删表格form格式 ===========
@router.delete("/del_data")
def del_data_form(id:int = Form(),user:str=Depends(verify_token)):
    # 先去查询是否有这条数据
    test = db.query(StuModel).filter_by(id = id).first()
    if test:
        db.delete(test)
        db.commit()
        db.close()
        return {
            "code": 200,
            "msg":"删除成功"
        }
    else:
        return {
            "code": 200,
            "msg":"数据未找到"
        }

# =========== 查询 ===========
@router.get("/user_role")
def get_user_role(user=Depends(verify_token)):
    data = db.query(
        UserModel.id,
        UserModel.userName,
        UserModel.role_id,
        RoseModel.roleName

    ).join(RoseModel,UserModel.role_id==RoseModel.id).all()
    # 定义空列表 存放组装完成返回的数据
    res_list = []
    for row in data:
        # 将row对象转为普通python字典
        d = row._asdict()
        # 转换字典方便访问
        res_list.append({
            "id":d["id"],
            "userName":d["userName"],
            "roleId":d["role_id"],
            "roleName":d["roleName"]
        })
    db.close()
    return {
        "code": 200,
        "msg":"查询成功",
        "data":res_list
    }


"""
注 ： 重点复习数据库操作 和这里的接口调用还有前后端连接

"""