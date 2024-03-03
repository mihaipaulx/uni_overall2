# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from scrapy.exceptions import DropItem

class FilterDepthPipeline:
    def __init__(self, max_depth=2):
        self.max_depth = max_depth

    def process_item(self, item, spider):
        if item['depth'] <= self.max_depth:
            return item
        else:
            # If the depth exceeds the maximum, you can either drop the item or handle it differently
            # For now, I'm just dropping the item
            raise DropItem(f"Depth {item['depth']} exceeds maximum depth of {self.max_depth}")

class PrintPipeline:
    def process_item(self, item, spider):
        print(item)
        return item