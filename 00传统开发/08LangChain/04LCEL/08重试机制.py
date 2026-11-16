from os import name

from langchain_core.runnables import RunnableLambda
# 自定义异常类 是整个重试机制的“开关” 如果是别的异常不会触发重试
class NetError(Exception):
    """
    网络波动异常
    """
# 全局计数器 统计接口调用了多少次
count = 0

def call_api(input_msg):
    # 声明要修改的是全局变量
    global count
    count += 1
    print(f"第{count}次发起请求")
    # 第一层访问 手动抛出错误
    if count == 1:
        raise ValueError("网络抖动，请求失败")
    # 第二次执行 正常返回结果
    return {
        "result": "接口调用成功",
        "msg":input_msg
    }

# 配置重试
api_run = RunnableLambda(call_api).with_retry(
    retry_if_exception_type=(NetError,ValueError),  # 哪些异常才重试 限定只有NetError才会重试
    stop_after_attempt = 3, # 最大尝试总次数
    wait_exponential_jitter=False, # 重试等待多久 False 关闭延时等待 立刻重试
)

if __name__ == "__main__":
    try:
        count = 0
        res = api_run.invoke("测试请求")
        print(res)
    except Exception as e:
        print("捕获到了不重试的异常，请求失败",e)


