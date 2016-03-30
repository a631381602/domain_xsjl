# -*- coding: utf-8 -*-

# Scrapy settings for domain_filter project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

import random

BOT_NAME = 'domain_filter'

SPIDER_MODULES = ['domain_filter.spiders']
NEWSPIDER_MODULE = 'domain_filter.spiders'

'''读取代理文件中的ip，写入PROXIES'''
PROXIES = []
for line in open('/Users/sunjian/Desktop/hc项目/proxy/hege_daili.txt'):
    line = line.strip()
    PROXIES.append({'ip_port':'%s' % line ,'user_pass':''})

# 随机cookie
def getCookie():
    cookie_list = [
    'BAIDUID=791ED7F86F43AF44A3808AB244404E1A:FG=1; PSTM=1443524661; BIDUPSID=4B0DC2F54860625BA83681F98C507951; BDUSS=VdqVXZlaHNPVE1jRzlRU3BEMlBFcFVDQTBGV3ZGcEZTSW90Sn5vZHFQT2pvVFJXQVFBQUFBJCQAAAAAAAAAAAEAAAAJkstJv7TXvMTj1NnM-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKMUDVajFA1WL; MCITY=-%3A; ispeed_lsm=2; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a01942858111; H_WISE_SIDS=100043_100288; BDSFRCVID=tAAsJeC627DsPNr4QNLk-qjWNeK2EJ7TH6ao_taMbqNtTyotFjlwEG0PJ3lQpYD-gGLkogKK0mOTHUcP; H_BDCLCKID_SF=JbAjoKK5tKvbfP0kh-QJhnQH-UnLqMrZJT7Z0lOnMp05flToM6OGhP0WQqQaJ-RULIbEXqbLBnRvOKO_e6t5D5J0jN-s-bbfHDJK0b7aHJOoDDvO2j35y4LdLp7xJb5AWKLJbR7wbnj0hpcR3p3s2RIv24vQBMkeWJLfoIP2JCPMbP365ITSMtCfbfO02D62aKDs-lnx-hcqEpO9QT-aLq-gjbQgKPIL-CoObDTe5bOo8Ro6yjOsDUThDHt8J50OfR3fL-08bPoEqbjg54r5hnjH-UIS26uDJJFeo6Q2bnOHDtJpMtJ_Htu32q32DJ3J55ryL4tBan7JDTQm5bOBK-QK5MoO-TPDt5neaJ5n0-nnhn0wDj_M0tuqBnjetlQ4Q5RWhDJR2UJ2en-Ry6C-D5v0jatDq-TtHDjLQ-bqbTrjDnCr34FWKUI8LPbO05Jq5aPe_UjytUTBfMcDW-6vKfu-Ma7OKMcAt2LEoCtXJIL2MDKr5nJbq4uehU6X2D62aKDsLpjp-hcqEIL4jUO50MCXjbQwWPPL-CQU2J5ctq5kMUbSj4QoBn0_Xf5DWJ3nMCOJKJcsbh5nhMJ_DPvGKhFvqfJxWPny523ion6vQpnlHUtu-n5jHjJBjG8J3f; BDRCVFR[ltbVPlNi2ac]=mk3SLVN4HKm; BD_UPN=123253; H_PS_645EC=8871KezGVuec0l6U03EckUIiztA%2Be7LttD91u%2FB6ntENY5ucpQaoGsil%2BFmSqHBO; sug=3; sugstore=1; ORIGIN=0; bdime=21110; BDRCVFR[skC-pcPB0g_]=mk3SLVN4HKm; BD_CK_SAM=1; BDSVRTM=91; H_PS_PSSID=',
    'BAIDUID=0236A7F2BA57EAD085EEDE626343CB91:FG=1; PLUS=1; BIDUPSID=0236A7F2BA57EAD085EEDE626343CB91; PSTM=1444372071; BDRCVFR[skC-pcPB0g_]=mk3SLVN4HKm; BD_CK_SAM=1; BDSVRTM=64; H_PS_PSSID='
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
    'domain_filter.middlewares.RandomUserAgent':400,

    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'domain_filter.middlewares.ProxyMiddleware': 100,
}

'''降低log级别，取消注释则输出抓取详情'''
LOG_LEVEL = 'INFO'

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
    'Host':'www.baidu.com',
    'RA-Sid':'7739A016-20140918-030243-3adabf-48f828',
    'RA-Ver':'3.0.7',
    'Upgrade-Insecure-Requests':'1',
    'Cookie':'%s' % getCookie(),
}

# 禁止显示<urlopen error timed out>告警
DOWNLOAD_HANDLERS = {
  's3': None,
}

# 下载延迟，既下载两个页面之间的等待时间
# DOWNLOAD_DELAY = 0.5

# 并发最大值
CONCURRENT_REQUESTS = 700

# 对单个网站的并发最大值
CONCURRENT_REQUESTS_PER_DOMAIN = 700

# #启动自动限速
# AUTOTHROTTLE_ENABLED = False

# 设置下载超时
DOWNLOAD_TIMEOUT = 60

#配置数据库
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'heichan'
MYSQL_USER = 'root'
MYSQL_PASSWD = ''


# #启用PIPELINES
# ITEM_PIPELINES = {
#     'domain_filter.pipelines.DomainFilterPipeline': 300,
#     'domain_filter.pipelines.MySQLDomainFilterPipeline': 400,
# }




