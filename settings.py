# -*- coding: utf-8 -*-

# Scrapy settings for Tahm project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from quotations.conf import config

BOT_NAME = 'Tahm'

SPIDER_MODULES = ['Tahm.spiders']
NEWSPIDER_MODULE = 'Tahm.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Tahm (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 30

ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 100,  # 配置redis管道
    'Tahm.pipelines.MysqlTwistedPipline': 300,
   # 'ScrapyTest.pipelines.ScrapytestPipeline': 300,
}


# 公账号授权的信息的list，用于在爬虫被禁掉时，自动切换账户
AUTH_LIST = [
        # {'Account':'119xxxxxx@qq.com','PassWord':'xxxxxxx'}
    ]

# 需要爬取的公帐号的名称，暂不支持同时爬取多个公帐号
OFFICIAL_ACCOUNTS = '李大霄'

# 是否需要使用语音播报，爬虫运行状态,当为True时，需要安装 python win32com 模块
SPEEK_ALLOW = False

# MongDB数据库配置
MONGO_HOST = "127.0.0.1"  # 主机IP
MONGO_PORT = 27017  # 端口号
MONGO_DB = "Weixin_Spider"  # 库名
MONGO_COLLECTION = "weixin_article"  # collection名

# MySQL数据库连接
MYSQL_HOST = "127.0.0.1"
MYSQL_DBNAME = "Weixin_Spider"
MYSQL_USER = "root"
MYSQL_PASSWORD = "xxxxxx"



# # 【日志配置】
# """
# CRITICAL - 严重错误(critical)
# ERROR - 一般错误(regular errors)
# WARNING - 警告信息(warning messages)
# INFO - 一般信息(informational messages)
# DEBUG - 调试信息(debugging messages)
# """
# # # 设置日志记录级别
# LOG_LEVEL = 'WARNING'
# # # 配置log文件输出
# # LOG_FILE = '.' + os.sep + 'log' + os.sep + 'spiders.log'
# # logger = logging.getLogger(__name__)


# # 【对接scrapy_redis】
# # 使用了scrapy_redis的去重组件，在redis数据库里做去重
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# # 使用了scrapy_redis的调度器，在redis里分配请求
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# # 在redis中保持scrapy-redis用到的各个队列，从而允许暂停和暂停后恢复，也就是不清理redis queues
# SCHEDULER_PERSIST = True
#
# # Redis连接参数
# # 本地仓库
# # REDIS_HOST = '127.0.0.1'
# # REDIS_PORT = 6379
#
# # {'decode_responses': True, 'host': '118.31.xx.xxx', 'port': xxxx, 'password': 'xxxx', 'db': x}
# __redis_conf = config('redis').get('data_10')
# del __redis_conf['decode_responses']
# REDIS_PARAMS = __redis_conf

