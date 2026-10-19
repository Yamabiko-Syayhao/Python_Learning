# 创建类
class Student:
    # 类属性 定义在类里面，方法外边，所有实例共享
    school = "神田白马学院"
    # 实例属性 在__init__ 里通过self.属性名去赋值的 特点是每个实例独有的
    def __init__(self, name):
        self.name = name
    # 实例方法
    def say_name(self):
        print(f"实例方法：我叫{self.name}，学校是{self.school}，"
              f"学校的另外获取方式{Student.school}，{self}")
    # 类方法 用@classmethod装饰
    @classmethod
    def say_cls(cls):
        # cls--->类本身
        print(f"类方法：类{cls}，{cls.school}") # 不能有{cls.name}
        # 类方法不能访问实例属性
        # print(cls.name)
    # 静态方法 用@staticmethod装饰
    # 它就是逻辑上属于两个类 但是不需要访问实例或者类
    @staticmethod
    def tip():
        print(F"静态方法，666")
        # 这个方法可以获取到school 但是如果牵扯到了子类继承关系 他会永运读取父类的
        # Student.school 无法改动
        print(Student.school)
        # 没有self拿不到实例， 没有cls拿不到类  属于独立函数
        # print(self.name, cls.school)

# 实例化对象
s1 = Student("阿拉蕾")
s2 = Student("藤都子")
# 三个属性打印的结果是一样的 因为取的都是最外面的类属性
# print(s1.school)
# print(s2.school)
# print(Student.school)
#
# '''
# s2和类调用的属性没有被改，因为这个并不是改类的属性 而是给s1这个实例对象新建了一个新的
# 实例属性school, 当你去s1.school找的是它自己的实例属性
# 而s2和Student依旧是类属性  属性查找属性“先找实例再找类”
# '''
# print("=="*30)
# s1.school = "家里蹲"
# print(s1.school)
# print(s2.school)
# print(Student.school)

print("=="*30)
# 调用实例方法
# s1.say_name()
# s2.say_name()
print(s1.say_name()) # 上面对应方法的输出里面调用了它自身，所以会有<__main__.Student object at 0x000001BE3E5F46E0>
# 调用类方法
print(s1.say_cls()) # 上面对应方法的输出里面调用了它自身，所以会有<class '__main__.Student'>
# 调用静态方法
s1.tip()
# 类方法 静态方法 支持对象调用
# s1.say_cls()
s1.tip()


# 类属性可以被下面直接改
Student.school = "wwwwww"
# 实例属性外面改不了
# s1.name = "22"
# print(s2.name)
print(s1.school)
print(s2.school)

print("=="*30)

'''
实例方法 有个self代表的是当前实例，可以获取实例属性和类属性 最常用 调用方式 对象.方法()
类方法 通过@classmethod装饰器去修饰，有个cls代表类本身，只能访问类的属性，不能获取实例属性
调用方式 类.方法()

静态方法 通过@staticmethod装饰器修饰 属于独立函数 无法直接获取实例属性和类属性
 
 最常用的是实例方法，要用实例就用实例方法，要用类就用类方法 两个都不用就用静态方法
'''