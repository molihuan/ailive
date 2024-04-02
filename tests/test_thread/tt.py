class ParentClass:
    def __init__(self):
        self._target = "parent_target"


class ChildClass(ParentClass):
    def __init__(self):
        super(ChildClass, self).__init__()  # 调用父类的构造函数
        # 获取父类的 _target 属性
        # parent_target = self._target
        # print("Parent target:", parent_target)

    def run(self):
        print("Parent target:", self._target)


# 创建子类的实例
child = ChildClass()

child.run()
