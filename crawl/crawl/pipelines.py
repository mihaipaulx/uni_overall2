# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from scrapy.exceptions import DropItem

class FilterDepthPipeline:
    def process_item(self, item, spider):
        if item["depth"] > 2:
            raise DropItem(f"Item depth ({item['depth']}) is greater than 2")
        else:
            return item
