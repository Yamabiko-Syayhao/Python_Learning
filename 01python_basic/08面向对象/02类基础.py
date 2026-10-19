'''
用class去创建类

语法
    class 类名：
        def __init__(self, 参数):
            self.属性 = 参数
        def 实例方法(self):
            自己的逻辑/pass

实例化对象（通过上面写的类去创建一个对象）
    类的名字(参数)
'''
# 定义一个类
class Car: # 类的名字习惯用大驼峰
    def __init__(self, name, color, price): # self 就是当前对象
        #
        # __init__ 构造方法，或者叫初始化方法 在你实例化对象的时候就已经调用了
        # 第一个参数的self是固定的，代表的是当前的对象，调用的时候不用手动传
        self.name = name
        self.color = color
        self.price = price
    def start(self):
        print(f"{self.name}www")

# 实例化对象（通过上门的类去造的车）
car1 = Car("宝马", "黑色", 1000)
car2 = Car("奔驰","白色",100)
car3 = Car("宝马","黑色",1000)
print(car1) # 直接输出car1会返回 <模块名.类名 object at 内存地址>
'''
__main__：定义该类的模块（这个类写在主脚本里，所以是 __main__）。                   
Car：类名。                                                                         
0x...：对象在内存中的地址（十六进制），每次运行都可能不同。
'''

print(car2)

# 以下的会打印出False car3 == car1返回False 因为他们两个car1 car3是完全不同的对象。
# 每次调用Car()都会产生一个全新的对象，内存地址不同
print(car3 == car1)

# 函数和方法
'''
len(xxx)这种就是函数
car1.start() 属于某个对象，是方法
但是本质上他们是一样的，都是封装了某个功能的函数
'''
car1.start()

print("==="*30)

# 学生类 三个属性 姓名 年龄 性别 方法有两个 学习方法 ，获取年龄的方法
class Student:
    # 限制生成的对象当中属性的数量
    __slots__ = ("name", "age", "sex")
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex
    def study(self):
        return self.name, self.sex
    def get_age(self):
        print(self.name)
        return self.age
student1 = Student("藤都子", "16", "女")

print(tuple(student1.study()))
print(student1.study())
# print(list(student1.get_age("梦限大MewType！")))
# print(student1.get_age("梦限大MewType！"))
student1.get_age()
print(student1.name)
print(student1.age)
print("==="*30)

student2 = Student("阿拉蕾", "16", "female")
print(student2.age)
# 为什么可以随便加？（这里指abc, 意思是随便加可以输出的参数/属性）   因为每个对象背后都有一个__dict__（字典），属性都在这里面
student2.abc = 777
print(student2.abc)
# print(student2.__dict__)  # {'name': '阿拉蕾', 'age': '16', 'sex': '女', 'abc': 777}
# print(student2.get_age(),"wdad")
# 如果我们想让对象只能有固定的某几个属性，不准乱加------用__slots__
# 如果给对象添加属性 是否报错取决于是否限制了属性__slots__
# 上面的  __slots__ = ("name", "age", "sex")，就是限制的传入类的属性，因为
# 被限制在原先的三个参数里面了，所以外面再加入abc，然后直接输出这个属性就会报错

