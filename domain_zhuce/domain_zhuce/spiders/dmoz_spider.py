#coding:utf-8

import scrapy,re,urllib,os,time,sys,random
from domain_zhuce.items import DomainZhuceItem
import MySQLdb as mdb
from scrapy import Request

reload(sys)
sys.setdefaultencoding('utf-8')

def search(req,html):
     text = re.search(req,html)
     if text:
         data = text.group(1)
     else:
         data = 'no'
     return data

class DmozSpider(scrapy.Spider):
    name = "zhuce"
    start_urls = []
    for word in open('/Users/sunjian/Desktop/hc项目/domain_xsjl/不可访问'):
        word = word.strip()
        url = 'http://panda.www.net.cn/cgi-bin/check.cgi?area_domain=%s' % word
        start_urls.append(url)

    def parse(self,response):

        # 提取查询domain
        domain = search(r'area_domain=(.*)',response.url)

        item = DomainZhuceItem()

        html = response.body

        if 'Domain name is available' in html:
            reuset = '可注册'
        elif 'Domain exists' in html or 'In use' in html:
            reuset = '已被抢'
        else:
            reuset = 'Error!!'

        item['domain'] = domain
        item['reuset'] = reuset
        yield item


# class DmozSpider(scrapy.Spider):
#     name = "zhuce"
#     start_urls = []
#     for word in open('/Users/sunjian/Desktop/hc项目/domain_xsjl/不可访问'):
#         word = word.strip()
#         url = 'http://whois.22.cn/%s' % word
#         start_urls.append(url)

#     def parse(self,response):

#         # 提取查询domain
#         domain = search(r'whois.22.cn/(.*)',response.url)

#         item = DomainZhuceItem()


#         html = response.body

#         if 'Whois查询_域名Whois查询注册工具_22.cn爱名网' not in html:
#             yield Request(url=response.url, callback=self.parse)

#         else:
#             if 'Name Server' in html:
#                 reuset = '已被抢'
#             elif '该域名尚未注册' in html:
#                 reuset = '可注册'
#             else:
#                 reuset = 'ERROR!!!!'
#                 print response.url
                
#             item['domain'] = domain
#             item['reuset'] = reuset
#             yield item


