"""
正则表达式是用一套特殊的语法写出来的“字符串模板”，用来判断某个字符串是否符合该模板的要求
或者是从字符串中提取/替换复合模板的部分

"""
import re

s1 = "abcabcpython9python9python"
# match()从字符串开头匹配第一个 找到返回对象 找不到返回None 注意只匹配开头
result1 = re.match("python", s1) # <re.Match object; span=(0, 3), match='abc'>

print(result1) # 这个会返回None 因为开头是abc...和python不匹配
# 假如result1 = re.match("abc", s1) 就会返回对象，因为abc和字符串开头的abc...匹配

# search()全文匹配第一个 找到返回对象 找不到返回None
s2 = "abcpythonpy999"
result2 = re.search("py", s2)
print(result2)

# findall() 找到所有的匹配项 返回列表 没有匹配项返回空列表
result3 = re.findall("py", s2)
print(result3)

s3 = "abcpython999"
# fullmatch() 整个字符串必须完全一模一样匹配才行 那样才会返回对于的对象
result4 = re.fullmatch("abcpython999", s3)
print(result4)







