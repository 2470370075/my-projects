# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Info(scrapy.Item):
    cururl = scrapy.Field()
    name = scrapy.Field()
    tag = scrapy.Field()
    uptime = scrapy.Field()
    des = scrapy.Field()


class Mp4_url(scrapy.Item):
    name = scrapy.Field()

    url = scrapy.Field()
    cover = scrapy.Field()

class Comments(scrapy.Item):
    name = scrapy.Field()

    comments = scrapy.Field()