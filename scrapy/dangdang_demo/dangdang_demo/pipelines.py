# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import traceback

import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DangdangDemoPipeline:
    def process_item(self, item, spider):
        # 连接数据库
        connect = pymysql.connect(host="127.0.0.1",user="root",password="jfkjyfb",db="dangdang_spider")
        try:
            cursor = connect.cursor()
            # 循环遍历，输出数据
            # 按title元组的长度来进行遍历，相当于一页的数据有len(item["title"])条
            for i in range(0,len(item["title"])):
                title = item["title"][i]
                price = item["price"][i]
                comment_num = item["comment_num"][i]
                link = item["link"][i]
                # print(title+":"+price)
                sql = "INSERT INTO `goods`(`title`, `price`, `comment_num`, `link`) VALUES (%s, %s, %s, %s);"
                # print(sql)
                # 使用这种方法执行SQL，需要注意手动提交事务，不然数据不能正常地被插入到数据库中。
                cursor.execute(sql, (title, price, comment_num, link))
            # 提交事务，插入数据
            connect.commit()
        except Exception as e:
            print("插入数据时出错:", e)
            # 打印完整的堆栈跟踪
            traceback.print_exc()  # ✅ 关键方法：输出完整异常堆栈
            connect.rollback()  # 出现异常回滚
        finally:
            cursor.close()
            connect.close()
        return item
