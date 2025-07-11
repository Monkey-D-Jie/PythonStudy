#面相对象编程
#类和对象
'''
创建一个类
class 类名:
    类里面的内容
'''
class cl1:
    pass
#实例化一个类
a=cl1()
print("实例化一个类")
print(a)

#构造方法
#self：在类中的方法必须加上self参数
#__init__(self,参数)
#构造函数的意义：初始化
class cl2:
    def __init__(self):
        print("I am constructor cl2 self")
        print("===============")
#给类加上参数：给构造方法加上参数
class cl3:
    def __init__(self,name,job):
        print("My name is +"+name+",and my job is "+job)
#属性：类里面的变量：self.属性名
class cl4:
    def __init__(self,name,job):
        self.myname=name
        self.myjob=job
     #类里面的方法，也叫函数。def 方法名(self,参数)   
    def greet(self):
        print(f"Hello, my name is {self.myname} and my job is {self.myjob}.")
class cl6:
    def __init__(self,name):
        self.myname=name
    def myfun1(self):
        print(f"Hello {self.myname}")

