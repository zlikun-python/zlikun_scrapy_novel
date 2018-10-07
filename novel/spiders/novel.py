# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.http import Request

from novel.items import NovelItem, ChapterItem


class NovelSpider(scrapy.Spider):
    name = 'novel'
    allowed_domains = ['www.biquge5200.cc']

    # start_urls = ['https://www.biquge5200.cc/']

    def start_requests(self):
        """
        使用全局配置来配置目标小说

        :return:
        """
        for item in self.settings.get('NOVEL_ITEMS'):
            if item:
                yield Request('https://www.biquge5200.cc/{}/'.format(item), callback=self.parse)

    def parse(self, response):
        """
        解析小说信息及章节列表

        :param response:
        :return:
        """

        # 提取小说信息
        item = NovelItem()
        item['number'] = response.url.split('/')[-2]
        item['name'] = response.xpath('//div[@id="info"]/h1/text()').extract_first().strip()
        item['author'] = response.xpath('//div[@id="info"]/p[1]/text()').extract_first().replace('作    者：', '').strip()
        item['cover'] = response.xpath('//div[@id="fmimg"]/img/@src').extract_first()
        item['origin_url'] = response.url

        yield item

        # 提取章节列表
        yield from [Request(chapter_url, meta={'novel_number': item['number']}, callback=self.parse_chapter) for
                    chapter_url in
                    response.xpath('//div[@id="list"]/dl/dd/a/@href').extract()[9:]]

    def parse_chapter(self, response):
        """
        解析章节信息

        :param response:
        :return:
        """
        item = ChapterItem()
        item['novel_number'] = response.meta['novel_number']
        item['number'] = int(re.search(r'/(\d+).html$', response.url).group(1))
        item['title'] = response.xpath('//div[@class="bookname"]/h1/text()').extract_first().strip()
        item['content'] = '\r\n'.join(response.xpath('//div[@id="content"]/p/text()').re(r'\S+'))
        item['origin_url'] = response.url

        yield item
