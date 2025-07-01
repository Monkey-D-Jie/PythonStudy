#正则表达式初识-爬虫的简单作业
import re
import urllib.request
from bs4 import BeautifulSoup

'''
将
https://read.douban.com/provider/all
下的初版社信息提取出来
'''
url = "https://read.douban.com/provider/all"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0 Safari/537.36"
}
req=urllib.request.Request(url,headers=headers)
# <div class="name">博集天卷</div>
# 发送请求
try:
    with urllib.request.urlopen(req) as response:
        data = response.read().decode("utf-8")
        print("成功获取数据，长度:", len(data))
        pat = "<div class=\"name\">(.*?)</div>"
        # rst = re.compile(pat).findall(data.decode("utf-8"))
        rst = re.findall(pat,data,re.DOTALL)
        print(rst)
        print("================BeautifulSoup=========================")
        soup = BeautifulSoup(data, "html.parser")
        # strip=True 去掉提取内容的空格
        names = [div.get_text(strip=True) for div in soup.select("div.name")]
        print("BeautifulSoup--->>>")
        for name in names:
            print(name)
except urllib.error.HTTPError as e:
    print("HTTP 错误:", e.code, e.reason)
