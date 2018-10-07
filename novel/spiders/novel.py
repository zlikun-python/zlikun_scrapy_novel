# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.http import Request


class NovelSpider(scrapy.Spider):
    name = 'novel'
    allowed_domains = ['www.biquge5200.cc']

    # start_urls = ['https://www.biquge5200.cc/']

    def start_requests(self):
        yield Request('https://www.biquge5200.cc/{}/'.format('79_79067'), callback=self.parse)

    def parse(self, response):
        """
        解析小说信息及章节列表

        :param response:
        :return:
        """

        # 提取小说信息
        number = response.url.split('/')[-2]
        name = response.xpath('//div[@id="info"]/h1/text()').extract_first().strip()
        author = response.xpath('//div[@id="info"]/p[1]/text()').extract_first().replace('作    者：', '').strip()
        cover = response.xpath('//div[@id="fmimg"]/img/@src').extract_first()

        self.logger.debug('number = {}, name = {}, author = {}, cover = {}'.format(number, name, author, cover))

        novel = {
            'number': number,
            'name': name,
            'author': author,
            'cover': cover,
        }

        yield novel

        # 提取章节列表
        yield from [Request(chapter_url, meta={'novel_number': novel['number']}, callback=self.parse_chapter) for
                    chapter_url in
                    response.xpath('//div[@id="list"]/dl/dd/a/@href').extract()[9:]]

    def parse_chapter(self, response):
        """
        解析章节信息

        :param response:
        :return:
        """
        novel_number = response.meta['novel_number']
        number = int(re.search(r'/(\d+).html$', response.url).group(1))
        title = response.xpath('//div[@class="bookname"]/h1/text()').extract_first().strip()
        content = '\r\n'.join(response.xpath('//div[@id="content"]/p/text()').re(r'\S+'))

        yield {
            'novel_number': novel_number,
            'number': number,
            'title': title,
            'content': content,
        }
