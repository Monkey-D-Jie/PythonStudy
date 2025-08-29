# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
# 使用相对导入
# from ...common.db_utils import insert_data_to_table
from common.db_utils import insert_data_to_table


class BaidunewsDemoPipeline:
    def process_item(self, item, spider):
        # print("当期获取到的item---->>>>>>>>",item)
        # 调用公共模块方法
        news_field_map = {
            "classify": "classify",
            "classify_name":"classify_name",
            "title": "title",
            "m_text": "m_text",
            "link": "link",
            "content": "content",
            "img_url": "img_url"
        }
        insert_data_to_table(item, "baidu_news",news_field_map)
        return item
