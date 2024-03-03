# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from scrapy.exceptions import DropItem

class FilterDepthPipeline:
    def process_item(self, item, spider):
        if item['type'] == "tuition":
            return item
        else:
            # If the depth exceeds the maximum, you can either drop the item or handle it differently
            # For now, I'm just dropping the item
            raise DropItem("Item type is not tuition")