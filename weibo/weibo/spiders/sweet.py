# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import os

def get_cookies(cookies_string):
    cookies_string = '; '+cookies_string+';'
    keys = re.findall('; (.*?)=',cookies_string)
    values = re.findall('=(.*?);',cookies_string)
    cookies = dict(zip(keys,values))
    return cookies

class SweetSpider(scrapy.Spider):
    name = 'sweet'
    allowed_domains = ['www.baidu.com','wx2.sinaimg.cn', 'wx1.sinaimg.cn', 'wx4.sinaimg.cn', 'wx3.sinaimg.cn', 'weibo.com']
    start_urls = ['https://weibo.com/u/1116218960?from=myfollow_all/']
    c = 0

    def start_requests(self):
        yield Request(
            self.start_urls[0],
            callback=self.parse,
            cookies=get_cookies(
                'SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5U4kFCu..K1W8dVMH0JsJk; _s_tentry=passport.weibo.com; Apache=1419321109996.3276.1585642509165; SINAGLOBAL=1419321109996.3276.1585642509165; ULV=1585642509301:1:1:1:1419321109996.3276.1585642509165:; TC-V5-G0=eb26629f4af10d42f0485dca5a8e5e20; Ugrow-G0=e1a5a1aae05361d646241e28c550f987; WBtopGlobal_register_version=3d5b6de7399dfbdb; UOR=,,login.sina.com.cn; SUB=_2AkMp36vlf8NxqwJRmP4VzGjjbY1wyAjEieKfg1o-JRMxHRl-yj9jqhEStRB6Al-FClx5SdU4cd62GLMJoy-wnduvFMJV; TC-Page-G0=b993e9b6e353749ed3459e1837a0ae89|1585652986|1585652828')
        )

    def parse(self, response):
        page = 1
        page_count = response.meta.get('page_count')

        if page_count:
            page = page_count

        for i in range(1,page+1):
            url = 'https://weibo.com/u/1116218960?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page={}#feedtop'.format(i)
            print(url)
            request = Request(url,
                              self.img,
                              cookies=get_cookies('SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W562vizmvqhwewD21Hd_LXF5JpX5KzhUgL.Fo-cSKzN1K541Kq2dJLoIXnLxK-LBKBL1-2LxK-L122LBKnLxK-L122LBKnLxKBLB.BLBK5LxKML1-2L1hBLxKML12eLB-2LxKnL1hBL1K2LxK-LB-BL1K5t; SINAGLOBAL=701068823940.0154.1585640119674; ULV=1585913256679:4:3:4:8918207104638.07.1585913256641:1585839353012; SUHB=0wn1neYy4wE-2A; ALF=1617449482; UOR=,,login.sina.com.cn; wvr=6; SUB=_2A25zg27aDeRhGeNI7lAW-S7FwjqIHXVQ-ccSrDV8PUNbmtAKLUj4kW9NSE6jQZTf0PboPw9e_wD-QgMN--0yVGuE; login_sid_t=7b70eac7c98859f5b55cbee14425a00b; cross_origin_proto=SSL; Ugrow-G0=7e0e6b57abe2c2f76f677abd9a9ed65d; TC-V5-G0=595b7637c272b28fccec3e9d529f251a; WBStorage=42212210b087ca50|undefined; _s_tentry=www.baidu.com; Apache=8918207104638.07.1585913256641; wb_view_log=1536*8641.25; SSOLoginState=1585913482; TC-Page-G0=62b98c0fc3e291bc0c7511933c1b13ad|1585913893|1585913807; wb_view_log_5652790996=1536*8641.25; webim_unReadCount=%7B%22time%22%3A1585913773562%2C%22dm_pub_total%22%3A6%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A6%2C%22msgbox%22%3A0%7D'),
                              )
            yield request


        for i in range(2):
            url = 'https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=2&pagebar={}&pl_name=Pl_Official_MyProfileFeed__20&id=1005051116218960&script_uri=/u/1116218960&feed_type=0&pre_page=1&domain_op=100505&__rnd=1585971835384'.format(i)
            for j in range(1,page+1):
                url = re.sub('page=\d', 'page={}'.format(str(j)), url)
                print(url)
                yield Request(url,
                              self.img,
                              cookies=get_cookies('Ugrow-G0=140ad66ad7317901fc818d7fd7743564; login_sid_t=bce82d26abdfef52130aaf1280a73072; cross_origin_proto=SSL; SUB=_2A25zhoMODeRhGeNI7lAW-S7FwjqIHXVQ9fPGrDV8PUNbmtAKLUrDkW9NSE6jQV86gJEmjNswD5OCgJuR0jUN802B; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W562vizmvqhwewD21Hd_LXF5JpX5KzhUgL.Fo-cSKzN1K541Kq2dJLoIXnLxK-LBKBL1-2LxK-L122LBKnLxK-L122LBKnLxKBLB.BLBK5LxKML1-2L1hBLxKML12eLB-2LxKnL1hBL1K2LxK-LB-BL1K5t; TC-V5-G0=595b7637c272b28fccec3e9d529f251a; _s_tentry=-; Apache=701068823940.0154.1585640119674; SINAGLOBAL=701068823940.0154.1585640119674; ULV=1585640119680:1:1:1:701068823940.0154.1585640119674:; wb_view_log=1536*8641.25; SUHB=0ebtIJ4eBNznFA; ALF=1617176284; SSOLoginState=1585640285; UOR=,,login.sina.com.cn; wvr=6; TC-Page-G0=62b98c0fc3e291bc0c7511933c1b13ad|1585653004|1585653004; wb_view_log_5652790996=1536*8641.25; webim_unReadCount=%7B%22time%22%3A1585652882743%2C%22dm_pub_total%22%3A6%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A6%2C%22msgbox%22%3A0%7D')
                              )


    def img(self, response):
        page_count = re.findall('countPage=(\w+)',response.text)
        imgs_data = re.findall('clear_picSrc=(.*?)&', response.text)
        img = re.findall('2F(.*?)(jpg|gif)', str(imgs_data))
        for i in img:
            img_id = ''.join(i).split('%2F')[-1]
            img_url = 'https://wx2.sinaimg.cn/mw690/' + img_id
            yield Request(img_url, self.img_down)

        url = 'https://www.baidu.com'
        if page_count:
            request = Request(url,self.parse)
            request.meta['page_count'] = int(page_count[0])
            yield request

    def img_down(self, response):
        self.c += 1
        img_name = response.url.split('/')[-1]
        path = os.path.curdir + '/imgs'
        if not os.path.exists(path):
            os.makedirs(path)

        with open('{}/{}'.format(path, img_name), 'wb') as f:
            print(self.c)
            f.write(response.body)
