import urllib.request
import re
import random

'''
2025年7月22日13:50:32 更新
本demo的旨在完成用户代理池的简单实践
'''
# 来源：浏览器中发起请求的user-agent
user_pools=[
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",#Google浏览器
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"#edge浏览器
]

# 定义使用用户代理池的方法
def ua_init(user_pools):
    # 随机获取到一个代理对象
    random_up = random.choice(user_pools)
    print(f"当前获取到的代理对象：{random_up}")
    # 全局设置请求头
    init_headers =("User-Agent",random_up)
    init_opener = urllib.request.build_opener()
    init_opener.add_headers = [init_headers]
    # 安装为全局
    urllib.request.install_opener(init_opener)
req_url = "https://baidu.com"
for i in range(1,10):
    try:
        ua_init(user_pools)
        # 模拟请求
        req_data = urllib.request.urlopen(req_url).read().decode("utf-8","ignore")
        print("第"+str(i)+"次请求，获取到内容长度为："+str(len(req_data)))
    except Exception as e:
        print("循环执行过程中出现了异常："+e)
