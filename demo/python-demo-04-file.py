#文件读取
'''
方法：open(文件地址，操作形式)
w：写
r：读
b：二进制形式读
a：追加
'''
fh=open("H:/myIdeaWorkSpace/PythonStudy/demo/testFile/test.txt","r",encoding="utf-8")
#文件读取
content = fh.read()
print(content)
print("++++++++++=")
#line=fh.readline()
#print(line)
#循环读取文件
'''
x=0
while True:
    line = fh.readline()
    if(len(line)==0 and x>10):
        break
    print(line)
    x+=1
#关闭文件
fh.close()
'''
#文件的写入
data="接天莲叶无穷碧，映日荷花别样红"
fh2=open("H:/myIdeaWorkSpace/PythonStudy/demo/testFile/test2.txt","w",encoding="utf-8")
fh2.write(data)
fh2.close()
data3="江南无所有，聊赠一枝春"
fh3=open("H:/myIdeaWorkSpace/PythonStudy/demo/testFile/test2.txt","a",encoding="utf-8")
fh3.write(data3)
fh3.close()

