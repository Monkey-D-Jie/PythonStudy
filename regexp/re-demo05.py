#正则表达式初识-常见正则实例
import re
'''
匹配.com和.cn网址
'''
# 1.match
string="<a href='https://www.baidu.com'>百度首页</a>"
pat="[a-zA-Z]+://[^\s]*[.com|cn]"
rst=re.compile(pat).findall(string)
print(rst)
#匹配电话号码
string="asdfasdfasdf021-78887889787fasdfasdfasdfasdfasdfasdfasdfasdfaf028-1234567734564564dfasddgfsdfgsdfgsdfgsdfgsdfgsdf"
pat="\d{4}-\d{7}|\d{3}-\d{8}"
rst=re.compile(pat).findall(string)
print(rst)