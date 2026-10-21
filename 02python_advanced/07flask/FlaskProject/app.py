# 1. 引入flask框架
from flask import Flask
# 2.从接口文件中引入定义好的蓝图 目的是为了在入口文件中注册蓝图
from api.json_api import api_bp
app = Flask(__name__) # 3.创建应用实例 使用flask
app.json.ensure_ascii = False # 让json直接输出中文
# 4.注册蓝图 把分离出去的所有接口 注册在主应用上，让入口文件能找到所有的接口
app.register_blueprint(api_bp)



if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0',port=5000,debug=True)
    # debug=True 开发模式 修改完代码自动重启 只要别动端口号就可以不用手动重启