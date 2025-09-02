#在UrlLib模块下使用XPath表达式
import urllib.request
from lxml import etree
def urllib_to_xpath_parse():
    # 访问指定链接获取到对应的数据信息
    # etree.HTML(data) 的作用是将原始的HTML文本（字符串）转换为一个结构化的元素树（ElementTree）对象。
    # 这是后续使用XPath进行精准解析的前提。
    data = urllib.request.urlopen("http://www.baidu.com").read().decode("utf-8","ignore")
    tree_data = etree.HTML(data)
    # 使用XPath表达式获取到指定标签下的内容
    title = tree_data.xpath("//title/text()")
    if str(type(title)) == "<class 'list'>":
        pass
    else:
        # 遍历title，并赋值给title。转换成对应的列表
        title = [i for i in title]
    #     打印第一个元素
    print(title[0])

if __name__ == '__main__':
    urllib_to_xpath_parse()


