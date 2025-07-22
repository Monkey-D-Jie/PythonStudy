import urllib.request
import re
import random
from urllib.request import HTTPHandler

'''
2025年7月22日14:10:51 更新
此demo旨在演示IP代理池的应用方法
构建IP代理池的第一种方案
同“用户代理池”类似，用写定的几个ip来做为发起请求的代理
与之相对应的，
还有另外的一种方式：即通过接口请求，获取到动态的ip地址，
然后赋值到ip_pools变量中，后面的按照同样的执行方式去获取到请求的目标数据
'''

agent_pools=[
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",#Google浏览器
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"#edge浏览器
]

ip_pools=[
    "24.233.2.14:80",
    "87.239.31.43:80",
    "87.239.31.42:80",
    "188.191.165.159:8080",
    "188.234.158.66:80",
    "109.95.220.45:8080",
    "109.197.153.25:8888",
    "95.66.138.21:8880",
    "77.238.103.98:8080",
    "91.239.17.22:8080"
]
req_pat = '<img[^>]*?src="/assets/img/loading_cheng\.gif\?v=2\.4\.20" [^>]*?lay-src="(.*?)"[^>]*?>'
# 定义使用用户代理池的方法
def ua_init(ip_pools):
    # 随机获取到一个代理对象
    random_ip = random.choice(ip_pools)
    print(f"当前获取到的IP代理对象：{random_ip}")
    # 全局设置请求头
    init_ip_proxy = urllib.request.ProxyHandler({"http":random_ip})
    # init_opener = urllib.request.build_opener(init_ip_proxy,HTTPHandler)
    init_opener = urllib.request.build_opener()

    random_up = random.choice(agent_pools)
    print(f"当前获取到的用户代理对象：{random_up}")
    # 全局设置请求头
    init_headers = ("User-Agent", random_up)
    init_opener.add_headers = [init_headers]
    # 安装为全局
    urllib.request.install_opener(init_opener)

# req_original="https://www.toopic.cn"
# req_url = "https://desk.3gbizhi.com/deskDM/index_2.html"
test_content="""class="dark-tab-item "><span class="tab-text"> 植物壁纸 </span><span class="tab-count">(48张)</span></a><a href="https://desk.3gbizhi.com/deskDW/" class="dark-tab-item "><span class="tab-text"> 动物壁纸 </span><span class="tab-count">(73张)</span></a><a href="https://desk.3gbizhi.com/deskCY/" class="dark-tab-item "><span class="tab-text"> 创意壁纸 </span><span class="tab-count">(73张)</span></a><a href="https://desk.3gbizhi.com/deskjy/" class="dark-tab-item "><span class="tab-text"> 简约壁纸 </span><span class="tab-count">(44张)</span></a><a href="https://desk.3gbizhi.com/deskCM/" class="dark-tab-item "><span class="tab-text"> 车模壁纸 </span><span class="tab-count">(107张)</span></a><a href="https://desk.3gbizhi.com/deskDT/" class="dark-tab-item "><span class="tab-text"> 动态壁纸 </span><span class="tab-count">(8张)</span></a></div></div></div></div><div class="cont-desk-listw"><ul class="cl video-wrapper"><li class="box_black video-item"><a href="https://desk.3gbizhi.com/deskDM/4598.html" class="desk imgw"><img src="/assets/img/loading_cheng.gif?v=2.4.20" lay-src="https://pic.3gbizhi.com/uploads/20250720/ba6f36e854710d92f9a7934452e3c2a7.webp" alt="黑色短发，面部硬朗，留着黑色胡须，手拿武士刀的刀客壁纸图片"><div class="title">黑色短发，面部硬朗，留着黑色胡须，手拿武士刀的刀客壁纸图片</div></a><div class="tips"><a href="https://www.3gbizhi.com/pictag/guangying">光影</a><a href="https://www.3gbizhi.com/pictag/daoke">刀客</a><a href="https://www.3gbizhi.com/pictag/hualigan">华丽感</a><a href="https://www.3gbizhi.com/pictag/jianyi">坚毅</a><a href="https://www.3gbizhi.com/pictag/wushidao">武士刀</a><a href="https://www.3gbizhi.com/pictag/nanxingdeliliang">男性的力量</a><a href="https://www.3gbizhi.com/pictag/yanshenruili">眼神锐利</a><a href="https://www.3gbizhi.com/pictag/susha">肃杀</a><a href="https://www.3gbizhi.com/pictag/heisehuxi">黑色呼吸</a></div></li><li class="box_black video-item"><a href="https://desk.3gbizhi.com/deskDM/4597.html" class="desk imgw">"""
# 添加跨行匹配和忽略大小写
test_url_list = re.compile(req_pat, re.S | re.I).findall(test_content)
print(test_url_list)
pic_save_path="G:\\测试图源集合\\"
for i in range(1,10):
    try:
        ua_init(ip_pools)
        # 模拟请求
        req_url = f"https://desk.3gbizhi.com/deskDM/index_{i}.html"
        req_data = urllib.request.urlopen(req_url).read().decode("utf-8","ignore")
        print("第"+str(i)+"次请求，获取到内容长度为："+str(len(req_data)))
        # pat = '<img class="lazy" data-original="(.*?)".*?/>'
        pic_url_list = re.compile(req_pat).findall(req_data)
        for j in range(1,len(pic_url_list)):
            current_pic_url = pic_url_list[j]
            current_pic_save_path = pic_save_path+str(i)+"_"+str(j)+".jpg"
            urllib.request.urlretrieve(current_pic_url,current_pic_save_path)
            print(f"url为：{current_pic_url}的图片保存成功")
    except Exception as e:
        print(f"循环执行过程中出现了异常：{e}")
