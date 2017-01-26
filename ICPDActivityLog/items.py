# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IcpdactivitylogItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    dispatch = scrapy.Field()
    inc = scrapy.Field()
    activity = scrapy.Field()
    disposition = scrapy.Field()
    addr = scrapy.Field()
    apt = scrapy.Field()
    time = scrapy.Field()
    date = scrapy.Field()

class IcpdScrapedBody(scrapy.Item):
    url = scrapy.Field()
    body = scrapy.Field()

class IcpdScrapedDetail(scrapy.Item):
    dispatch = scrapy.Field()
    details = scrapy.Field()

