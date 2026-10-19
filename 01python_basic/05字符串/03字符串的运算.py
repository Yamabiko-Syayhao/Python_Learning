a = "还有十一天放假"
# len()方法 获取这个字符串的长度 一共有多少个字符
print(len(a))
# 循环获取每个字符
for i in range(len(a)):
    print(f"{a[i]}-{i}",end="")
print("")

# 这个字符串是否在a字符串中
print("十" in a)
# 这个字符是否不在a字符串中
print("十" not in a)

# 字符比较大小 比较的是ASCII码的值 是一个字符一个字符的对比
print(a > "abc")

# 查看ASCII码的值 ord()方法
print(ord("a"))
print(ord(a[6]))






