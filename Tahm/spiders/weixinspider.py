# -*- coding: utf-8 -*-
import json
import random
import scrapy
import time
from scrapy.conf import settings
from scrapy.http import Request
from win32com import client as Client
from scrapy_redis.spiders import RedisSpider
from Tahm.utils.auth_mangaer import WeXinLogin
from ..items import WexincrawlerItem, WeixinItemLoader


class WeixinspiderSpider(scrapy.Spider):  # scrapy.Spider
    name = 'weixinspider'
    _official_accounts = settings['OFFICIAL_ACCOUNTS']  # 获取公众号名称信息
    allowed_domains = ['mp.weixin.qq.com']
    start_urls = ['http://mp.weixin.qq.com/']
    speaker = Client.Dispatch("SAPI.SpVoice")
    _auth_list = settings['AUTH_LIST']
    _speek_allow = settings['SPEEK_ALLOW']
    _randomparams = '0.81{0}47026587991'
    _begin = 0

    headers = {
        'Accept': 'application / json, text / javascript, * / *; q = 0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'mp.weixin.qq.com',
        'Connection': 'keep - alive',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
    }

    # 公众号查询URL
    _query_weixin_official_accounts_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&token={0}&lang=zh_CN&f=json&ajax=1&random=0.5242867752964442&query={1}&begin=0&count=5'
    # 公众号所有文章查询
    _query_weixin_official_articles_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token={0}&lang=zh_CN&f=json&ajax=1&random={1}&action=list_ex&begin={2}&count=5&query=&fakeid={3}&type=9'

    def auth_callback(self, token, cookies):
        '''
        更新token和cookies,已经请求header中的referer值
        :param token: 登录获得的token
        :param cookies: 登录返回的cookies
        :return:
        '''
        # 首先读取本地cookies
        token = self.__read_data('token.txt')
        cookies = self.__read_data('cookies.txt')

        self.token = token
        self.cookies = cookies

        referer = 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token={}&lang=zh_CN'.format(
            self.token)
        self.headers["Referer"] = referer
        print('auth success and token is {}'.format(self.token))

    def speek_spider_status(self, message):
        if self._speek_allow and self.speaker is not None:
            self.speaker.Speak(message)

    def auth_login(self):
        '''
        授权登录，并通过回调返回token和Cookies
        :return: auth_callback
        '''
        # 启动线程获取token cookies

        username, password = self.get_auth_param()
        self.speek_spider_status(u"开始执行登录认证,当前登录账号是%s" % username)
        # auth_weixin_thread = WeXinLogin(username=username, password=password, callback=self.auth_callback)
        # auth_weixin_thread.start()
        # auth_weixin_thread.join(60)
        self.auth_callback('', '')  # 手动调试


        if self.token is None or self.cookies is None:
            self.speek_spider_status(u"登录认证失败，准备退出")
            raise SystemError('When login weixin meet an error')

    def get_auth_param(self):
        if len(self._auth_list) < 0 or not isinstance(self._auth_list, list):
            self.speek_spider_status(u"参数设置失败，请检查配置参数")
            raise SystemError('setting AUTH_LIST param error')

        param_dict = self._auth_list.pop()
        _username = param_dict['Account']
        _password = param_dict['PassWord']

        return _username, _password

    def start_requests(self):
        self.auth_login()  # 验证登录状态

        query_weixin_official_accounts_url = self._query_weixin_official_accounts_url.format(self.token,
                                                                                             self._official_accounts)

        self.speek_spider_status(u"登录认证通过，开始爬取数据,目标公众号为%s" % self._official_accounts)
        yield Request(headers=self.headers, cookies=self.cookies, url=query_weixin_official_accounts_url)

    def parse(self, response):
        if response is None or response.status is not 200:
            self.speek_spider_status(u"请求公众号信息时，发生错误，准备退出")
            raise SystemError('current request error')

        results = json.loads(response.text, encoding='utf-8')

        if results is None or results['base_resp']['ret'] != 0:
            print('result :>>', results)
            self.speek_spider_status(u"请求公众号信息时，返回数据异常，准备退出")
            raise SystemError('json data Exception')

        self.fakeid = results['list'][0]['fakeid']

        # 获取所有文章
        # 构造参数
        __query_weixin_official_articles_url = self._create_articles_url()
        yield Request(headers=self.headers, cookies=self.cookies, url=__query_weixin_official_articles_url,
                      callback=self._parse_articles)

    def _parse_articles(self, response):
        results = json.loads(response.text, encoding='utf-8')

        if results is None:
            self.speek_spider_status(u"请求公众号文章列表时，没有响应数据，准备退出")
            raise SystemError('Return data exception')

        elif results['base_resp']['ret'] == 200013:
            print('!!!!!!!!!now,Account is prohibited need to change your account!!!!!!!!!!')
            self.speek_spider_status(u"当前爬虫被封，准备执行切换账号操作")
            self.auth_login()

            __query_weixin_official_articles_url = self._create_articles_url()

            yield Request(headers=self.headers, cookies=self.cookies, url=__query_weixin_official_articles_url,
                          callback=self._parse_articles)

            return

        articles_count = int(results['app_msg_cnt'])
        print('%s共有%d篇文章' % (self._official_accounts, articles_count))
        for item_article in results['app_msg_list'][:1]:
            loader = WeixinItemLoader(item=WexincrawlerItem())
            loader.add_value('appmsgid', item_article['appmsgid'])
            loader.add_value('cover', item_article['cover'])
            loader.add_value('digest', item_article['digest'])
            loader.add_value('link', item_article['link'])
            loader.add_value('title', item_article['title'])
            loader.add_value('update_time', item_article['update_time'])
            # item['appmsgid'] = item_article['appmsgid']
            # item['cover'] = item_article['cover']
            # item['digest'] = item_article['digest']
            # item['link'] = item_article['link']
            # item['title'] = item_article['title']
            # item['update_time'] = item_article['update_time']
            item = loader.load_item()
            # yield item   # 不落地scrapy
            time.sleep(random.randint(1, 5))

            articles_url = item.get('link')
            print('articles_url >>>>>>>>>>>', articles_url)
            yield Request(headers=self.headers, cookies=self.cookies, url=articles_url,
                          callback=self.__parse_context)

            # exit(111)
            # 递归爬取
            # if self._begin < articles_count - 5:
            #     self._begin += 5
            #     print('当前页面数字是%d' % (self._begin))
            #     __query_weixin_official_articles_url = self._create_articles_url()
            #
            #     yield Request(headers=self.headers, cookies=self.cookies, url=__query_weixin_official_articles_url,
            #                   callback=self._parse_articles)
            #
            # else:
            #     self.speek_spider_status(u"完成所有文章的爬取，准确退出，再见")
            #     print('completed all articles crawler')

    def __parse_context(self, response):
        """文章格式解析"""
        data = response.body
        # print(response.body.decode('utf-8'))
        with open('test.html', 'wb') as f:
            f.write(data)

    def _create_articles_url(self):

        random_param = float(self._randomparams.format(random.choice(range(500))))
        __query_weixin_official_articles_url = self._query_weixin_official_articles_url.format(self.token, random_param,
                                                                                               self._begin, self.fakeid)

        return __query_weixin_official_articles_url

    def __read_data(self, file_name):
        """读取信息"""
        with open(file_name, 'r') as f:
            _data = json.loads(f.read())
        return _data
