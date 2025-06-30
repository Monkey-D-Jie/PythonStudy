#异常处理
'''
异常处理语法格式
try:
    程序
except Exception as 异常名称 :
    异常处理部分
'''
#异常出现，直接终止了程序
try:
    for i in range(0,10):
        print(i)
        if(i==4):
            print(wer)
    print("Hello")
except Exception as err:
    print(err)
#在颗粒度更细的地方捕获异常，以执行全部程序。有异常的打印异常信息
print("+++++++++++++++++++")
for i in range(0,10):
    try:
         print(i)
         if(i==4):
             print(wer)
    except Exception as err:
        print(err)
print("Hello")
