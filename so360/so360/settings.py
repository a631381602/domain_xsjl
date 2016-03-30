# -*- coding: utf-8 -*-

# Scrapy settings for so360 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

import random

BOT_NAME = 'so360'

SPIDER_MODULES = ['so360.spiders']
NEWSPIDER_MODULE = 'so360.spiders'

'''读取代理文件中的ip，写入PROXIES'''
PROXIES = []
for line in open('/Users/sunjian/Desktop/hc项目/proxy/hege_daili.txt'):
    line = line.strip()
    PROXIES.append({'ip_port':'%s' % line ,'user_pass':''})

# 随机cookie
def getCookie():
    cookie_list = [
    'QiHooGUID=01547CB5F9C3B2CF236B92F5EAA018A7.1456906808741; tso_Anoyid=11145690680812406559; __guid=15484592.2780430531132906000.1456914750285.4814; dpr=0.8999999761581421; webp=1; stc_haosou_home=0fadb9b0bd12; count=50; test_cookie_enable=null'
    ]
    cookie = random.choice(cookie_list)
    return cookie

# 定义ua列表
USER_AGENTS =[
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        #'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
    ]

RETRY_TIMES = 10
RETRY_HTTP_CODES = [ 500 , 503 , 504 , 400 , 403 , 404 , 408 ,302]

# 假如中间件
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware' : 90 ,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,
    'so360.middlewares.RandomUserAgent':400,

    # 'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    # 'so360.middlewares.ProxyMiddleware': 100,
}

# '''降低log级别，取消注释则输出抓取详情'''
# LOG_LEVEL = 'INFO'

# 禁止cookie
COOKIES_ENABLED = False

# cookie debug
# COOKIES_DEBUG = False

# DEFAULT_REQUEST_HEADERS ，定义请求的头信息
DEFAULT_REQUEST_HEADERS = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Host':'www.so.com',
    'Upgrade-Insecure-Requests':'1',
    'Cookie':'%s' % getCookie(),
}

# 禁止显示<urlopen error timed out>告警
DOWNLOAD_HANDLERS = {
  's3': None,
}

# 下载延迟，既下载两个页面之间的等待时间
DOWNLOAD_DELAY = 0.1

# 并发最大值
CONCURRENT_REQUESTS = 10

# 对单个网站的并发最大值
CONCURRENT_REQUESTS_PER_DOMAIN = 10

# #启动自动限速
# AUTOTHROTTLE_ENABLED = False

# 设置下载超时
DOWNLOAD_TIMEOUT = 60

#配置数据库
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'heichan'
MYSQL_USER = 'root'
MYSQL_PASSWD = ''





