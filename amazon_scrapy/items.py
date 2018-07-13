# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class AmazonScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    am_asin = scrapy.Field()
    am_name = scrapy.Field()
    am_stock = scrapy.Field()
    am_price = scrapy.Field()
    am_price_shipping = scrapy.Field()
    am_condition = scrapy.Field()
    am_delivery = scrapy.Field()
    pass
