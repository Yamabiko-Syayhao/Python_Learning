# 引入json模块
import json

'''
json字符串是一种数据结构，其实就是个字符串，是一种有规律的字符串，内部是字典
json字符串===>里边的字典属性和属性值必须用双引号

'''
json_str = '{"name":"阿拉蕾","age":"16","sex":"女"}' # 这是一个字符串！
# 因为里面都必须有双引号，所以为了防止出错，外层必须要是单引号
print(json_str, type(json_str))


# 1.把json字符串转成字典的形式
dict1 = json.loads(json_str)
print(dict1, type(dict1))

json_dict = {"name":"律","age":"16","sex":"female"}
print(json_dict, type(json_dict))

# 2.字典转为json字符串
str1 = json.dumps(json_dict, ensure_ascii=False) # 把u编码转换成中文，假如没有
# 这一步会直接输出汉字的u编码
print(str1, type(str1))





