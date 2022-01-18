# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class OzbPipeline:
    wish_list = [
        'Nintendo',
        'LEGO',
        'Xiaomi',
        '3080'
        # 'Coles',
        # 'Woolworths'
    ]

    print(wish_list)

    def process_item(self, item, spider):
        for wish_item in OzbPipeline.wish_list:
            if(wish_item in item['name'] and item['tag'] is None):
                return item
            else:
                raise DropItem(f'Filter out non compliance item')

        
