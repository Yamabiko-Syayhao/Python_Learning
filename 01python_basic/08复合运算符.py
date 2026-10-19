# 复合运算符 +=  -=  *=  /=  %=   //=  **=
"""
    a+=b   ===>  a=a+b
    a-=b   ===>  a=a-b
    以此类推
    a//=b   ===>  a=a//b
    a**=b   ===>  a=a**b
"""
a = 5
b = 3
a += b
# 相当于a = a+b =8
print(a,b)

a *= b + 2
# 相当于a = a*(b+2) = 8*5 = 40
print(a,b)

x = 11
x %= 2 * 4
print(x)