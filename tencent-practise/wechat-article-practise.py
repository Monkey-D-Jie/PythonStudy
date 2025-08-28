# -*- coding: utf-8 -*-
import os
import time
import urllib.request
import urllib.parse
import re
import random
import time
from pathlib import Path
from time import sleep
from typing import Union, Any

from tqdm import tqdm
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent

# 直接导入（需确保PyCharm已标记Sources Root）
from common.urllib_common import ua_init, extract_redirect_url,save_as_mhtml,html_convert_to_mhtml



from bs4 import BeautifulSoup
import requests


ua = UserAgent()
headers = {
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    'host':'weixin.sogou.com',
    'cookie':'IPLOC=CN5101; SUID=62AEB96E5B54A20B000000006764C5E6; cuid=AAGQLkKYUAAAAAuiUusErgAASQU=; SUV=00514C436EB9AE626764C5E8F3DB7133; ABTEST=0|1754298952|v1; weixinIndexVisited=1; SNUID=1BB1F05A3F3805B9B1416EB63FAAF9D8; ariaDefaultTheme=undefined'
}

weixin_headers = {
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    'orgin':'https://mp.weixin.qq.com',
    'cookie':'pgv_pvid=23391385; ptcz=abf40a67d146f70d4f7539bd683b1a321486da1e370b0d8b46263e0a9e6c59dc; pac_uid=0_KY38tyWw6KzPQ; ua_id=AeYZaCDFYclJgh44AAAAABgXb9YRQ0xDZAU-kkEtvoE=; wxuin=32505449292765; mm_lang=zh_CN; suid=user_0_KY38tyWw6KzPQ; _qimei_uuid42=18b1b0928131003506693b8e754017f2addfaba8c8; RK=vW29Z6p600; _qimei_q32=5a0bb7f66e49d761db307214d843525e; _qimei_q36=8a858171939505fbd88c6019300016e18411; yyb_muid=319CF8F7CB816B6F3197E86ECAC26AB4; omgid=0_KY38tyWw6KzPQ; _qimei_h38=b00bd380937b5737ec0e7a6002000009017a14; _clck=3596452815|1|fxp|0; xid=f2fcf382db3f90c1d4f8f3606603be1a; _qimei_fingerprint=2ee8162b283c384d7f73b9a761300af1; rewardsn=; wxtokenkey=777'
}


# 1.定义用户代理池，直接使用已定义好的方法
from common.urllib_common import ua_init

def reg_pat_parse_data(response_data,regex) -> Union[list[Any], list[Union[Union[str, bytes], Any]]]:
    parse_data = re.compile(regex, re.S | re.I).findall(response_data)
    return parse_data
def soup_parse_data(response_data) -> Union[list[Any]]:
    links = []
    soup = BeautifulSoup(response_data,features = "html.parser")
    # strip=True 去掉提取内容的空格，通过CSS解析器来获取到指定标签下的内容，soup.select("标签")
    # parse_ret = [div.get_text(strip=True) for div in soup.select("a[href]")]
    # 指定要查找的HTML标签类型，这里是 <a> 标签（超链接标签）。过滤条件，表示只选择包含 href 属性和 target="_blank" 属性的 <a> 标签
    href_arr = soup.select('a[target="_blank"][href]')
    # 遍历所有<a>标签（超链接标签）
    for a_tag in href_arr:  # href=True表示必须包含href属性
        link = a_tag.get('href')  # 获取href属性值
        if "link?url" in link and "sogou" not in link:
            links.append(link)
    # print(links)
    return list(set(links))


def anti_anti_spider(url):
    # 配置浏览器参数
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # 初始化浏览器
    driver = Chrome(options=chrome_options)

    try:
        # 随机延时（2-5秒）
        time.sleep(random.uniform(1, 2))

        # 访问页面
        driver.get(url)

        # 模拟人类滚动
        for _ in range(3):
            ActionChains(driver).move_by_offset(
                xoffset=random.randint(100, 300),
                yoffset=random.randint(200, 400)
            ).perform()
            time.sleep(random.uniform(0.5, 1.5))

        # 获取完整页面内容
        html = driver.page_source
        return html

    except Exception as e:
        print(f"触发反爬机制: {str(e)}")
        # 此处添加验证码处理逻辑
        return None
    finally:
        driver.quit()


def save_article_content(url: str, save_path: str, headers: dict = None):
    """使用requests安全保存网页内容"""
    try:
        # 创建存储目录（如果不存在）
        Path(os.path.dirname(save_path)).mkdir(parents=True, exist_ok=True)

        # 发送HTTP请求
        print(f"------>>>请求链接：{url},对应的请求头：{headers}")
        response = requests.get(url, headers=headers, timeout=15,stream=True)
        response.raise_for_status()  # 自动处理HTTP错误码

        # 获取文件总大小（可能不存在）
        total_size = int(response.headers.get('content-length', 0))

        # 初始化字节缓冲区
        content_buffer = bytearray()
        # 创建进度条（动态调整单位）
        with tqdm(total=total_size, unit='B',
                  unit_scale=True,
                  desc=f"下载 {os.path.basename(save_path)}") as pbar:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:  # 过滤保持连接的空白块
                        f.write(chunk)
                        content_buffer.extend(chunk)
                        pbar.update(len(chunk))

        # 处理编码（优先使用网页声明的编码）
        encoding = response.encoding if 'charset' in response.headers.get('content-type', '') else 'utf-8'
        content = content_buffer.decode(encoding, errors='replace')

        # 安全写入文件
        # with open(save_path, 'w', encoding='utf-8') as f:
        #     f.write(content)

        if html_convert_to_mhtml(url,
                         content,  # 确保这是完整的HTML内容
                         save_path):
            print("mhtml文件内容已成功生成")
            return True
        return None
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {url} | 错误: {str(e)}")
        return False
    except IOError as e:
        print(f"文件保存失败: {save_path} | 错误: {str(e)}")
        return False


# 5. 处理重定向并获取最终内容
def get_redirected_content(url):
    try:
        # 不自动重定向
        req = urllib.request.Request(url)
        for key, value in headers.items():
            req.add_header(key, value)

        # 创建不自动重定向的opener
        no_redirect = urllib.request.HTTPRedirectHandler()
        opener = urllib.request.build_opener(no_redirect)

        response = opener.open(req)

        # 如果是重定向响应
        if response.status in (301, 302, 303, 307):
            redirect_url = response.headers['Location']
            print(f"重定向至: {redirect_url}")

            # 再次请求重定向URL
            final_req = urllib.request.Request(redirect_url)
            for key, value in headers.items():
                final_req.add_header(key, value)

            final_response = urllib.request.urlopen(final_req)
            return final_response.read().decode('utf-8', 'ignore')
        else:
            return response.read().decode('utf-8', 'ignore')

    except Exception as e:
        print(f"请求失败: {e}")
        return None


# 2.支持在执行窗口中输入搜索词
default_query = '灵笼'
input_query_key = input(f"请输入您感兴趣的关键词:")
query_key = input_query_key if input_query_key else default_query

parse_req_server="https://weixin.sogou.com"
for i in range(1,2):
    cur_req_url = "https://weixin.sogou.com/weixin?query="+urllib.parse.quote(query_key)+"&type=2&page="+str(i)+"&_sug_=n"
    print(f"------>>>当前的请求链接：{cur_req_url}")
    # ua_init()
    # cur_req_data = urllib.request.urlopen(cur_req_url).read().decode("utf-8","ignore")
    # cur_req_data = anti_anti_spider(cur_req_url)
    cur_req_response = requests.get(cur_req_url, headers=headers)
    cur_req_data = cur_req_response.text
    print(f"得到的响应内容大小为：{len(cur_req_data)}")
    # 提取内容
    # cur_content_reg_pat = '.*?<a target="_blank" href="(.*?)"'
    # reg_parse_data = reg_pat_parse_data(cur_req_data,cur_content_reg_pat)
    # print(f"reg_parse_ret---当前提取到的内容为：{reg_parse_data}")
    soup_parse_ret = soup_parse_data(cur_req_data)
    print(f"soup_parse_ret---当前提取到的内容为：{soup_parse_ret}")
    print("--------------------------------------")
    for j in range(0,len(soup_parse_ret)):
        article_req_url = parse_req_server+soup_parse_ret[j]
        redirect_data = get_redirected_content(article_req_url)
        redirect_url = extract_redirect_url(redirect_data)
        article_file_name = "wechat_article_"+query_key+"_"+str(i)+"_"+str(j)+".mhtml"
        save_dir = "H:\\myIdeaWorkSpace\\PythonStudy\\testFile\\wechat-article\\"
        # urllib.request.urlretrieve(article_req_url,"H:\\myIdeaWorkSpace\\PythonStudy\\testFile\\wechat-article\\"+article_file_name)
        # print(article_file_name+"抓取完成！")
        # 随机延时（2-5秒）
        '''
        2025年8月8日11:03:54 更新
        由于现在公众号已经对文章内容做了加密，
        虽然能拿到标题，
        但整体内容上还是有比较大的缺失。
        故暂时只能作罢。
        '''
        time.sleep(random.uniform(2, 5))
        if save_article_content(redirect_url,
                                os.path.join(save_dir, article_file_name),
                                headers=weixin_headers):
            print(f"{article_file_name} 抓取完成！")

