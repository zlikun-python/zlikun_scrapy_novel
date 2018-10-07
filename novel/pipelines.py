# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

import pymongo
from pymongo import MongoClient

from novel.items import NovelItem, ChapterItem


class NovelPipeline(object):
    def process_item(self, item, spider):
        return item


# https://docs.scrapy.org/en/latest/topics/item-pipeline.html#write-items-to-mongodb
class NovelMongoPipeline(object):
    """
    官方文档上的Mongo配置方法仅供参考（可能过时了），新版 pymongo 库不使用 url 配置Mongo连接
    """

    def __init__(self, mongo_host, mongo_db):
        self.mongo_host = mongo_host
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        # 这里的配置由 settings.py 文件提供
        # 构造(初始化)方法中的值由这里注入
        return cls(
            mongo_host=crawler.settings.get('MONGO_HOST'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = MongoClient(host=self.mongo_host)
        self.db = self.client.get_database(self.mongo_db)

    def close_spider(self, spider):
        self._update_latest_chapter()
        self.client.close()

    def _update_latest_chapter(self):
        """
        爬虫运行结束时，将最新章节ID更新到小说表中，方便下次断点续爬

        :return:
        """
        for novel in self.db.get_collection('novel').find():
            # 查找小说对应章节表最大章节编号记录
            result = self.db.get_collection('novel_{}'.format(novel['number'])). \
                find({}, {'_id': 0, 'number': 1}).sort('number', direction=pymongo.DESCENDING).limit(1)
            try:
                record = result.next()
                if record:
                    # 将其更新至小说记录中
                    latest_chapter_number = record['number']
                    self.db.get_collection('novel').update_one({'number': novel['number']}, {
                        '$set': {'latest_chapter_number': latest_chapter_number, 'update_time': datetime.now()}})
            except StopIteration:
                pass

    def process_item(self, item, spider):
        if isinstance(item, NovelItem):
            self.db.get_collection('novel').insert_one(dict(item))
        if isinstance(item, ChapterItem):
            self.db.get_collection('novel_{}'.format(item['novel_number'])).insert_one(dict(item))
        return item
