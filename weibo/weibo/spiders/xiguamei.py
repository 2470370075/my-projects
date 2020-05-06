# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import os


class XiguameiSpider(scrapy.Spider):
    name = 'xiguamei'
    allowed_domains = ['wx2.sinaimg.cn', 'wx1.sinaimg.cn', 'wx4.sinaimg.cn', 'wx3.sinaimg.cn', 'weibo.com']
    start_urls = ['https://weibo.com/272757325?from=myfollow_no-group/']

    def start_requests(self):
        yield Request(
            self.start_urls[0],
            callback=self.parse,
            cookies={
                'SUB': '_2AkMp3nO1f8NxqwJRmP4VzGjjbY1wyAjEieKfgoJuJRMxHRl-yT9jqmpftRB6Al5dWnP2kwgsf8WreUmZ_S--o9R_1VBm',
                'SUBP': '0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5U4kFCu..K1W8dVMH0JsJk',
                '_s_tentry': 'passport.weibo.com',
                'Apache': '1419321109996.3276.1585642509165',
                'SINAGLOBAL': '1419321109996.3276.1585642509165',
                'ULV': '1585642509301:1:1:1:1419321109996.3276.1585642509165',
                'TC-Page-G0': '7a922a70806a77294c00d51d22d0a6b7|1585642712|1585642627'
            }
        )

    def parse(self, response):
        url = """https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=2&pagebar=1&pl_name=Pl_Official_MyProfileFeed__21&id=1005053063609231&script_uri=/272757325&pre_page=3&domain_op=100505"""
        yield Request(url, self.img)
        # info = response.xpath('//div').extract()
        # print(info)

    def img(self, response):
        data = response.text
        imgs_url = re.findall("img src=(.*?.jpg)", data)
        for i in imgs_url:
            img = 'https:/' + i[5:].replace('\\', '')
            print(img)
            yield Request(img, self.img_down)

    def img_down(self, response):
        path = os.path.curdir + '/imgs'
        if not os.path.exists(path):
            os.makedirs(path)

        with open('{}/{}'.format(path, response.url[-20:]), 'wb') as f:
            f.write(response.body)
