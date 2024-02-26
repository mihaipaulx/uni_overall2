# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class LinkItem(scrapy.Item):
    url = scrapy.Field()
    type = scrapy.Field()
    keyword = scrapy.Field()
    depth = scrapy.Field()