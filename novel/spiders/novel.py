# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class NovelSpider(scrapy.Spider):
    name = 'novel'
    allowed_domains = ['www.biquge5200.cc']

    # start_urls = ['https://www.biquge5200.cc/']

    def start_requests(self):
        yield Request('https://www.biquge5200.cc/{}/'.format('79_79067'), callback=self.parse)

    def parse(self, response):
        # self.logger.info('parse {}'.format(response.url))

        pass
