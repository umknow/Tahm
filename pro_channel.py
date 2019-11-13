# -*- coding=utf-8 -*-
# author: king
# datetime: 2019/10/24 10:51
# describtion: 
"""
    项目启动入口

    # # 当接入了 scrapy_redis
    # 在指定位置丢入消息
    lpush baidu:start_urls http://www.baidu.com/
    # 爬虫框架一直在轮询进行检测（挂起状态）
"""
import os
from scrapy.http import Request
from scrapy.shell import Shell,Spider


# os.system('scrapy fetch "http://www.baidu.com/"')  # 直接下载HTML
# os.system('scrapy crawl baiduspider')  # 百度爬虫
os.system('scrapy crawl weixinspider')  # 微信公众号爬虫
