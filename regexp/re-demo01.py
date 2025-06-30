#正则表达式初识
import re
string="jiafajiaoyuzhengzhengrishang"
#这里的pattern就叫做原子，此处是以普通字符作为原子
pattern="zhe"
rst = re.search(pattern,string)
print(rst)
#非打印字符作为原子
#比如 \n-换行符，\t-制表符，等等
str='''jiafajiaoyu
honghonghuohuo
'''
pat = "\n"
rst = re.search(pat,str)
print(rst)
#通用字符作为原子
'''
\w 字符、数字、下划线
\W 除字符、数字、下划线的其他字符
\d 十进制数字
\D 除十进制数字外的其他数字
\s 空白字符
\S 除空白字符的其他字符
'''
string='''jiafajiaoyu3 00559honghonghuohuo'''
pat="\w\s\d\d\d\d"
rst=re.search(pat,string)
print(rst)
#原子表.表示匹配的是原子表中的任意一个元素。如果加上了一个“^”符号，则表示需要配出掉原子表中指定到的元素。
string="jiafajiaoyugufenyouxiangongsi"
pat="jiaoyu[^gu]"
rst=re.search(pat,string)
print(rst)