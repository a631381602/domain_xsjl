# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class So360Item(scrapy.Item):
    # define the fields for your item here like:
    word = scrapy.Field()
    bd_index = scrapy.Field()
    daopai = scrapy.Field()
    sr = scrapy.Field()
    score = scrapy.Field()
    pass
