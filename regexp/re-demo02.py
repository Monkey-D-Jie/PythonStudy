#正则表达式初识-元字符
'''
. 除换行符外的任意一个字符
^ 开始位置
$ 结束位置
* 0/1/多次
? 0/1次
+ 1/多次*
{n} 恰好n次
{n+} 至少n次
{n,m} 至少n次，至多m次
| 模式选择符 或
() 分组
'''
import re
text = "cat cbt c9t cut ct"
print(re.findall(r"c.t",text))

text = "apple"
print(re.findall(r"^a....",text))

text = "file1"
text2 = "data2"
text3 = "image.jpg"
print(re.findall(r"\d$",text))
print(re.findall(r"\d$",text2))
print(re.findall(r"\d$",text3))

text = "jiafajiaoyu"
print(re.findall(r"jiafa.*",text))
text = "aaab aab cd"
print(re.findall(r"a.*",text))

text = "a1b2"
print(re.search(r"\d+",text))

patterns = [
    r"colou?r",     # ? 匹配0或1个u (color/colour)
    r"go*gle",      # * 匹配0或多个o (ggle/gogle/google)
    r"wo+w",        # + 匹配1或多个o (wow/woooow)
    r"hi{3}",       # {n} 精确匹配 (hiii)
    r"ha{2,4}"      # {n,m} 范围匹配 (haa/haaa/haaaa)
]
test_cases = ["color", "colour", "ggle", "google", "wow", "woooow", "hiii", "haa", "haaaa"]
for pattern in patterns:
    print(f"\n Pattern:{pattern}")
    for test in test_cases:
        if(re.search(pattern,test)):
            print(f"---> {test}")
pattern = r"(apple|orange) juice"  # 匹配apple juice或orange juice
test_cases = [
    "I like apple juice",
    "orange juice is fresh",
    "banana juice is yellow"
]
for test in test_cases:
    match = re.search(pattern,test)
    print(f"{test}:{'Match('+match.group(1)+')' if match else 'No match'}")
pattern = r"^\d{4}[-/]\d{2}[-/]\d{2}$"  # YYYY-MM-DD 或 YYYY/MM/DD
test_cases = [
    "2023-08-15",
    "1999/12/31",
    "01/01/2023",
    "2023-8-05"
]
for test in test_cases:
    print(f"{test}: {'Valid' if re.match(pattern, test) else 'Invalid'}")
pattern = r"\bcat\b"  # 精确匹配单词"cat"
test_cases = [
    "I have a cat",
    "category is important",
    "concatenate strings",
    "wildcat"
]
for test in test_cases:
    print(f"{test}: {'Match' if re.search(pattern, test) else 'No match'}")

# 邮箱验证（简化版）
email_pattern = r"^\w+@\w+\.[a-z]{2,3}$"

# 手机号匹配（中国大陆）
phone_pattern = r"^1[3-9]\d{9}$"

# HTML标签匹配（基础）
html_pattern = r"<([a-z]+)>(.*?)</\1>"