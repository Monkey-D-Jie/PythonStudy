#urllib库方法初始
import re
import urllib.request,urllib.parse

#查看网页的简介信息
url = "https://www.bilibili.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0 Safari/537.36"
}
for i in range(1,100):
    try:
        req = urllib.request.Request(url, headers=headers)
        file = urllib.request.urlopen(req,timeout=2)
        print(str(i)+"------->>>"+str(file.code))
    except Exception as e:
        print("访问出错"+str(e))
