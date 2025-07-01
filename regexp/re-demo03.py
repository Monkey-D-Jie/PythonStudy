#正则表达式初识-模式修正符
import re
'''
I 匹配时葫芦大小写
M 多行匹配
L 本地化识别匹配,py3.6+版本已经弃用
S 让.匹配包括换行符
'''
pattern = r"pyt"  #匹配pyt,不区分大小写
test_cases = [
    "python",
    "Python",
    "pig",
    "patch"
]
for test in test_cases:
    print(f"{test}: {'Valid' if re.search(pattern, test,re.I) else 'Invalid'}")

text = "Python is powerful. PYTHON is versatile. python is easy to learn."
# 不使用忽略大小写
matches1 = re.findall(r"python", text)
print("不使用re.I:", matches1)  # 只匹配小写

# 使用忽略大小写
matches2 = re.findall(r"python", text, re.I)
print("使用re.I:", matches2)  # 匹配所有变体

# 内联方式 (?i)
matches3 = re.findall(r"(?i)python", text)
print("内联(?i):", matches3)

text = """
First line
Second line starts with 123
Third line
404: Not Found on fourth line
Last line
"""
# 不使用多行模式 - ^只匹配整个字符串开头
matches1 = re.findall(r"^\d+", text)
print("不使用re.M:", matches1)  # 无匹配

# 使用多行模式 - ^匹配每行开头
matches2 = re.findall(r"^\d+", text, re.M)
print("使用re.M:", matches2)  # 匹配第四行的404

# 查找每行结尾的数字
matches3 = re.findall(r"\d+$", text, re.M)
print("行尾数字:", matches3)  # 匹配第二行的123

# 内联方式 (?m)
matches4 = re.findall(r"(?m)^\w+", text)
print("行首单词:", matches4)  # 每行第一个单词

html_content = """
<html>
<head><title>Test Page</title></head>
<body>
  <div>Content Section</div>
</body>
</html>
"""

# 不使用dotall - 点号不匹配换行符
match1 = re.search(r"<title>.*</title>", html_content)
print("不使用re.S:", match1.group() if match1 else "无匹配")

# 使用dotall - 点号匹配换行符
match2 = re.search(r"<title>.*</title>", html_content, re.S)
print("使用re.S:", match2.group() if match2 else "无匹配")

# 提取整个body内容（跨多行）
body_content = re.search(r"<body>(.*?)</body>", html_content, re.S)
print("Body内容:", body_content.group(1).strip() if body_content else "无匹配")

# 内联方式 (?s)
match3 = re.search(r"(?s)<div>(.*?)</div>", html_content)
print("Div内容:", match3.group(1) if match3 else "无匹配")

# 输出:
# 不使用re.S: <title>Test Page</title>
# 使用re.S: <title>Test Page</title>
# Body内容: <div>Content Section</div>
# Div内容: Content Section


text = """Names:
- ALICE
- Bob
- charlie
- diana"""
# 组合使用re.I和re.M
matches = re.findall(r"^-\s*(\w+)", text, re.I | re.M)
print("所有名字:", matches)  # 忽略大小写+多行模式

# 内联组合方式 (?im)
matches2 = re.findall(r"(?im)^-\s*(\w+)", text)
print("内联组合:", matches2)

# 输出:
# 所有名字: ['ALICE', 'Bob', 'charlie', 'diana']
# 内联组合: ['ALICE', 'Bob', 'charlie', 'diana']

log_data = """
[ERROR] 2023-08-15 10:30:45 - Connection timeout
[WARN] 2023-08-15 10:31:22 - Disk space low
[INFO] 2023-08-15 10:32:01 - Backup completed
[error] 2023-08-15 11:45:33 - Authentication failed
"""

# 提取所有错误日志（忽略大小写+多行模式）
errors = re.findall(r"^\[error\].*$", log_data, re.I | re.M)
print("所有错误日志:")
for error in errors:
    print("-", error)

# 提取时间范围内的日志
aug_errors = re.findall(r"^\[.*?] 2023-08-15 1[0-2]:.*$", log_data, re.M)
print("\n上午的错误日志:")
for log in aug_errors:
    print("-", log)

# 输出:
# 所有错误日志:
# - [ERROR] 2023-08-15 10:30:45 - Connection timeout
# - [error] 2023-08-15 11:45:33 - Authentication failed
#
# 上午的错误日志:
# - [ERROR] 2023-08-15 10:30:45 - Connection timeout
# - [WARN] 2023-08-15 10:31:22 - Disk space low
# - [INFO] 2023-08-15 10:32:01 - Backup completed

#贪婪模式与懒惰模式
string="jiafajiaoyu"
pat1="jia.*a"#贪婪模式
pat2="jia.*?a"#懒惰模式，精准
rst1=re.search(pat1,string,re.I)
rst2=re.search(pat2,string,re.I)
print(rst1)
print(rst2)
# 基础示例：提取HTML标签内容
html = "<div>Content 1</div><div>Content 2</div>"
# 贪婪模式 - 默认
greedy_match = re.search(r"<div>(.*)</div>", html)
print("贪婪模式:", greedy_match.group(1))  # "Content 1</div><div>Content 2"

# 懒惰模式 - 添加?
lazy_match = re.search(r"<div>(.*?)</div>", html)
print("懒惰模式:", lazy_match.group(1))  # "Content 1"

# 提取引号内的内容
text = 'John said: "Hello" and Mary said: "Hi"'

# 贪婪模式
greedy_quotes = re.findall(r'"(.*)"', text)
print("贪婪模式提取:", greedy_quotes)  # ['Hello" and Mary said: "Hi']

# 懒惰模式
lazy_quotes = re.findall(r'"(.*?)"', text)
print("懒惰模式提取:", lazy_quotes)  # ['Hello', 'Hi']

# 提取URL参数
url = "https://example.com?name=John&age=30&city=NY"
# 贪婪模式 - 错误提取
greedy_param = re.findall(r'&(.+)', url)
print("贪婪参数提取:", greedy_param)  # ['age=30&city=NY']

# 懒惰模式 - 正确提取
lazy_param = re.findall(r'&(.+?)&', url)
print("懒惰参数提取:", lazy_param)  # ['age=30']

# 更好的方式 - 使用非捕获组
all_params = re.findall(r'(?:\?|&)([^&]+)', url)
print("所有参数:", all_params)  # ['name=John', 'age=30', 'city=NY']

log_data = """
[Start] Item 1 [End]
[Start] Item 2 [End]
[Start] Item 3 [End]
"""

# 贪婪模式 - 匹配所有内容
greedy_items = re.findall(r'\[Start\](.*)\[End\]', log_data, re.DOTALL)
print("贪婪模式匹配项数:", len(greedy_items))  # 1 - 整个文本

# 懒惰模式 - 正确匹配每个项目
lazy_items = re.findall(r'\[Start\](.*?)\[End\]', log_data, re.DOTALL)
print("懒惰模式匹配项数:", len(lazy_items))  # 3 - 每个项目
print("第一个项目:", lazy_items[0].strip())  # "Item 1"