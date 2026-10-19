"""# 单继承：一个子类继承一个父类
# 多继承：一个子类同时继承多个父类，从而拥有多个父类属性和方法

# 父类Mom
class Mom:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.job = "程序员"
    def sayHi(self):
        print("say hi")
    def show(self):
        print(f"我是妈妈的show，{self.name}，{self.age}岁,职业是{self.job}")

class Dad:
    def __init__(self, job, hobby):
        self.job = job
        self.hobby = hobby
    def sayHello(self):
        print("say hello")
    def show(self):
        print(f"我是爸爸的show，职业是{self.job}，爱好是{self.hobby}")

# 子类Kid
class Kid(Mom, Dad): # 关于用的是哪个父类的相同方法是由这里决定的
    def __init__(self, name, age, job, hobby):
        # super().__init__(name, age, job, hobby)
        # 实际上相当于
        # Mom.__init__(self, name, age, job, hobby)
        # super()在多继承里面不是调用所有的父类，而是按照MRO链依次调用下一个类
        # MRO是方法解析顺序 Method Resolution Order（方法解析顺序）
        # 利用了了c3线性化算法，决定多继承时属性和方法的查找顺序
        # 可以用__mro__查看

        # 显示各自调用的构造函数
        Dad.__init__(self, job, hobby) # 初始化爸爸那部分：self.job = "学生"
        Mom.__init__(self, name, age) # 初始化妈妈那部分：self.job = "程序员"
        # 注意：两个父类用的是同一个 self.job，Dad 先写、Mom 后写，
        # 所以最终 self.job 被妈妈的值覆盖成 "程序员"。




    def sayhaha(self): # Kid自己独有的方法
        print("say haha")

# 实例化子类
children = Kid("小蕾",16,"学生","唱歌")
# 继承自Mom
children.sayHi()
# 继承自Dad
children.sayHello()
# 自己独有的
children.sayhaha()

# show()
# 如果子类当中没有定义某个方法的时候，python会按照MRO链的顺序去父类当中找
children.show() # 这里调用的是Mom的show()因为python是按顺序解析的
# MRO: Kid -> Mom -> Dad -> object，先命中 Mom.show
# 而 Mom.show 里打印 self.job，这个值也在上面被 Mom 覆盖成了 "程序员"
# 所以方法来自 Mom、job 值也来自 Mom，看起来全是妈妈的
# 两个父类中使用相同名的方法，注意冲突

print(Kid.__mro__,"MRO") # <class '__main__.Kid'>, <class '__main__.Mom'>, <class '__main__.Dad'>, <class 'object'>"""

"""class Mom:
    def __init__(self, name, age, **kwargs):
        # super()更准确的说是去找在MRO列表中 找当前类之后的下一个类
        super().__init__(**kwargs) # 把剩余参数传给MRO中当前类的下一个类，
        # 这里下一个类按照mro是Dad
        self.name = name
        self.age = age
        self.job = "程序员"

    def sayHi(self):
        print("say hi")

    def show(self):
        print(f"我是妈妈的show，{self.name}，{self.age}岁,职业是{self.job}")

class Dad:
    def __init__(self, job, hobby, **kwargs):
        super().__init__(**kwargs)
        self.job = job
        self.hobby = hobby

    def sayHello(self):
        print("say hello")
    def show(self):
        print(f"我是爸爸的show，职业是{self.job}，爱好是{self.hobby}")

class Kid(Mom, Dad):
    def __init__(self, name, age, job, hobby):
        super().__init__(name=name,age=age,job=job,hobby=hobby)

    def sayhaha(self):  # Kid自己独有的方法
        print("say haha")

# 实例化子类
children = Kid("小蕾",16,"学生","唱歌")
print(Kid.__mro__,"MRO")
children.sayHi()
children.sayHello()
children.sayhaha()
children.show()
"""


# 共同的祖先 只调用一次
class Person:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.species = "人类"
        print("Person.__init__被调用了")

class Mom(Person):
    def __init__(self, name, age, **kwargs):
        # super()更准确的说是去找在MRO列表中 找当前类之后的下一个类
        super().__init__(**kwargs) # 把剩余参数传给MRO中当前类的下一个类，
        # 这里下一个类按照mro是Dad
        self.name = name
        self.age = age
        self.job = "程序员"

    def sayHi(self):
        print("say hi")

    def show(self):
        print(f"我是妈妈的show，{self.name}，{self.age}岁,职业是{self.job}")

class Dad(Person):
    def __init__(self, job, hobby, **kwargs):
        super().__init__(**kwargs)
        self.job = job
        self.hobby = hobby

    def sayHello(self):
        print("say hello")
    def show(self):
        print(f"我是爸爸的show，职业是{self.job}，爱好是{self.hobby}")

class Kid(Mom, Dad):
    def __init__(self, name, age, job, hobby):
        super().__init__(name=name,age=age,job=job,hobby=hobby)

    def sayhaha(self):  # Kid自己独有的方法
        print("say haha")

# 实例化子类
children = Kid("小蕾",16,"学生","唱歌")
print(Kid.__mro__,"MRO")
# Kid -> Mom -> Dad -> Person -> object
children.sayHi()
children.sayHello()
children.sayhaha()
children.show() # 程序员

print(children.species)





