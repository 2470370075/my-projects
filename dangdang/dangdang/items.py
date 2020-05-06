# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Book(scrapy.Item):

    name = scrapy.Field()
    price = scrapy.Field()

class Detail(scrapy.Item):

    name = scrapy.Field()
    price = scrapy.Field()
    abstract = scrapy.Field()
    author = scrapy.Field()
    pub = scrapy.Field()
    cover = scrapy.Field()