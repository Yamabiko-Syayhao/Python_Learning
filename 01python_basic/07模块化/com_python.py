# 自己封装了个小小的模块  主要是想实现求最大值 最小值 平均数
# def input_list(*numlist):
#     return (max(list(numlist)),min(list(numlist)),
#             sum(list(numlist)) / len(list(numlist)))

def max_num(val):
    return max(val)

def min_num(val):
    return min(val)

def avg_num(val):
    return sum(val) / len(val)



"""
     __name__ 是python中一个隐含的变量 代表的是当前模块的名字
     当模块被直接运行 那么 __name__ 的值就是__main__
     当模块被导入的时候 __name__ 的值为文件名
"""
# print(__name__, "__name__变量")



# 如果__name__的值等于__main__ 说明当前模块被直接运行，要去执行下边的代码 否则不执行
if __name__ == '__main__':
    print(max_num([10, 20, 30, 40, 50]))
    print(min_num([10, 20, 30, 40, 50]))
    print(avg_num([10, 20, 30, 40, 50]))
    print("模块被直接运行了")







