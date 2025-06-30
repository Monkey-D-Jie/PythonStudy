##继承（单继承，多继承）
#父亲类-基类
class father():
    def speak(self):
        print("father can speak!")
#儿子类，单继承
class son(father):
    pass
#母亲类-基类
class mother():
    def write(self):
        print("mother cab write!")
#多继承
class daughter(father,mother):
    def listen(self):
        print("daughter can listen!")
    
#重写（重载）
class son2(father):
    def speak(self):
        print("son2 override father speak()")
