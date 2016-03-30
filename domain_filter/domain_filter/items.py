# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DomainFilterItem(scrapy.Item):
    domain = scrapy.Field()
    bd_index = scrapy.Field()
    reverse_index = scrapy.Field()
    chinese = scrapy.Field()
    pan_analysis = scrapy.Field()
    illegal = scrapy.Field()
    sgsr = scrapy.Field()
    current_time = scrapy.Field()
    url = scrapy.Field()
    pass
