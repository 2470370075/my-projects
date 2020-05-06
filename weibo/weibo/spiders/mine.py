# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Request
import os

# 先爬取自己的主页，找到下一页并找到所有关注的人的uid，构造url

# 爬取某个用户主页的所有发布的照片，
# 多个分页都有爬，
# 每个分页请求分两部分，上部分图片信息直接存在页面下面的script标签里，下部分内容随着页面下滑再发新的请求获得
# 页码信息也在下部分响应数据中藏着，所以想取到并不容易，
# 所以开始只下载第一页，得到页码信息后重新返回self.parse进行所有分页的数据下载
# 取得图片id信息后，下载大图的url地址为'https://wx2.sinaimg.cn/mw690/' + img_id

# 访问太快返回414 429，在setting里加入DOWNLOAD_DELAY参数，只需0.5秒即可
# 但更好的方法是RETRY_HTTP_CODES = [429]
# AUTOTHROTTLE_ENABLED = True，自动限速，防止下载内容遗漏

def get_cookies(cookies_string):
    cookies_string = '; ' + cookies_string + ';'
    keys = re.findall('; (.*?)=', cookies_string)
    values = re.findall('=(.*?);', cookies_string)
    cookies = dict(zip(keys, values))
    return cookies


class ZhuyeSpider(scrapy.Spider):
    name = 'mine'
    allowed_domains = ['www.baidu.com', 'wx2.sinaimg.cn', 'wx1.sinaimg.cn', 'wx4.sinaimg.cn', 'wx3.sinaimg.cn',
                       'weibo.com']
    start_urls = ['https://weibo.com/5652790996/follow?from=page_100505&wvr=6&mod=headfollow#place']
    c = 0
    cookies = 'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W562vizmvqhwewD21Hd_LXF5JpX5KzhUgL.Fo-cSKzN1K541Kq2dJLoIXnLxK-LBKBL1-2LxK-L122LBKnLxK-L122LBKnLxKBLB.BLBK5LxKML1-2L1hBLxKML12eLB-2LxKnL1hBL1K2LxK-LB-BL1K5t; SINAGLOBAL=701068823940.0154.1585640119674; ULV=1587831509527:11:10:1:2476901335072.4434.1587831509523:1587804379365; SUHB=0qj0ScdZe_xFdh; ALF=1619367630; UOR=,,login.sina.com.cn; SCF=Asw-BG1MGL9O--w-SZ8DnwyPaOvAcGIizxzcxpbVfHs3tmPpDwfdoW_ciRrbaOojN2bXmBmKKSEqbinjH-tNy3M.; wvr=6; webim_unReadCount=%7B%22time%22%3A1587831530871%2C%22dm_pub_total%22%3A6%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A6%2C%22msgbox%22%3A0%7D; Ugrow-G0=7e0e6b57abe2c2f76f677abd9a9ed65d; SUB=_2A25zoBMfDeRhGeNI7lAW-S7FwjqIHXVQ1APXrDV8PUNbmtAKLRTEkW9NSE6jQQQ8gJtjFmqtoGJceDGTGw3Tcc1h; SSOLoginState=1587831630; _s_tentry=login.sina.com.cn; Apache=2476901335072.4434.1587831509523; TC-V5-G0=eb26629f4af10d42f0485dca5a8e5e20; TC-Page-G0=153ff31dae1cf71cc65e7e399bfce283|1587831650|1587831648; wb_view_log_5652790996=1536*8641.25'
    def start_requests(self):
        yield Request(
            self.start_urls[0],
            callback=self.parse,
            cookies=get_cookies(self.cookies)
        )

    def parse(self, response):

        uids = re.findall('uid=(\w+)&', response.text)
        next_page = re.findall('(?:href=)+(\S+Pl_Official_RelationMyfollow__95)', response.text)[0].replace('\\','')
        next_page_url = 'https://weibo.com/' + next_page
        yield Request(
            next_page_url,
            self.parse,
            cookies=get_cookies(self.cookies)
        )

        for i in list(set(uids)):
            homepage_url = 'https://weibo.com/u/' + i
            request = Request(homepage_url, self.homepage_parse, cookies=get_cookies(self.cookies))
            request.meta['uid'] = i
            request.meta['name'] = response.meta.get('name')
            yield request

    def homepage_parse(self, response):
        name = response.xpath('//title/text()').extract()[0]
        page = 1
        uid = response.meta.get('uid')
        page_count = response.meta.get('page_count')

        if page_count:
            page = page_count

        for i in range(1, page + 1):
            url = 'https://weibo.com/u/{}?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page={}#feedtop'.format(
                uid, i)
            print(url)
            request = Request(url,
                              self.img,
                              cookies=get_cookies(self.cookies),
                              headers={
                                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'},
                              )
            request.meta['name'] = name
            request.meta['uid'] = uid
            yield request

        for i in range(2):
            url = 'https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=2&pagebar={1}&pl_name=Pl_Official_MyProfileFeed__20&id=100505{0}&script_uri=/u/{0}&feed_type=0&pre_page=1&domain_op=100505&__rnd=1585971835384'.format(
                uid, i)
            for j in range(1, page + 1):
                url = re.sub('page=\d', 'page={}'.format(str(j)), url)
                print(url)
                request = Request(url,
                              self.img,
                              cookies=get_cookies(self.cookies)
                              )
                request.meta['name'] = name
                request.meta['uid'] = uid
                yield request

    def img(self, response):
        uid = response.meta.get('uid')
        page_count = re.findall('countPage=(\w)', response.text)
        print(page_count)
        imgs_data = re.findall('clear_picSrc=(.*?)&', response.text)
        img = re.findall('2F(.*?)(jpg|gif)', str(imgs_data))
        for i in img:
            img_id = ''.join(i).split('%2F')[-1]
            img_url = 'https://wx2.sinaimg.cn/mw690/' + img_id
            request = Request(img_url, self.img_down)
            request.meta['name'] = response.meta.get('name')
            request.meta['uid'] = uid
            yield request

        if page_count:
            url = 'https://weibo.com/u/' + uid
            request = Request(url, self.homepage_parse,dont_filter=True)
            request.meta['page_count'] = int(page_count[0])
            request.meta['name'] = response.meta.get('name')
            request.meta['uid'] = uid
            yield request

    def img_down(self, response):
        owner = response.meta.get('name')
        self.c += 1
        img_name = response.url.split('/')[-1]
        path = os.path.curdir  + '/imgs/'+ owner
        if not os.path.exists(path):
            os.makedirs(path)

        with open('{}/{}'.format(path,img_name), 'wb') as f:
            print(self.c)
            f.write(response.body)
