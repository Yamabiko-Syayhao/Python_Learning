class Person:
    def __init__(self, name, age, salary):
        self.name = name # 公共的属性，任何地方都能访问
        self._age = age #受保护的属性（约定）约定为内部使用，但是语法上不强制禁止外部访问
        self.__salary = salary # 私有属性，不允许直接修改 会触发名称改写
        # 外部和子类不能直接修改
    # 对外提供接口
    def get_salary(self):
        return self.__salary


p1 = Person("zss", 16,23)
print(p1.name) # 外部可以直接访问
p1.name = "wws" # 外部可以修改
print(p1.name)

p2 = Person("www",18,24)
# 语法上可以访问 但是不建议 单下划线只是约定. 告诉其他程序员“这个值是内部使用的”
print(p2._age)


p3 = Person("www",19,25)
# print(p3.__salary) # 访问不了
# 当写了__属性名的时候，python底层会把属性名改成_类名__属性名
print(p3._Person__salary)

# 正规要这样获取 通过某个方法去获取
print(p3.get_salary())




# 面向对象特点之一，封装 把属性和方法打包到类里面，该暴露的暴露给外面用，不该暴露的藏起来
# 不让随便修改，上边的salary就是

# 封装 将数据和操作数据方法封装在一起，对外提供接口，隐藏内部的细节


# 特点之二 抽象 把复杂的事物抽象成类，只关注对象要做什么，不关注对象怎么实现



