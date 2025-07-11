# print(1234)
'''
print(1234)
print(1234)
print(1234)

print(1234)
print(1234)
print(1234)
abc=10
#列表：跟java类似，可以存储多个数据
arr=[7,'cd',9]
#元组,元素不可重新赋值
c=(7,'cd',9)
#字典{"键":值...}
d={'a':1,'b':2,'c':"12qaz"}
#集合
e=set("abcdefgaged")
f=set("arfbgh")
g=e-f
h=e and f
#运算符，+ - * / %,跟java的一样的。%也是取余运算

#缩进
#控制流，感觉也是跟java类似的。if，while，for
b=1
if(b==1):
    print("1为真");
elif(b==0):
    print("2为真")
#while分支控制
a=0
while(a<10):
    print("Hello"+str(a));
    a+=1
#for 常规循环
for i in range(0,10):
    print("Hello A")
'''
#乘法口诀表输出
#end=""表示不换行输出
print("乘法口诀-顺序输出")
for i in range(1,10):
    for j in range(1,i+1):
        print(str(i)+"*"+str(j)+"="+str(i*j),end="   ")
    print()
print("乘法口诀-逆序输出")
for i in range(9,0,-1):
    for j in range(i,0,-1):
        print(str(i)+"*"+str(j)+"="+str(i*j),end="   ")
    print()





