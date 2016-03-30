#coding:utf-8

import scrapy,re,urllib,os,time,sys,random,csv
from so360.items import So360Item
from scrapy import Request
import MySQLdb as mdb
import StringIO,pycurl

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
    name = "360"
    start_urls = []

    csvfile = file('/Users/sunjian/Desktop/hc项目/domain_xsjl/一轮过滤.csv', 'rb')
    reader = csv.reader(csvfile)

    for line in reader:
        try:
            word = line[0]
            bd_index = line[1]
            daopai = line[2]
            sr = line[3]

            url_bd = 'https://www.so.com/s?q=site%%3A%s&data=%s_%s_%s' % (word,bd_index,daopai,sr)

            start_urls.append(url_bd)
        except:
            print line

    def parse(self,response):

        # 提取查询domain
        word = search(r'site%3A(.*?)&data',response.url)
        data = search(r'&data=(.*)',response.url)

        bd_index = data.split('_')[0]
        daopai = data.split('_')[1]
        sr = data.split('_')[2]

        html = response.body

        aq_score = search(r'<p class="ele-score"><em>(\d+)</em><i>分',html)
        if aq_score != 'no':
            if int(aq_score) > 70:
                score = '较安全'
            else:
                score = '不安全'
        else:
            score = '无数据'

        item = So360Item()
        item['word'] = word
        item['bd_index'] = bd_index
        item['daopai'] = daopai
        item['sr'] = sr
        item['score'] = score
        yield item


