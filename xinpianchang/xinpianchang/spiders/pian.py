# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Request
import json
from xinpianchang.items import Info              #info表
from xinpianchang.items import Mp4_url           #mp4表
from xinpianchang.items import Comments          #com表

# 主要运用了pipeline，数据库，
# 返回三个item，分开通过pipline存入数据库，info一对一mp4，一对多com，
# info是视频主要信息表，mp4是视频地址等其他信息表，com是多个评论表

def get_cookies(cookies_string):
    cookies_string = '; '+cookies_string+';'
    keys = re.findall('; (.*?)=',cookies_string)
    values = re.findall('=(.*?);',cookies_string)
    cookies = dict(zip(keys,values))
    return cookies

cookies = 'Device_ID=5e6f789fa857d; _ga=GA1.2.244836811.1584363560; UM_distinctid=170e36d5b8d7ba-051b3896e99926-3a36540e-144000-170e36d5b8e13c; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22170e36d5b5c575-0b6fa03b487d5b-3a36540e-1327104-170e36d5b5d17d%22%2C%22%24device_id%22%3A%22170e36d5b5c575-0b6fa03b487d5b-3a36540e-1327104-170e36d5b5d17d%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; Authorization=60947BB885A6CB9D285A6C4F2285A6CBD9F85A6C85CB6A5A5B41; PHPSESSID=v8loej01hq5k6a1ceehtjv91se; SERVER_ID=b52601c8-5caf45c0; Hm_lvt_dfbb354a7c147964edec94b42797c7ac=1584707534,1584790850,1586700070,1586953566; CNZZDATA1262268826=1253962270-1584359150-https%253A%252F%252Fwww.baidu.com%252F%7C1586949053; _gid=GA1.2.279411973.1586953566; _gat=1; Hm_lpvt_dfbb354a7c147964edec94b42797c7ac=1586953578; cn_1262268826_dplus=%7B%22distinct_id%22%3A%20%22170e36d5b8d7ba-051b3896e99926-3a36540e-144000-170e36d5b8e13c%22%2C%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201586953597%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201586953597%7D'

class PianSpider(scrapy.Spider):
    name = 'pian'
    allowed_domains = ['app.xinpianchang.com','www.xinpianchang.com','openapi-vtom.vmovier.com']
    start_urls = ['https://www.xinpianchang.com/channel/index/sort-like?from=navigator']

    def parse(self, response):
        videos = response.xpath('//li[@class="enter-filmplay"]/@data-articleid').extract()
        for i in videos:
            url = 'https://www.xinpianchang.com/a{}?from=ArticleList'.format(i)
            resquest = Request(url,self.parse_video,)
            resquest.meta['pid'] = i
            yield resquest

        pages = response.xpath('//div[@class="page"]//a/@href').extract()
        for page in pages:
            yield response.follow(page,self.parse,cookies=get_cookies(cookies))


    def parse_video(self,response):
        post = Info()
        post['cururl'] = response.url
        r = re.compile('vid: "(\w+)",')
        video_id = r.findall(response.text)
        post['name'] = response.xpath('//h3/text()').extract_first()
        tags = response.xpath('//span[contains(@class,"cate")]//text()').extract()
        post['tag'] = ''.join([i.strip() for i in tags])
        post['uptime'] = response.xpath('//span[contains(@class,"update-time")]//text()').extract()
        # post['play_count'] = response.xpath('//i[contains(@class,"play-counts")]//text()').extract()
        desc = response.xpath('//p[contains(@class,"desc")]//text()').extract_first()
        if desc == None:
            desc = ''
        post['des'] = desc.strip()
        video_request = 'https://openapi-vtom.vmovier.com/v3/video/{}?expand=resource&usage=xpc_web'.format(video_id[0])
        request = Request(video_request,callback=self.video_mp4,dont_filter=False)
        request.meta['post'] = post
        yield post
        yield request
    #
        comments_url = 'https://app.xinpianchang.com/comments?resource_id={}&type=article&page=1&per_page=24'.format(response.meta['pid'])
        request = Request(comments_url,callback=self.comments_parse)
        request.meta['post'] = post
        yield request
    #
    def video_mp4(self,response):
        mp4 = Mp4_url()
        post = response.meta['post']
        data = json.loads(response.text)
        video_mp4 = re.findall("'url': '(.*?)'",str(data))[1]
        cover = data['data']['video']['cover']
        mp4['name'] = post['name']
        mp4['cover'] = cover
        mp4['url'] = video_mp4
        yield mp4
    #
    #
    def comments_parse(self,response):
        com = Comments()
        post = response.meta['post']
        if post.get('comments'):
            l = post['comments']
        else:
            l = []
        data = json.loads(response.text)
        for i in data['data']['list']:
            l.append(i['content'])
        com['name'] = post['name']
        com['comments'] = l
        next_page = data['data']['next_page_url']
        if next_page:
            next_page ='https://app.xinpianchang.com'+ next_page
            request = Request(next_page,self.comments_parse)
            request.meta['post'] = post
            yield request
        else:
            yield com


