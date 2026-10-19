strs = "月亮不睡你不睡，你是一个秃头小宝贝"
# index方法 查找字符串中是否有这个字符，找到返回下标，找不到报错
# 这个方法可以在列表、元组、字符串都能用
print(strs.index("月"))
# print(strs.index("周"))

# find方法 在字符串中查找子字符串或者元素的位置，找到返回下标，
# 但是find方法只能在字符串用
# 找不到返回-1
print(strs.find("月"))
print(strs.find("周"))

print("="*30)

# split()方法  根据字符串中的字符将字符串分割成列表
str1 = "青岛-百杉-智能-科技-有限-公司"
print(str1.split("-")) # 根据 - 去吧字符串分割成列表

str4 = "byeyyy2026ysamey0y9y"
print(str4.split("y"))




# partition)() 把字符串 根据第一个出现的分隔符切成三部分，返回一个元组（
# 分隔符前边、分隔符本身、分隔符后边）
# 它的返回值永远都是长度为3的元组
print(str1.partition("-"),"partition方法实例") # ('青岛', '-', '百杉-智能-科技-有限-公司')

print("="*30)

# 把列表list1里面的元素变回str1那种字符串形式，关键在于去掉最后一个-
list1 = ['青岛', '百杉', '智能', '科技', '有限', '公司']

# 方法1
for j in list1:
    print(j + "-", end="")
print("\b")

# 方法2
str2 = ""
for item in list1:
    str2 += item + '-'
print(str2[:-1])

# join() 方法，将列表通过某种符号转换为字符串 “符号”.join(列表)

# 方法3
print("-".join(list1),"join方法实例")

# replace() 用新数据去替换旧数据 字符串.replace(旧数据, 新数据)
str3 = "阿拉蕾平常的爱好是，唱歌说话魔法露露"
print(str3.replace("唱歌", "蜜瓜包"))
# 这里的话把原字符串里面的唱歌替换为了“蜜瓜包”

print(30 * "=")
a = " hello world "
b = "BYESAME"
c = "hello"
print(a.upper()) # 大写转换
print(b.lower()) # 小写转换
print(c.capitalize())  # 首字母大写
print(c.title())  # 每个单词首字母都大写
print(a.strip(), "777") # 去掉前后空格
print(a, "888")
print(a.count("l")) # 检测l在字符串中出现的次数

print(a.strip().startswith("he"))
print(a.startswith("he")) # 检测字符串a是否以字符“he”开头
print(a.endswith("ld")) # 检测字符串a是否以“ld”结尾
print(a.isalpha()) # 检测字符串中是否全是字母 大小写均可

# 由于字符串a里面开头结尾都是空格，且其中中间还含有空格，所以全输出False

print(c.isdigit()) # 检测字符串中是否全为数字
print(c.isalnum()) # 检测字符串中是否全为字母或数字
print(c.isupper())  # 检测是否全为大写
print(c.islower())  # 检测是否全为小写
print(c.istitle()) # 检测是否每个单词首字母都是大写




