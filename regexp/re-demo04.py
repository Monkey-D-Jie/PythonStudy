#正则表达式初识-正则表达式函数
import re
'''
常见的主要包括以下几种
re.match()
re.search()
findAll
re.sub()
'''
# 1.match
string="pythonpythonpythonpythonpythonpython"
pat="p.*?n"
rst=re.match(pat,string,re.I)
print(f"{rst}")
rst=re.compile(pat).findall(string)
print(rst)