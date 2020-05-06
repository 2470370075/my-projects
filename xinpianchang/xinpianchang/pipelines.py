# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from xinpianchang.items import Info
import pymysql
from xinpianchang.items import Mp4_url
from xinpianchang.items import Comments


class XinpianchangPipeline(object):
    def open_spider(self,spider):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', passwd='saber2014', db='xinpianchang')
        self.cur = self.conn.cursor()


    def close_spider(self,spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):

        if isinstance(item,Info):
            keys = item.keys()
            values=list(item.values())

            sql = "insert into info({}) values ({})".format(                #变量名在excule里面不好弄，双重字符串格式化
                ','.join(keys),
                ','.join(['%s']*len(values))
            )

            self.cur.execute(sql,values)
            self.conn.commit()
        #
        if isinstance(item,Mp4_url):
            keys = item.keys()
            values=list(item.values())

            sql = "insert into mp4({}) values ({})".format(                #
                ','.join(keys),
                ','.join(['%s']*len(values))
            )

            self.cur.execute(sql,values)

        if isinstance(item,Comments):
            for i in item['comments']:

                sql = 'insert into com(name,com) values ("{}","{}")'.format(
                   item['name'],i
                )

                self.cur.execute(sql)

        return item


