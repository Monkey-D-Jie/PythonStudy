#作用域。函数，局部变量与全局变量 
'''
i=10
def func():
    j=10
    print(j)
print(i)
'''
def abc():
    print("Hello Function");
#调用函数：函数名(参数)
abc()
#函数参数的应用：与外界沟通的媒介
#参数：形参和实参，
#形参：函数定义式使用的参数，用于声明接口调用方法和规则
#实参：实际调用函数的时候使用的参数
def fun2(a,b):
    if(a > b):
        print("a大");
    else:
        print("b大或者两者相等");
#函数调用示例
fun2(4,5)
fun2(8,6)
#模块

