#urllib库方法初始
import re
import urllib.request,urllib.parse

#urlretrieve(网址，本地文件存储地址)，直接爬取到本地
# urllib.request.urlretrieve("https://www.baidu.com/","H://myIdeaWorkSpace//PythonStudy//demo//testFile//urlretrieve-demo.html")
#清除网页访问本地缓存
# urllib.request.urlcleanup()
#查看网页的简介信息
url = "https://www.bilibili.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0 Safari/537.36"
}
req=urllib.request.Request(url,headers=headers)
file=urllib.request.urlopen(req)
print(file.info())
print(file.code)
print(file.url)