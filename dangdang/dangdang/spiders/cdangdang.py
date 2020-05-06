# -*- coding: utf-8 -*-

"""
爬取当当网的图书总榜单
爬取特别简单，当当网几乎没有任何反爬措施，只有一条，就是封ip
其中爬取下一页时，下一页按钮里的a标签的href是一个javascript方法，不好取
然后我就直接点击下一页，分析每次下一页的url，发现只是url里的一个代表页码的数字在变化
自己构建url
然后把数据存在了mysql里
建了两张表，
一个是只有书名和价格的简单表
一个是有书很多信息的细节表
"""


import scrapy
from scrapy import Request
from dangdang.items import Book
from dangdang.items import Detail
import re


def html(response):
    with open('{}.html'.format(response.url[8:].replace('.', '').replace('/', '').replace('?', '').replace('=', '')),
              'w', encoding='utf-8') as f:
        f.write(response.text)


class CdangdangSpider(scrapy.Spider):

    name = 'cdangdang'
    allowed_domains = ['book.dangdang.com/','bang.dangdang.com','www.dangdang.com','product.dangdang.com']
    start_urls = ['http://book.dangdang.com/']
    page_count = 1

    def parse(self, response):
        newbooks = response.xpath('//div[@class="book_new "]//a[@class="hot_link"]/@href').extract()[0]
        yield Request(newbooks,self.newbooks_parse)

    def newbooks_parse(self,response):
        books = response.xpath('//ul[contains(@class,"bang_list")]//div[@class="name"]//a/text()').extract()
        price = response.xpath('//ul[contains(@class,"bang_list")]//div[@class="price"]//span[@class="price_n"]/text()').extract()
        data = list(zip(books,price))
        book = Book()
        for i in data:
            book['name'] = i[0]
            book['price'] = i[1]
            yield book


        self.page_count += 1
        if self.page_count <= 50:
            print(self.page_count)
            next_page = re.sub('[^-]+$', '', response.url) + str(self.page_count)
            yield Request(next_page,self.newbooks_parse)

        detail = response.xpath('//ul[contains(@class,"bang_list")]//div[@class="name"]//a/@href').extract()
        for i in detail:
            yield Request(i,self.detail_parse)

    def detail_parse(self,response):
        detail = Detail()
        abstract = response.xpath('//span[@class="head_title_name"]/text()').extract()[0].strip()
        detail['abstract'] = abstract
        name = response.xpath('//div[@class="name_info"]/h1/@title').extract()[0]
        detail['name'] = name

        data=response.xpath('//p[@id="dd-price"]')
        text = data.xpath('string(.)').extract_first()
        price = text.strip()
        detail['price'] = price

        author = response.xpath('//span[@id="author"]/a/text()').extract()[0]
        detail['author'] = author

        pub = response.xpath('//span[@id="author"]/following-sibling::span[1]/a/text()').extract()[0]
        detail['pub'] = pub

        cover = response.xpath('//img[@id="largePic"]/@src').extract()[0]
        detail['cover'] = cover
        yield detail
