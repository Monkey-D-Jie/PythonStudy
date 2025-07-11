#get请求操作demo
import random
import re
import time
import urllib.request,urllib.parse



def write_res_data_to_local_file(data, filePath,write_mode):
    # 添加 encoding='utf-8' 参数
    with open(filePath, write_mode, encoding='utf-8') as fh:
        fh.write(data)
    fh.close()

local_file_path = "/testFile//"

'''
浏览器伪装
'''
url = "http://blog.csdn.net"
#opener
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36')]
openerRes = opener.open(url).read().decode("utf-8")
print(url+"》》》======》》》------->>>"+openerRes)
write_res_data_to_local_file(openerRes, local_file_path + "openerRes.html", "w")
# 随机等待1-3秒，避免请求过于频繁
time.sleep(random.uniform(1, 3))
#request
#模拟浏览器的请求头格式
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    # ,"Referer": "https://cn.bing.com/",
    # "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    # "Accept-Encoding": "gzip, deflate, br",
    # "Connection": "keep-alive"
}
req = urllib.request.Request(url, headers=headers)
rea_response = urllib.request.urlopen(req).read().decode("utf-8")
print(url+"》》》======》》》------->>>"+rea_response)
write_res_data_to_local_file(rea_response, local_file_path + "reqResponse.html", "w")





