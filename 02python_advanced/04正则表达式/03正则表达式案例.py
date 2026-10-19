import re
s1 = "_abc_2322ef"
# 字符串开头 第一位是大小写字母下划线取一个，后边跟着5-15位的单词字符结尾
print(re.findall(r"^[a-zA-Z_]\w{5,15}$",s1))

s2 = '100100120'
# 开头是一位数字然后后面跟着4到10位数字结尾
print(re.findall(r"^[1-9]\d{4,10}$",s2))


s3 = "12333@qq.com"
res = re.findall(r"^\w{5,10}@(163|qq|126)\.(?:com|cn)$",s3)
# findall() 发现正则里面有捕获分组 就只会返回括号里面匹配到的内容
# 捕获分组 就是正则当中用普通括号（......）包起来的部分
# 非捕获分组(?:.....)
print(res)

res1 = re.findall(r"\w{5,10}@(?:163|qq|126)\.(?:com|cn)$",s3)
print(res1)





