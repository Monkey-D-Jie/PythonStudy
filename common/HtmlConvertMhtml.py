import re
import requests
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from urllib.parse import urljoin, urlparse

class HTMLToMHTMLConverter:
    def __init__(self, base_url):
        """
        初始化转换器
        :param base_url: HTML对应的基础URL（用于解析相对路径）
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": base_url
        }
        self.resources = []  # 存储所有资源 (url, content, mime_type)

    def _get_absolute_url(self, relative_url):
        """将相对URL转换为绝对URL"""
        if not relative_url:
            return None
        # 处理//开头的URL（协议相对URL）
        if relative_url.startswith('//'):
            parsed_base = urlparse(self.base_url)
            return f"{parsed_base.scheme}:{relative_url}"
        return urljoin(self.base_url, relative_url)

    def _download_resource(self, url):
        """下载资源并返回内容和MIME类型"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            mime_type = response.headers.get('Content-Type', 'application/octet-stream').split(';')[0]
            return response.content, mime_type
        except Exception as e:
            print(f"警告：无法下载资源 {url}，错误：{str(e)}")
            return None, None

    def _extract_resources(self, html_content):
        """从HTML中提取所有外部资源链接"""
        soup = BeautifulSoup(html_content, 'html.parser')
        resources = []

        # 提取CSS链接
        for link in soup.find_all('link', href=True):
            if link.get('rel') in [['stylesheet'], ['shortcut icon'], ['mask-icon'], ['apple-touch-icon-precomposed']]:
                url = self._get_absolute_url(link['href'])
                if url:
                    resources.append(('link', url, link))

        # 提取JS脚本
        for script in soup.find_all('script', src=True):
            url = self._get_absolute_url(script['src'])
            if url:
                resources.append(('script', url, script))

        # 提取图片
        for img in soup.find_all('img', src=True):
            url = self._get_absolute_url(img['src'])
            if url:
                resources.append(('img', url, img))

        return resources, soup

    def convert(self, html_content, output_file):
        """转换HTML为MHTML并保存到文件"""
        # 提取资源并下载
        resources, soup = self._extract_resources(html_content)
        for _, url, _ in resources:
            # 去重
            if url not in [r[0] for r in self.resources]:
                content, mime_type = self._download_resource(url)
                if content:
                    self.resources.append((url, content, mime_type))

        # 构建MIME多部分消息
        mime_boundary = "----=_NextPart_000_0000_0123456789ABCDEF"
        mhtml = MIMEMultipart('related', boundary=mime_boundary)
        mhtml['MIME-Version'] = '1.0'
        mhtml['Content-Type'] = f'multipart/related; boundary="{mime_boundary}"'

        # 添加HTML主文档
        html_part = MIMEText(html_content, 'html', 'utf-8')
        html_part.add_header('Content-Location', self.base_url)
        mhtml.attach(html_part)

        # 添加所有资源
        for url, content, mime_type in self.resources:
            part = MIMEBase(mime_type.split('/')[0], mime_type.split('/')[1])
            part.set_payload(content)
            encoders.encode_base64(part)
            part.add_header('Content-Location', url)
            part.add_header('Content-Transfer-Encoding', 'base64')
            mhtml.attach(part)

        # 写入文件
        with open(output_file, 'wb') as f:
            f.write(mhtml.as_bytes())
        print(f"MHTML文件已保存至：{output_file}")


# 使用示例
if __name__ == "__main__":
    # 你的HTML内容（可以从文件读取或直接传入）
    with open("mhtml前的html内容.txt", "r", encoding="utf-8") as f:
        html_content = f.read()

    # 基础URL（根据HTML来源设置，此处以微信公众号为例）
    base_url = "https://mp.weixin.qq.com"

    # 转换并保存
    converter = HTMLToMHTMLConverter(base_url)
    converter.convert(html_content, "output.mht")