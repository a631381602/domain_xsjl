#coding:utf-8

import scrapy,re,urllib,os,time,sys,random
from domain_filter.items import DomainFilterItem
from scrapy import Request
import MySQLdb as mdb
import StringIO,pycurl

reload(sys)
sys.setdefaultencoding('utf-8')

current_time = time.strftime("%Y-%m-%d",time.localtime(time.time()))
# current_time = '2016-03-20'

req = open('/Users/sunjian/Desktop/hc项目/weijin.txt').read().strip()

def search(req,html):
     text = re.search(req,html)
     if text:
         data = text.group(1)
     else:
         data = 'no'
     return data

# 搜狗SR cookie
def sg_cookie():
    cookie_list = [
    'SUID=BA75417C4FC80D0A0000000056D6A238; SUV=1457445239014830; SMYUV=1457851039864076; wuid=AAEXCgMmEAAAAAqTLn3PlQkAZAM=; fromwww=1; usid=Jt04V81y1IlvJgv6; gpsloc=%E5%8C%97%E4%BA%AC%E5%B8%82; pgv_pvi=1062389760; pgv_si=s856082432; SNUID=2476FBF924210D090B12995E245FFC81; ld=eOaKWZllll2QC$wclllllVbItEGlllllK9VCmklllx9lllll9joll5@@@@@@@@@@; IPLOC=CN1100; sct=52; LSTMV=352%2C470; LCLKINT=3557'
    ]
    cookie = random.choice(cookie_list)
    return cookie


def getUA():
    uaList = [
        'Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+.NET+CLR+1.1.4322;+TencentTraveler)',
        'Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1;+.NET+CLR+2.0.50727;+.NET+CLR+3.0.4506.2152;+.NET+CLR+3.5.30729)',
        'Mozilla/5.0+(Windows+NT+5.1)+AppleWebKit/537.1+(KHTML,+like+Gecko)+Chrome/21.0.1180.89+Safari/537.1',
        'Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1;+SV1)',
        'Mozilla/5.0+(Windows+NT+6.1;+rv:11.0)+Gecko/20100101+Firefox/11.0',
        'Mozilla/4.0+(compatible;+MSIE+8.0;+Windows+NT+5.1;+Trident/4.0;+SV1)',
        'Mozilla/4.0+(compatible;+MSIE+8.0;+Windows+NT+5.1;+Trident/4.0;+GTB7.1;+.NET+CLR+2.0.50727)',
        'Mozilla/4.0+(compatible;+MSIE+8.0;+Windows+NT+5.1;+Trident/4.0;+KB974489)',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
    ]
    headers = random.choice(uaList)
    return headers


def getHtml(url,headers):
    while 1:
        try:
            c = pycurl.Curl()
            c.setopt(pycurl.MAXREDIRS,2)
            c.setopt(pycurl.REFERER, url)
            #c.setopt(pycurl.FOLLOWLOCATION, True)
            c.setopt(pycurl.CONNECTTIMEOUT, 10)
            c.setopt(pycurl.TIMEOUT,10)
            c.setopt(pycurl.ENCODING,'gzip,deflate')
            # c.setopt(c.PROXY,ip()) 
            c.fp = StringIO.StringIO()
            c.setopt(pycurl.URL, url)
            c.setopt(pycurl.HTTPHEADER,headers)
            c.setopt(c.WRITEFUNCTION, c.fp.write)
            c.perform()
            #code = c.getinfo(c.HTTP_CODE) 返回状态码
            html = c.fp.getvalue()
            if 'verify.baidu.com' in html:
                print '被封'
                continue
            elif '<title>302 Found</title>' in html:
                continue
            elif "<html><head></head><body><a id='go' rel='noreferrer'></a>" in html:
                continue
            elif 'The page cannot be displayed' in html:
                continue
            elif '500 Internal Server Error' in html:
                continue
            elif '<title>Rede Metodista</title>' in html:
                continue
            elif '<title>Bad Gateway!</title>' in html:
                continue
            elif '<title>503 Service Temporarily Unavailable</title>' in html:
                continue
            elif '<title>404 Not Found</title>' in html:
                continue
            elif '您的电脑或所在的局域网络有异常的访问' in html:
                print '被封'
                continue
            else:
                return html
        except Exception, what:
            information = '错误信息：%s' % what
            return information
            continue


sogou_headers = [
    "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding:gzip, deflate, sdch",
    "Accept-Language:zh-CN,zh;q=0.8,en;q=0.6",
    "Cache-Control:no-cache",
    "Connection:keep-alive",
    "Cookie:%s" % sg_cookie(),
    "Host:rank.ie.sogou.com",
    "Pragma:no-cache",
    "Upgrade-Insecure-Requests:1",
    "User-Agent:%s" % getUA(),
]    


class DmozSpider(scrapy.Spider):
    name = "domain"
    start_urls = []
    for word in open('/Users/sunjian/Desktop/hc项目/domain_xsjl/可注册.txt'):
        word = word.strip()

        url_bd = 'http://www.baidu.com/s?&tn=baidulocal&ie=utf-8&cl=3&wd=site%%3A%s' % word

        start_urls.append(url_bd)

    def parse(self,response):

        # 提取查询domain
        word = search(r'site%3A(.*)',response.url)

        item = DomainFilterItem()

        # 抓取百度
        baidu_html = response.body
        bd_index = search('百度为您找到相关网页(\d+)篇',baidu_html)
        if bd_index == 'no' or 'us1.wss.webroot.com' in response.url or 'search/error.html' in response.url:
            yield Request(url=response.url, callback=self.parse)
            #yield Request(url=response.url, callback=self.parse)
        else:

            # 检测首页结果进入倒排索引的数量
            size_list = re.findall(';(\d+)K&',baidu_html)
            reverse_index = len(size_list) - size_list.count(1)

            # 检测百度搜索标题是否包含中文（判断是否为中文站点）
            title_list = re.findall('<font size="3">(.*?)</font>',baidu_html)
            if len(title_list) == 0:
                chinese = 'no_language'
            else:
                title_set = ''.join(title_list)
                if len(re.findall(u'[\u4e00-\u9fa5]+',title_set.decode('utf8'))) > 0:
                    chinese = 'chinese'
                else:
                    chinese = 'english'

            # 检测是否泛解析过（二级域名>=3，则判定为泛解析）
            domain_list = re.findall(r'<font color=#008000>([^\.]*?)\.%s/' % word,baidu_html)
            if len(set(domain_list)) >= 3:
                pan_analysis = '泛解析'
            else:
                pan_analysis = '正常'

            # 检测是否做过非法违禁内容（检测html是否包含违禁关键词）
            if search('(%s)' % req,baidu_html) == 'no':
                illegal = '正常'
            else:
                illegal = '包含违禁词'    

            # 搜狗SR查询
            sgsr_html = getHtml('http://rank.ie.sogou.com/sogourank.php?ur=http%%3A%%2F%%2Fwww.%s%%2F' % word, sogou_headers)
            sgsr = search(r'sogourank=(\d+)',sgsr_html)

            item['domain'] = word
            item['bd_index'] = bd_index
            item['reverse_index'] = reverse_index
            item['chinese'] = chinese
            item['pan_analysis'] = pan_analysis
            item['illegal'] = illegal
            item['sgsr'] = sgsr
            item['current_time'] = current_time
            yield item


