# JWT（JSON WEB TOKEN） token可以理解为一个"通行证" 令牌
# 基于fastapi和python-jose 实现jwt认证
from jose import JWTError,jwt
# 引入时间模块 用于设置过期时间
from datetime import datetime,timedelta,timezone
# Request 获取前端发来请求的信息，HTTPException 抛出错误
from fastapi import Request,HTTPException

# JWT 核心配置
# 密钥 用来签名和验证token 绝不能泄露 自己随机写的字符串 越复杂越安全
SECRET_KEY = "you-secret-key-it-safe-never-leak"
# 加密算法 固定使用HS256 对称加密（加密解密都用同一个密钥）
ALGORITHM = "HS256"
# 过期时间（分钟） 60*24=1天
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24


# =============== token工具函数 ===============
# 创建token 用户登录成功之后调用该方法生成token
def create_access_token(data: dict):
    # 复制一份传入的数据避免修改原数据
    to_encode = data.copy()
    # 设置过期时间 用当前时间+过期的有效时长
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # 将过期时间存入传入来的数据当中
    to_encode.update({"exp": expire})
    # 加密生成token
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

# 验证token 解密
def verify_token(request: Request):
    # 从请求头当中获取token 前端页面 headers:{"token":"xxxxxxx"}
    token = request.headers.get("token")
    if not token: # 前端没有传入token
        # 抛出错误 status_code 401 未认证
        raise HTTPException(status_code=401, detail="Token is invalid")
    try:
        # 解密token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # 取出来userName sub是jwt规范当中的主体字段
        userName:str = payload.get("sub")
        if userName is None:
            raise HTTPException(status_code=401, detail="invalid token")
        else:
            return userName
    # token过期 被篡改
    except JWTError:
        raise HTTPException(status_code=403, detail="token was expired")