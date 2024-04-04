class MyClass:
    shared_variable = 0  # 这是一个类变量

    def __init__(self, value):
        self.instance_variable = value


# 实例化类
obj1 = MyClass(5)
obj2 = MyClass(8)

# 访问类变量
print(MyClass.shared_variable)  # 输出: 0

# 修改类变量
MyClass.shared_variable = 10
print(MyClass.shared_variable)  # 输出: 10

# 访问实例变量
print(obj1.instance_variable)  # 输出: 5
print(obj2.instance_variable)  # 输出: 8

MyClass.shared_variable = 3

# 修改类变量后，所有实例中对应的值都会被修改
print(obj1.shared_variable)  # 输出: 10
print(obj2.shared_variable)  # 输出: 10
