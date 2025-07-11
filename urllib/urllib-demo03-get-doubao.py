import urllib.request
from urllib.parse import quote
from bs4 import BeautifulSoup
import time
import random
import re

# 设置请求头，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
}


def get_search_results(keyword, page=1):
    """获取百度搜索结果"""
    # 百度搜索URL，添加pn参数表示页码，每页10条结果
    # 使用quote函数对关键词进行URL编码
    encoded_keyword = quote(keyword)
    url = f"https://www.baidu.com/s?wd={encoded_keyword}&pn={str((page - 1) * 10)}"

    try:
        # 创建请求对象，添加请求头
        req = urllib.request.Request(url, headers=headers)

        # 发送HTTP请求
        with urllib.request.urlopen(req, timeout=10) as response:
            # 检查响应状态码
            if response.status == 200:
                # 随机等待1-3秒，避免请求过于频繁
                time.sleep(random.uniform(1, 3))

                # 读取响应内容并解码
                html_content = response.read().decode('utf-8', errors='ignore')

                # 使用BeautifulSoup解析HTML内容
                soup = BeautifulSoup(html_content, 'html.parser')

                # 提取搜索结果
                results = []

                # 尝试多种可能的CSS选择器组合，提高兼容性
                result_selectors = [
                    '.result.c-container',  # 常规搜索结果
                    '.c-container',  # 简化版搜索结果
                    '.t a'  # 直接选择标题链接
                ]

                for selector in result_selectors:
                    result_items = soup.select(selector)
                    if len(result_items) > 0:
                        print(f"使用选择器 '{selector}' 找到 {len(result_items)} 条结果")

                        for item in result_items:
                            title = ""
                            link = ""

                            if selector == '.t a':
                                # 直接选择标题链接的情况
                                title = item.get_text(strip=True)
                                link = item.get('href', '')
                            else:
                                # 其他选择器的情况
                                title_element = item.select_one('h3 a') or item.select_one('a')
                                if title_element:
                                    title = title_element.get_text(strip=True)
                                    link = title_element.get('href', '')

                            if title and link:
                                # 处理百度的跳转链接，提取真实URL
                                if 'baidu.com/link?' in link:
                                    try:
                                        # 发送HEAD请求获取真实URL
                                        head_req = urllib.request.Request(link, headers=headers, method='HEAD')
                                        with urllib.request.urlopen(head_req, timeout=5) as real_url_response:
                                            real_url = real_url_response.geturl()
                                    except:
                                        real_url = link
                                    results.append({
                                        'title': title,
                                        'url': real_url
                                    })
                                else:
                                    results.append({
                                        'title': title,
                                        'url': link
                                    })

                        # 如果找到了结果，就不再尝试其他选择器
                        if len(results) > 0:
                            break

                return results
            else:
                print(f"请求失败，状态码：{response.status}")
                return []

    except urllib.error.URLError as e:
        print(f"URL错误：{e}")
        return []
    except Exception as e:
        print(f"发生错误：{e}")
        return []


def main():
    # 搜索关键词
    keyword = "灵笼"

    print(f"开始搜索关于 '{keyword}' 的百度搜索结果...")

    # 获取前3页的搜索结果
    all_results = []
    for page in range(1, 4):
        print(f"\n正在获取第 {page} 页搜索结果...")
        page_results = get_search_results(keyword, page)
        all_results.extend(page_results)
        print(f"第 {page} 页获取到 {len(page_results)} 条结果")

    # 输出结果
    print(f"\n总共获取到 {len(all_results)} 条关于 '{keyword}' 的搜索结果：")
    for i, result in enumerate(all_results, 1):
        print(f"{i}. {result['title']}")
        print(f"   {result['url']}")
        print("-" * 80)


if __name__ == "__main__":
    main()