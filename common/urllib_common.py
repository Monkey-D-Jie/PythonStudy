import random
import urllib.request
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
from urllib.parse import urlparse
from common import HtmlConvertMhtml

from fake_useragent import UserAgent

from common.HtmlConvertMhtml import HTMLToMHTMLConverter

agent_pools=[
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",#Google浏览器
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"#edge浏览器
]

ip_pools=[
    "203.174.15.142:8080",
    "192.163.215.98:80",
    "61.179.129.1:80",
    "69.160.9.166:8080",
    "102.68.128.217:8080",
    "183.164.243.138:8089",
    "178.213.24.216:8080",
    "117.69.236.216:8089",
    "117.71.155.60:8089",
    "213.150.76.246:3128"
]


ua = UserAgent()
headers = {
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    'Referer': 'https://weixin.sogou.com/'
}

# 定义使用用户代理池的方法
def ua_init():
    # 随机获取到一个代理对象
    random_ip = random.choice(ip_pools)
    print(f"当前获取到的IP代理对象：{random_ip}")
    # 全局设置请求头
    init_ip_proxy = urllib.request.ProxyHandler({"http":random_ip})
    # init_opener = urllib.request.build_opener(init_ip_proxy,HTTPHandler)
    init_opener = urllib.request.build_opener()

    random_up = random.choice(agent_pools)
    # print(f"当前获取到的用户代理对象：{random_up}")
    # 全局设置请求头
    # init_headers = ("User-Agent", random_up)
    # 设置cookie
    init_cookie = "IPLOC=CN5101; SUID=62AEB96E5B54A20B000000006764C5E6; cuid=AAGQLkKYUAAAAAuiUusErgAASQU=; SUV=00514C436EB9AE626764C5E8F3DB7133; ABTEST=0|1754298952|v1; weixinIndexVisited=1; SNUID=1BB1F05A3F3805B9B1416EB63FAAF9D8; ariaDefaultTheme=undefined"
    init_cookie_headers = ("cookie",init_cookie)
    init_opener.add_headers = [init_cookie_headers,headers]
    # 安装为全局
    urllib.request.install_opener(init_opener)

def extract_redirect_url(content):
    """
    从给定的HTML/JS内容中提取跳转的URL
    :param content: 包含跳转JS代码的内容字符串
    :return: 提取到的完整URL，如果未找到则返回None
    """
    # 使用正则表达式匹配所有url += '...'的部分
    # 匹配模式：url += '任意字符'，捕获单引号内的内容
    pattern = r"url \+?= '([^']+)'"
    matches = re.findall(pattern, content)

    if not matches:
        return None

    # 拼接所有匹配到的URL片段
    full_url = ''.join(matches)

    # 执行代码中的replace操作（如果有的话）
    full_url = full_url.replace("@", "")
    return full_url



def save_as_mhtml(url, content, filename):
    # 创建MIME容器
    msg = MIMEMultipart('related', boundary="MY_MHTML_BOUNDARY")

    # 添加主文档部分
    main_part = MIMEText(content, 'html', 'utf-8')
    main_part['Content-Location'] = url
    msg.attach(main_part)

    # （可选）处理内嵌资源
    # 这里需要解析content并下载图片/CSS等资源
    # 然后添加为额外的MIME part

    # 写入文件
    with open(filename, 'wb') as f:
        f.write(msg.as_bytes().replace(b'\n', b'\r\n'))  # MIME要求CRLF换行
        f.write(b'\r\n')  # 结束边界

def html_convert_to_mhtml(url,handle_html_content,filename):
    # 你的HTML内容（可以从文件读取或直接传入）
    # with open(handle_html_content, "r", encoding="utf-8") as f:
    #     html_content = f.read()

    # 基础URL（根据HTML来源设置，此处以微信公众号为例）
    # base_url = "https://mp.weixin.qq.com"

    # 转换并保存
    converter = HTMLToMHTMLConverter(url)
    converter.convert(handle_html_content, filename)
    return True


import re
import time
import random
import requests
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from urllib.parse import urljoin, urlparse


# --------------------------
# 1. 爬取微信公众号文章HTML内容
# --------------------------
def fetch_wechat_article(url):
    """获取微信公众号文章的HTML内容，处理反爬"""
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.38"
        ]),
        "Referer": "https://mp.weixin.qq.com/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        # 可选：添加Cookie（从浏览器复制，处理登录状态）
        # "Cookie": "你的微信Cookie"
        'cookie': 'pgv_pvid=23391385; ptcz=abf40a67d146f70d4f7539bd683b1a321486da1e370b0d8b46263e0a9e6c59dc; pac_uid=0_KY38tyWw6KzPQ; ua_id=AeYZaCDFYclJgh44AAAAABgXb9YRQ0xDZAU-kkEtvoE=; wxuin=32505449292765; mm_lang=zh_CN; suid=user_0_KY38tyWw6KzPQ; _qimei_uuid42=18b1b0928131003506693b8e754017f2addfaba8c8; RK=vW29Z6p600; _qimei_q32=5a0bb7f66e49d761db307214d843525e; _qimei_q36=8a858171939505fbd88c6019300016e18411; yyb_muid=319CF8F7CB816B6F3197E86ECAC26AB4; omgid=0_KY38tyWw6KzPQ; _qimei_h38=b00bd380937b5737ec0e7a6002000009017a14; _clck=3596452815|1|fxp|0; xid=f2fcf382db3f90c1d4f8f3606603be1a; _qimei_fingerprint=2ee8162b283c384d7f73b9a761300af1; rewardsn=; wxtokenkey=777'
    }

    try:
        # 随机延迟，模拟人类浏览
        time.sleep(random.uniform(1, 3))
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = "utf-8"  # 强制UTF-8编码，避免乱码

        # 检查是否触发验证码
        if "验证码" in response.text:
            raise Exception("请求被拦截，需手动处理验证码或添加Cookie")
        return response.text
    except Exception as e:
        print(f"爬取失败：{str(e)}")
        return None


# --------------------------
# 2. HTML转MHTML核心类
# --------------------------
class HTMLToMHTMLConverter:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": base_url,
            "Cookie":"pgv_pvid=23391385; ptcz=abf40a67d146f70d4f7539bd683b1a321486da1e370b0d8b46263e0a9e6c59dc; pac_uid=0_KY38tyWw6KzPQ; ua_id=AeYZaCDFYclJgh44AAAAABgXb9YRQ0xDZAU-kkEtvoE=; wxuin=32505449292765; mm_lang=zh_CN; suid=user_0_KY38tyWw6KzPQ; _qimei_uuid42=18b1b0928131003506693b8e754017f2addfaba8c8; RK=vW29Z6p600; _qimei_q32=5a0bb7f66e49d761db307214d843525e; _qimei_q36=8a858171939505fbd88c6019300016e18411; yyb_muid=319CF8F7CB816B6F3197E86ECAC26AB4; omgid=0_KY38tyWw6KzPQ; _qimei_h38=b00bd380937b5737ec0e7a6002000009017a14; _clck=3596452815|1|fxp|0; xid=f2fcf382db3f90c1d4f8f3606603be1a; _qimei_fingerprint=2ee8162b283c384d7f73b9a761300af1; rewardsn=; wxtokenkey=777"
        }
        self.resources = []  # 存储资源：(url, content, mime_type)

    def _get_absolute_url(self, relative_url):
        """处理相对URL和协议相对URL（如//res.wx.qq.com）"""
        if not relative_url:
            return None
        if relative_url.startswith('//'):
            parsed_base = urlparse(self.base_url)
            return f"{parsed_base.scheme}:{relative_url}"
        return urljoin(self.base_url, relative_url)

    def _download_resource(self, url):
        """下载资源并返回内容和MIME类型"""
        try:
            time.sleep(random.uniform(0.5, 1.5))  # 资源下载延迟
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            mime_type = response.headers.get('Content-Type', 'application/octet-stream').split(';')[0]
            return response.content, mime_type
        except Exception as e:
            print(f"资源下载失败 {url}：{str(e)}")
            return None, None

    def _extract_resources(self, html_content):
        """从HTML中提取所有外部资源（CSS、JS、图片等）"""
        soup = BeautifulSoup(html_content, 'html.parser')
        resources = []

        # 提取CSS链接
        for link in soup.find_all('link', href=True):
            if link.get('rel') in [['stylesheet'], ['shortcut icon'], ['mask-icon']]:
                url = self._get_absolute_url(link['href'])
                if url:
                    resources.append(('link', url))

        # 提取JS脚本
        for script in soup.find_all('script', src=True):
            url = self._get_absolute_url(script['src'])
            if url:
                resources.append(('script', url))

        # 提取图片
        for img in soup.find_all('img', src=True):
            url = self._get_absolute_url(img['src'])
            if url:
                resources.append(('img', url))

        return resources, soup

    def convert(self, html_content, output_file):
        """转换为MHTML并保存"""
        resources, _ = self._extract_resources(html_content)

        # 下载资源（去重）
        for _, url in resources:
            if url not in [r[0] for r in self.resources]:
                content, mime_type = self._download_resource(url)
                if content:
                    self.resources.append((url, content, mime_type))

        # 构建MIME多部分消息
        mime_boundary = "----=_WeChatMHTMLBoundary_" + str(random.getrandbits(64))
        mhtml = MIMEMultipart('related', boundary=mime_boundary)
        mhtml['MIME-Version'] = '1.0'
        mhtml['Content-Type'] = f'multipart/related; boundary="{mime_boundary}"'

        # 添加HTML主内容
        html_part = MIMEText(html_content, 'html', 'utf-8')
        html_part.add_header('Content-Location', self.base_url)
        mhtml.attach(html_part)

        # 添加所有资源
        for url, content, mime_type in self.resources:
            main_type, sub_type = mime_type.split('/', 1) if '/' in mime_type else ('application', 'octet-stream')
            part = MIMEBase(main_type, sub_type)
            part.set_payload(content)
            encoders.encode_base64(part)
            part.add_header('Content-Location', url)
            part.add_header('Content-Transfer-Encoding', 'base64')
            mhtml.attach(part)

        # 保存文件
        with open(output_file, 'wb') as f:
            f.write(mhtml.as_bytes())
        print(f"MHTML已保存：{output_file}")


# --------------------------
# 3. 主函数：爬取+转换
# --------------------------
if __name__ == "__main__":
    # 目标微信公众号文章链接
    article_url = "https://mp.weixin.qq.com/s?src=11&timestamp=1754387510&ver=6156&signature=ifCPnB49Q0tlVvzyqE-RHEGPo1olkNFtNqfOnxAI2GnhUQxewOPDCMegZxa1tN-YlDJeMMpyCCCF6w2SZHl8RjcqkRyCEF42gwhxpGYwnlxhk*SCOQYoDQJZrp-ruk4n&new=1"

    # 1. 爬取文章HTML
    html_content = fetch_wechat_article(article_url)
    if not html_content:
        exit(1)

    # 2. 转换为MHTML
    base_url = "https://mp.weixin.qq.com"  # 基础URL用于解析相对路径
    converter = HTMLToMHTMLConverter(base_url)
    converter.convert(html_content, "wechat_article.mhtml")