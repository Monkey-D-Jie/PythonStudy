#正则表达式初识-简单的爬虫正则表达式
import re
import urllib.request
'''
简单爬虫demo
'''
data=urllib.request.urlopen("https://edu.csdn.net").read()
pat="<script src=.*?</script>"
rst=re.compile(pat).findall(data.decode("utf-8"))
print(rst)