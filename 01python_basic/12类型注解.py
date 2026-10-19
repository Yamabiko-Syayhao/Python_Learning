# python类型注解（类型提示）
# 变量:类型 = 值

# 此处的:int 这部分就叫做【类型注解】
# 提示变量a应该存一个整数
a:int = 1
# 会有警告 但是代码可以正常运行  a变成字符串
a = "hello"
# python解释器运行的时候不会去强制校验类型，不会阻止你赋值别的类型
print(a)
print(type(a))

# 动态类型语言 python
# 静态类型语言 java/c/ts