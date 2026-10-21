"""
蓝图作用是将接口从入口文件中分离出来（把项目按照功能进行拆分模块化），这样做的目的是方便维护
让代码结构更清晰，方便维护
使用蓝图三步：创建蓝图--注册蓝图--访问接口

思路：
    1.引入flask 跨域插件
    2.用蓝图（blueprint）统一管理接口 给所有的接口统一加前缀/api
    3.处理跨域

什么是跨域？
    当前端页面去请求后端接口的时候，如果协议 域名 端口号 这三者中任一个不同，浏览器就认为是
    “跨域”请求
同源策略：两个url中协议 域名 端口 三者完全相同，才算同源，任一项不同 就是跨域
解决跨域的方法：前端解决 或 后端解决

"""
# 该文件就是要封装一个蓝图模块（接口定义）

# 1.引入蓝图类Blueprint,request接收前端传来的参数。render_template渲染模板文件
# 2.引入跨域插件 解决跨域用的7 uv add flask-cors （需要自己下）
from flask import Blueprint,request,render_template
from flask_cors import CORS
# 3.创建蓝图 用于把所有的接口进行统一管理
# 参数一：给蓝图起了一个名字
# 参数二：当前模块名 代表当前这个python所在的模块
# 参数三：给这个蓝图下面的所有接口统一加一个前缀
api_bp = Blueprint('api',__name__,url_prefix='/api')
# 4.给当前的蓝图启用跨域 这样后端就会在响应头里面加上 Access-Control-Allow-Origin:*
CORS(api_bp)


# -------------------- 1.首页 --------------------
@api_bp.route('/') # 写接口 首页
def miyako():  # put application's code here
    # return 'Hello World!'
    # 渲染html模板文件
    return render_template('index.html')

# -------------------- 2.get请求无参数 --------------------
@api_bp.route('/get',methods=['GET'])
def get_site():
    return {
        "msg":"请求成功",
        "code":200,
        "data":{
            "userName":"admin",
            "tel":"18364976570"
        }
    }

# -------------------- 3.get请求有参数 --------------------
@api_bp.route('/getList',methods=['GET'])
# http://127.0.0.1:5000/api/getList?userName=admin&passWord=123456
def get_List():
    # get请求 获取前端传来的数据 通过request.args.get()接收
    userName = request.args.get('userName')
    passWord = request.args.get('passWord')
    if userName == "admin" and passWord == "123456":
        return {
            "msg":"请求List成功",
            "code":200,
            "data":{
                "userName":userName,
                "passWord":passWord
            }
        }
    else:
        return {
            "msg": "请求失败",
            "code": 200,
            "data":{}
        }


# -------------------- 4.get请求有参数 --------------------
# http://127.0.0.1:5000/api/list/arl/1234
# 通过路径中的<参数>接收 函数接收形参 路径参数需要把参数写在路径当中
@api_bp.route('/list/<userName>/<pwd>',methods=['GET'])
def get_lists(userName,pwd):
    return {
        "msg": "请求List成功",
        "code": 200,
        "data": {
            "userName": userName,
            "passWord": pwd
        }
    }

# -------------------- 5.post请求-form --------------------
# 获取post请求参数 request.form.get
# 请求头类型 applicaation/x-www-form-urlencoded
# 请求实例：http://127.0.0.1:5000/api/form 请求头 传参body
@api_bp.route('/form',methods=['POST'])
def post_form():
    userName = request.form.get('userName')
    passWord = request.form.get('passWord')
    if userName == "admin" and passWord == "123456":
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

# -------------------- 6.post请求-json --------------------
# 请求头类型 applicaation/json
# 请求实例：http://127.0.0.1:5000/api/data 请求头 传参body
@api_bp.route('/data',methods=['POST'])
def post_data():
    # 核心 解析json请求体 获取以json形式传进来的参数
    # silent = True 避免解析失败的时候抛出错误
    data = request.get_json(silent = True)
    # 如果没有参数
    if not data:
        return {
            "error":"缺少必要参数"
        }
    # 如果参数存在 需要解析具体的参数
    userName = data.get('userName')
    eat = data.get('eat')
    return {
        "code": 200,
        "userInfo":{
            "userName":userName,
            "eat":eat
        }
    }




# -------------------- 7.put请求-json --------------------
# 请求头类型 application/json
# 请求实例：http://127.0.0.1:5000/api/put 请求头 传参body
@api_bp.route('/put',methods=['PUT'])
def put_data():
    # 获取json请求体 这里只演示接收参数和返回数据
    data = request.get_json(silent = True)
    if not isinstance(data,dict):
        return {
            "code":400,
            "msg":"请传入JSON对象"
        },400 # 括号外的400表示给外面设置真正的http状态码，如果不设置走到这一步外面仍是200
    # return 返回内容, HTTP状态码
    # 如果参数正确 需要解析具体的参数
    userId = data.get('id')
    userName = data.get('userName')
    eat = data.get('eat')
    if userId is None or userName is None or eat is None:
        return {
            "code":400,
            "msg":"缺少必要参数"
        },400
    return {
        "code":200,
        "msg":"PUT请求成功",
        "data":{
            "id":userId,
            "userName":userName,
            "eat":eat
        }
    }

# -------------------- 8.delete请求-json --------------------
# 请求头类型 application/json
# 请求实例：http://127.0.0.1:5000/api/delete 请求头 传参body
@api_bp.route('/delete',methods=['DELETE'])
def delete_data():
    # 获取json请求体 这里只演示接收参数和返回数据
    data = request.get_json(silent = True)
    if not isinstance(data,dict):
        return {
            "code":400,
            "msg":"请传入JSON对象"
        },400
    userId = data.get('id') # 后端要的字段
    if userId is None:
        return {
            "code":400,
            "msg":"缺少必要参数"
        },400
    return {
        "code":200,
        "msg":"DELETE请求成功",
        "data":{
            "id":userId
        }
        # 如果在真实开发里面，这里应该执行数据库的删除
    }

# get请求 主要用于查询 分页查询
# post请求 主要用于登录 注册 添加
# put请求用于修改
# delete请求用于删除