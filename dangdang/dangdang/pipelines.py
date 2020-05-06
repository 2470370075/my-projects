# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from dangdang.items import Book
from dangdang.items import Detail


class DangdangPipeline(object):

    def open_spider(self,spider):
        self.conn = pymysql.connect(host='127.0.0.1',user='root',passwd='saber2014',db='dangdang')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item,Book):
            name = item['name']
            price = item['price']
            sql = 'insert into book (name,price) values (%s,%s)'
            self.cur.execute(sql,(name,price))
            self.conn.commit()

        if isinstance(item,Detail):
            keys = item.keys()
            values = item.values()
            print(list(values))
            sql = 'insert into detail ({}) values ({})'.format(','.join(keys),','.join(len(keys) * ['%s']))
            self.cur.execute(sql,list(values))
            self.conn.commit()

    def close_spder(self,spider):
        self.cur.close()
        self.conn.close()
