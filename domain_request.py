#coding:utf-8

'''查看域名能否被正常访问'''

import StringIO,pycurl,time,random,re,os,csv,urllib,socket,sys,HTMLParser
from threading import Thread,Lock
from Queue import Queue
from bs4 import BeautifulSoup as bs
from lxml import etree
import MySQLdb as mdb

reload(sys)    
sys.setdefaultencoding('utf-8')  

csvfile = open('/Users/sunjian/Desktop/hc项目/domain_xsjl/不可访问','wb')    #存放关键词和搜索结果页源码的文件

daili_list = [] #存储代理ip
def ip():
    for x in open('/Users/sunjian/Desktop/hc项目/proxy/hege_daili.txt'):
        x = x.strip()
        daili_list.append(x)
    newip = random.choice(daili_list)
    return newip

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


def is_index(url,headers):
    while 1:
        try:
            socket.setdefaulttimeout(15.0)
            c = pycurl.Curl()
            c.setopt(pycurl.MAXREDIRS,2)
            c.setopt(pycurl.REFERER, url)
            #c.setopt(pycurl.FOLLOWLOCATION, True)
            c.setopt(pycurl.CONNECTTIMEOUT, 10)
            c.setopt(pycurl.TIMEOUT,15)
            c.setopt(pycurl.ENCODING,'gzip,deflate')
            # c.setopt(c.PROXY,ip()) 
            c.fp = StringIO.StringIO()
            c.setopt(pycurl.URL, url)
            c.setopt(pycurl.HTTPHEADER,headers)
            c.setopt(c.WRITEFUNCTION, c.fp.write)
            c.perform()
            code = c.getinfo(c.HTTP_CODE)
            html = c.fp.getvalue()
            return code
        except Exception, what:
            information = '错误信息：%s' % what
            return str(information)
            continue

def search(req,line):
    text = re.search(req,line)
    if text:
        data = text.group(1)
    else:
        data = 'no'
    return data

url_list = []
con = mdb.connect(host="127.0.0.1",user="root",passwd="",db="heichan",charset='utf8');
with con:
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute("select domain from check_zhuce")
    rows = cur.fetchall()
    for row in rows:
        query = row['domain']
        url_list.append(query)
con.close()

class Fetcher:
    def __init__(self,threads):
        self.lock = Lock() #线程锁
        self.q_req = Queue() #任务队列
        self.q_ans = Queue() #完成队列
        self.threads = threads
        for i in range(threads):
            t = Thread(target=self.threadget) #括号中的是每次线程要执行的任务
            t.setDaemon(True) #设置子线程是否随主线程一起结束，必须在start()
                              #之前调用。默认为False
            t.start() #启动线程
        self.running = 0 #设置运行中的线程个数
 
    def __del__(self): #解构时需等待两个队列完成
        time.sleep(0.5)
        self.q_req.join() #Queue等待队列为空后再执行其他操作
        self.q_ans.join()
 
    #返回还在运行线程的个数，为0时表示全部运行完毕
    def taskleft(self):
        return self.q_req.qsize()+self.q_ans.qsize()+self.running 

    def push(self,req):
        self.q_req.put(req)
 
    def pop(self):
        return self.q_ans.get()
 
    #线程执行的任务，根据req来区分 
    def threadget(self):
        while True:
            line = self.q_req.get()
            word = line.strip()

            '''
            Lock.lock()操作，使用with可以不用显示调用acquire和release，
            这里锁住线程，使得self.running加1表示运行中的线程加1，
            如此做防止其他线程修改该值，造成混乱。
            with下的语句结束后自动解锁。
            '''

            with self.lock: 
                self.running += 1

            '''构造请求头，header请自行修改'''
            headers = [
				"Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
				"Accept-Encoding:gzip, deflate, sdch",
				"Accept-Language:zh-CN,zh;q=0.8,en;q=0.6",
				"Cache-Control:no-cache",
				"Connection:keep-alive",
				"Host:%s" % word,
				"Pragma:no-cache",
				"Upgrade-Insecure-Requests:1",
				"User-Agent:%s" % getUA(),
            ]    
            
            code = is_index(word,headers)
            if '错误信息' in str(code):
                print word
                csvfile.write('%s\n' % word)



            #self.q_ans.put((req,ans)) # 将完成的任务压入完成队列，在主程序中返回
            self.q_ans.put(line)
            with self.lock:
                self.running -= 1
            self.q_req.task_done() # 在完成一项工作之后，Queue.task_done()
                                   # 函数向任务已经完成的队列发送一个信号
            time.sleep(0.1) # don't spam
 
if __name__ == "__main__":
    f = Fetcher(threads=150) #设置线程数
    for url in url_list:
        f.push(url)         #所有url推入下载队列
    while f.taskleft():     #若还有未完成的的线程
        f.pop()   #从下载完成的队列中取出结果
          

# data = []
# data.append(word)
# data.append('can_register')
# writer = csv.writer(csvfile,dialect='excel')
# writer.writerow(data)    
