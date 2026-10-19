import re
# ============== 1.基础的元字符：数字 单词字符 ==============
# r原始字符 这里的作用是关闭python当中的反斜杠\转义功能
s1 = "pyThon123py999asd-01234zxc"
# \d匹配单个数字 等价于[0-9]
result1 = re.search(r"\d", s1)
print(result1)

result2 = re.search(r"[0-9]", s1)
print(result2)

print(f"匹配的内容是：{result1.group()}")
print(f"匹配的下标区域是：{result1.span()}")

# [a-z] 匹配字母
print(re.search(r'[a-z]',s1))# 匹配小写字母
print(re.search(r'[A-Z]',s1)) # 匹配大写字母

# \w 用于匹配字母、数字和下划线 而 \W 是用于非字母、数字、下划线
s2 = "asd123_666-g$123&123a"
result3 = re.findall(r"\w",s2)
print(result3)

result3 = re.findall(r"\W",s2)
print(result3)

# 量词 + 匹配多个连续的字符 {n}匹配n个
# 查找连续的数字
result5 = re.findall(r'\d+',s2)
print(result5)

# 查询连续的三个数字
result6 = re.findall(r'\d{3}',s2)
print(result6)

# 查询连续两个数字
result6 = re.findall(r'\d{2}',s2)
print(result6)

#查询连续的三个字母
result7 = re.findall(r'[a-z]{3}',s2)
print(result7)

#查询连续的两个字母
result8 = re.findall(r'[a-z]{2}',s2)
print(result7)

#查询连续的字母
result9 = re.findall(r'[a-z]+',s2)
print(result9)


# ============== 2.边界符 ^ $ \b ==============
s3 = """
    abcdefg@163.com,
    asdfghjklasd@163.com,
    ab@163.com,
    _123123ab@163.com1
"""
# ^规定位置 必须从字符串开头开始
# 在字符串的开头位置上必须是一个小写字母 后边跟着5-17位单词字符 然后跟着@163.com
print(re.findall(r"^[a-z]\w{5,17}@163.com",s3))
# 一个小写字母 后边跟着5-17位单词字符 然后跟着@163.com
print(re.findall(r"[a-z]\w{5,17}@163.com",s3))
# {5,17} 是匹配长度为5~17位的字母或数字或下划线

# $匹配字符串的结尾
print(re.findall(r"[a-z]\w@163.com\d$",s3))
# 会从匹配到的后面开始，看末尾是不是符合@163.com\d （即@163.com加一个数字）

# \b 单词边界（\w和\W或者字符串边缘之间） 匹配的是位置 不是字符，本身不消耗任何字符
# 你可以把他理解为单词字符和非单词字符之间的分界线 或者是单词字符和字符串边缘之间的分界线
s4 = "cat cats test-cat 123catcat123"
res = re.findall(r"\bcat\b",s4)
print(res) # 其中第一个cat左边没有东西，右边是空格，所以两边都是非单词字符，这里就有了
# 一个单独cat,就符合设置的边界\bcat\b

# ============== 3^放在[]里面为取反 ==============
s5 = "123457asd"
print(re.findall(r"[^a-z]",s5)) # 取字母的相反 那么这里就是数字

# ============== 4 | 或分支 ==============
"""
这个正则有二部分 用|分开 |表示或者
匹配下边三种之一
[1-9]?反斜杠d$
100
200
"""
res1 = re.match(r"[1-9]?\d$|100|200","101")
print(res1) #None

re2 = re.match(r"[1-9]?\d$|1[0-9]{2}|200","101")
print(re2) # <re.Match object; span=(0, 3), match='101'>

res3 = re.match(r"\w{4,10}@(163|qq|126).com","test_es@qq.com")
print(res3)

