#get请求操作demo
import random
import re
import time
import urllib.request,urllib.parse

#查看网页的简介信息
'''
场景
在必应中搜索“灵笼”，
然后将首页的搜索结果打印出来
https://cn.bing.com/search?q=%E7%81%B5%E7%AC%BC&FPIG=1E344C2D8C884BB3BE0ABDEC51FBB985&first=10
2025年7月7日15:13:00 更新
未能实现，
因为现在访问到的页面，
它们的内容已经发生了很大的变化。
视频中的方法是5年前的了，已经不再适用。
故本demo旨为理解过程，细节之处暂不深究。
'''
url = "https://cn.bing.com/search?form=bing&q="
keyword="灵笼"
transKeyWord=urllib.parse.quote(keyword)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    # ,"Referer": "https://cn.bing.com/",
    # "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    # "Accept-Encoding": "gzip, deflate, br",
    # "Connection": "keep-alive"
}
for i in range(1,10):
    try:
        pageUrl=url+transKeyWord+"&FPIG=1E344C2D8C884BB3BE0ABDEC51FBB985&first="+str((i-1)*10)
        req = urllib.request.Request(pageUrl, headers=headers)
        # 随机等待1-3秒，避免请求过于频繁
        time.sleep(random.uniform(1, 3))
        response = urllib.request.urlopen(req,timeout=2).read().decode("utf-8")
        pat = '<span class="b_mdsnp">(.*?)</span>'
        # pat2='<h2 class=""><a target="_blank".*?》(.*?)'
        patRet = re.compile(pat).findall(response)
        print(pageUrl+"》》》======》》》"+str(i)+"------->>>"+str(patRet))
    except Exception as e:
        print("访问出错"+str(e))
