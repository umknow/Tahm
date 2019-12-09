# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider


# from ScrapySpiders.items import AnalysterItem
# from reports.ScrapySpiders.utils.crawl_utils import GetProxy


class BaiduspiderSpider(RedisSpider):  # scrapy.Spider
    name = 'baiduspider'
    allowed_domains = ['www.baidu.com']
    # start_urls = ['http://www.baidu.com/', 'http://news.baidu.com/']
    redis_key = 'baidu:start_urls'

    def parse(self, response):
        print('parse >>', response)

        url = 'http://news.baidu.com/'

        yield scrapy.Request(  # scrapy.Request
            url=url,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            callback=self.parse_page1,
            dont_filter=True
        )

    def parse_page1(self, response):
        print('parse_page1 >>>>', response)
        # print(response)
        pass

