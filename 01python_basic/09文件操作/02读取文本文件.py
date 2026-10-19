# 找到utils文件夹中的wenben.txt文件 并读取内容


'''
读取文本语法
    open(file="文件", mode="模式", encoding="编码格式"))

    model:
        r：只读，不能写入 文件必须存在 否则会报错
        w：不能读 可写入 文件存在--清空 文件不存在--创建
        a：文件存在--在文件末尾加内容 文件不存在--创建
        r+：读写 文件必须存在 写入文件会覆盖原有
        w+：读写
        a+：追加+可读 写入永远在末尾

'''
import sys
print(sys.getdefaultencoding(),"获取当前编码格式")

f = None
try:
    f = open(file = "utils/wenben1.txt", mode = "r", encoding = "utf-8")
    # f.read() 读取所有内容
    # print(f.read())
    print(f.readline())

except Exception as e:
    print(f"读取失败了{e}")
finally:
    # 因为一开始f定义的初始值就算None，只有open成功过，f才会是个文件对象，才能调用close()
    if f is not None: # f起初返回就是None，如果没有被后面open成功，如果open成功就会不是
        # None 就可以满足下面的if条件
        f.close()

# 操作完必须关闭文件



a = [[1,2,3],[4,5,6],[7,8,9]]
print(a)

