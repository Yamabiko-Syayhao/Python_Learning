# 继承 儿子继承父类的一些属性和方法 并且儿子也有自己独特的属性和方法

# 父类
class Teacher:
    def __init__(self, name, age, title):
        self.name = name
        self.age = age
        self.title = title
    def eat(self, food):
        print(f"{self.name}老师正在吃{food}")
    def teach(self, course):
        print(f"{self.name}老师，正在讲{course}")


# 学生类 继承自老师类
class Student(Teacher):
    def __init__(self, name, age, score, title):
        # 通过super 调用父类（也就是老师类）的构造函数
        super().__init__(name, age, title)
        self.score = score

    def eat(self, food): # 扩展父类方法的功能
        super().eat(food)
        print("再吃点小垃圾")

    def study(self, band):
        print(f"{self.name}学生正在学校，学习的课程是{self.score},是乐队{band}的成员")
    def play(self, val):
        print(f"{self.name}学生正在玩{val}")

# 实例化
s1 = Student("千石由乃", "16", "游戏", "音乐老师")
# 学生类里面没有title属性，没有eat/teach方法，现在这个属性和方法能用起来是因为继承了
# 老师类里面的title属性和eat/teach方法
print(s1.title)
s1.eat("apple")
s1.teach("mj")
s1.study("Mewtype")
s1.play("瓦洛兰特")





'''
面向对象的特点：
1.封装：将数据和操作数据的方法封装在一起，对外提供接口，隐藏内部实现的细节
2.抽象：将复杂的事物抽象成类，只关注对象要做什么，不关注对象如何做
3.继承：子类可以继承父类的属性和方法，子类可以扩展父类的功能
4.父类定义的操作方法可以被子类重写，实现不同子类的功能
'''

class Animal:
    def speak(self):
        pass


class Dog(Animal):
    def speak(self):
        print("wwww")

class Cat(Animal):
    def speak(self):
        print("mmmm")

class Duck(Animal):
    def speak(self):
        print("gggg")

# 同一个函数 接收不一样的对象
# 这个函数并不关心传入的对象是dog还是cat还是duck 它只知道这些对象当中都有一个speak方法
def make_noise(animal):
    animal.speak()

make_noise(Dog())
make_noise(Cat())
make_noise(Duck())
