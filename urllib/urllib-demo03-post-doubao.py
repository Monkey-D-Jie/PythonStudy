import requests
from bs4 import BeautifulSoup

# 目标URL
url = "https://baidu.com"  # 替换成实际的目标URL

# POST请求的参数
data = {
    "username": "18581514809",
    "password": "123456",
    "csrf_token": "xxx"  # 如果网站需要CSRF令牌，要从页面获取
}

# 设置请求头，模拟浏览器访问
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Referer": "https://example.com",  # 替换成实际的来源URL
    "Content-Type": "application/x-www-form-urlencoded"
}

try:
    # 先发送GET请求获取CSRF令牌（如果需要）
    session = requests.Session()
    response = session.get(url)

    # 从响应中提取CSRF令牌（如果有）
    # 下面是一个示例，具体的提取方式要依据网站实际情况调整
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
    data['csrf_token'] = csrf_token

    # 发送POST请求
    response = session.post(url, data=data, headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
        # 请求成功
        print("请求成功")

        # 解析响应内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取需要的信息
        # 下面是一个示例，具体的提取方式要根据网站结构调整
        items = soup.find_all('div', class_='item')
        for item in items:
            title = item.find('h3').text
            description = item.find('p').text
            print(f"标题: {title}")
            print(f"描述: {description}")
            print("-" * 50)

        # 保存响应内容到文件
        with open('response.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("响应内容已保存到response.html")
    else:
        print(f"请求失败，状态码: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"请求异常: {e}")
except Exception as e:
    print(f"发生错误: {e}")