#coding:utf-8

'''http://web.archive.org/cdx/search/cdx?url=oa24h.com&output=json&from=2014&to=2016&fl=timestamp,original'''
'''http://web.archive.org/web/20140625131200/http://www.kanzhun.com/'''


'''拼接archive检测url，默认提取该域名13-16年的快照'''

import StringIO,pycurl,time,random,re,os,csv,urllib,socket,sys,HTMLParser,whois
from threading import Thread,Lock
from Queue import Queue

current_time = time.strftime("%Y%m%d",time.localtime(time.time()))

def getHtml(url,headers):
    c = pycurl.Curl()    #通过curl方法构造一个对象
    #c.setopt(pycurl.REFERER, 'http://qy.m.58.com/')    #设置referer
    c.setopt(pycurl.FOLLOWLOCATION, True)    #自动进行跳转抓取
    c.setopt(pycurl.MAXREDIRS,5)            #设置最多跳转多少次
    c.setopt(pycurl.CONNECTTIMEOUT, 60)        #设置链接超时
    c.setopt(pycurl.TIMEOUT,120)            #下载超时
    c.setopt(pycurl.ENCODING, 'gzip,deflate')    #处理gzip内容，有些傻逼网站，就算你给的请求没有gzip，它还是会返回一个gzip压缩后的网页
    c.setopt(c.PROXY,'23.236.79.228:25')    # 代理
    c.fp = StringIO.StringIO()    
    c.setopt(pycurl.URL, url)    #设置要访问的URL
    c.setopt(pycurl.HTTPHEADER,headers)        #传入请求头
    # c.setopt(pycurl.POST, 1)
    # c.setopt(pycurl.POSTFIELDS, data)        #传入POST数据
    c.setopt(c.WRITEFUNCTION, c.fp.write)    #回调写入字符串缓存
    c.perform()        

    code = c.getinfo(c.HTTP_CODE)    #返回状态码
    html = c.fp.getvalue()    #返回源代码
    return html

headers = [
    "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding:gzip, deflate, sdch",
    "Accept-Language:zh-CN,zh;q=0.8,en;q=0.6",
    "Cache-Control:no-cache",
    "Cookie:wayback_server=75; CNZZDATA5024563=cnzz_eid%3D1864149450-1364016276-http%253A%252F%252Fweb.archive.org%26ntime%3D1364016276%26cnzz_a%3D2%26retime%3D1457686173418%26sin%3Dnone%26ltime%3D1457686173418%26rtime%3D0; ui3=1457877300; Hm_lvt_a9760a3d6beec272c93bcd6ad331996d=1457922674; bdshare_firstime=1457922676750; PVID=356507592938; visited=20160315; CNZZDATA5874432=cnzz_eid%3D863936874-1458135488-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1458135488; CNZZDATA1000382057=317424067-1458136374-http%253A%252F%252Fweb.archive.org%252F%7C1458136374; Hm_lvt_99dcf067895041504faa56ec21bcbb31=1458136393; CNZZDATA1000335018=396733047-1458137232-http%253A%252F%252Fweb.archive.org%252F%7C1458137232; __smToken=NKqQl40HtItHAADqL38mzesc; __atuvc=1%7C11; CNZZDATA5843659=cnzz_eid%3D1177950953-1452709876-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1452709876; Hm_lvt_c12ae5a7404dcf43567d8dd20252ea0a=1458140546; CNZZDATA3084975=cnzz_eid=54163074-1349405368-http%253A%252F%252Fweb.archive.org%252Fweb%252F*%252Fwww.zzchanke.com&ntime=1349405368&cnzz_a=1&retime=1458309353543&sin=none&ltime=1458309353543&rtime=0; CNZZDATA3017066=cnzz_eid%3D2082567497-1386657959-http%253A%252F%252Fweb.archive.org%26ntime%3D1386657882%26cnzz_a%3D0%26sin%3Dnone%26ltime%3D1458310695801; a9166_times=1; Hm_lvt_6d2fda750858f3d7dafab23f9bc0111f=1458310879; CNZZDATA4327894=cnzz_eid%3D1390851336-1420060092-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1420060092; CNZZDATA1000501466=1850261808-1458311167-http%253A%252F%252Fweb.archive.org%252F%7C1458311167; Hm_lvt_c3b8c6a896ae4b2e105499f81515b320=1458311727; Hm_lvt_3bfabfeae0eb27888d516cd6eadb8579=1458312250; CNZZDATA4022134=cnzz_eid=61277713-1341886377-http%253A%252F%252Fweb.archive.org%252Fweb%252F20150418190351%252Fhttp%253A%252F%252Fwww.exiuit.com%252F&ntime=1341886377&cnzz_a=0&retime=1458312470903&sin=none&ltime=1458312470903&rtime=0; CNZZDATA155540=cnzz_eid=82997278-1341161931-http%253A%252F%252Fweb.archive.org%252Fweb%252F20150418190351%252Fhttp%253A%252F%252Fwww.exiuit.com%252F&ntime=1341161931&cnzz_a=0&retime=1458312474148&sin=none&ltime=1458312474148&rtime=0; Hm_lvt_cc9108732961f96a2650e0226534b7ef=1458312690; CNZZDATA1658256=cnzz_eid%3D808205089-1456271567-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1456271567; CNZZDATA2920380=cnzz_eid%3D886651646-1447690099-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1447690099; CNZZDATA3675158=cnzz_eid%3D1644836704-1438591090-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1438591090; Hm_lvt_fdcf4e04d6793164b047f6814d1fb27e=1458315410; CNZZDATA3985489=cnzz_eid%3D1538296277-1422097548-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1422097548; GUID=35a47739-0360-43c7-b660-739aeaab327f; vct=1; CNZZDATA30039332=cnzz_eid%3D1139295155-1452669335-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1389839187%26cnzz_a%3D0%26sin%3Dnone%26ltime%3D1458319654822; _gscu_1416254272=58319872elf08t10; Hm_lvt_b70683a2021a193a3ca610efa8b2ea42=1458368248; Hm_lvt_1179210cc1d6fd038000f8c5fc159490=1458368567; a1079_times=1; a7871_times=1; pgv_pvi=1646538582; CNZZDATA1253509468=941683865-1418935190-http%253A%252F%252Fweb.archive.org%252F%7C1418935190; _cnzz_CV1253509468=toJSONString%7C%7C; sgsa_id=archive.org|1458383738445665; CNZZDATA3258717=cnzz_eid%3D358212149-1387859308-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1387859308%26cnzz_a%3D0%26sin%3Dnone%26ltime%3D1458383943530; CNZZDATA3765758=cnzz_eid%3D488513570-1438481235-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1438481235; CNZZDATA1254692310=37677455-1458385021-http%253A%252F%252Fweb.archive.org%252F%7C1458385021; Hm_lvt_6dd061a631f0c683f0ac5cf3ab8bcc50=1458385289; Hm_lvt_9c685da8a2112e332f867c5c417f6c8d=1458385383; lzstat_uv=35668732932304190945|2566952@2208862@3339480@2594874; CNZZDATA80714024=cnzz_eid%3D1354358359-1438655338-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1438655338; CNZZDATA4850181=cnzz_eid%3D1359994263-1387109010-http%253A%252F%252Fweb.archive.org%26ntime%3D1387109010%26cnzz_a%3D0%26sin%3Dnone%26ltime%3D1458386733972; Hm_lvt_27deb11e8ab112e9c19da7045e1c731d=1458383496; a9147_times=1; __utma=268623735.1911061433.1458140680.1458140680.1458390230.2; __utmz=268623735.1458140680.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=268623735.|1=Theme=CleanPeppermintBlack=1; CNZZDATA3537378=cnzz_eid%3D117760250-1416350229-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1416350229; CNZZDATA3960396=cnzz_eid%3D1193823713-1452613134-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1418959244; CNZZDATA1759739=cnzz_eid%3D1319658489-1419386919-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1400626577%26cnzz_a%3D0%26sin%3Dnone%26ltime%3D1458390642608; CNZZDATA4208364=cnzz_eid=44430815-1347394527-http%253A%252F%252Fweb.archive.org%252Fweb%252F*%252Fhttp%253A%252F%252Fwww.lxswed.com&ntime=1347394527&cnzz_a=0&retime=1458390818734&sin=none&ltime=1458390818734&rtime=0; looyu_id=79f525809bb0bd4a60ac060dd8f0d901c1_51197%3A1; CNZZDATA293206=cnzz_eid%3D711889795-1452390571-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1452390571; CNZZDATA5719050=cnzz_eid%3D937644064-1458385965-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1458441230; CNZZDATA3156024=cnzz_eid%3D1231311394-1438721523-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1438721523; pgv_pvid=5822316068; ts_uid=5696144012; CNZZDATA3351851=cnzz_eid%3D301703007-1418958900-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1418958900; a3663_times=1; a5362_times=1; CNZZDATA1850583=cnzz_eid%3D1678322967-1458469363-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1458469363; _ga=GA1.2.1911061433.1458140680; a2371_times=2; Hm_lvt_1736826e57811d9f7106b9b09963090c=1458386895; Hm_lvt_cc7c68ca6e0732df36608aed8e72564c=1458537288; Hm_lvt_fb6739b84b8b63fa6605272e81f965b7=1458558168; Hm_lvt_30885519281b128afa44e224e7a49e29=1458569656; Hm_lvt_07c9269a2ab0c159846a382d09a9a4ac=1458570042; AJSTAT_ok_times=10; YPF8827340282Jdskjhfiw_928937459182JAX666=207.241.229.214; a6292_times=2; CNZZDATA1254110291=829128679-1443476901-http%253A%252F%252Fweb.archive.org%252F%7C1428839594; CNZZDATA1255737199=253467276-1458572548-http%253A%252F%252Fweb.archive.org%252F%7C1458572548; _cnzz_CV1255737199=toJSONString%7C%7C; Hm_lvt_af46b9c9d17cb8aaab421511a24604f1=1458572641; CNZZDATA3842823=cnzz_eid%3D1933555479-1418983800-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1418983800; CNZZDATA5679085=cnzz_eid%3D894573438-1458572880-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1458572880; Hm_lvt_051cf16079eac247f7f3484afbd932a6=1458572881; Hm_lvt_455e62761cf1a1af7a36d0b68b8272b5=1458573030; a3377_times=1; CNZZDATA4710751=cnzz_eid%3D2007301519-1387814284-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1387814284%26cnzz_a%3D0%26sin%3Dnone%26ltime%3D1458573322307; isg=C688A618FB6C5CA4BE7A01E1C9CABC7C; l=AqGhnlQUeWAn/sHUsD/bKGdTMWe7ThVA; a4669_times=1; Hm_lvt_d3911f797350ab256b52a519546dd1e6=1458573521; CNZZDATA5955926=cnzz_eid%3D41553988-1458573523-http%253A%252F%252Fweb.archive.org%252F%26ntime%3D1458573523; Hm_lvt_aeabfe93e2f61b88aedad37f979b80e9=1458573524; PHPSESSID=qtdecbermc5c24mee033fa3rb5; JSESSIONID=DF49C178E0060FC17CAD65E6B8E775FB",
    "Host:web.archive.org",
    "Pragma:no-cache",
    "Proxy-Connection:keep-alive",
    "Upgrade-Insecure-Requests:1",
    "User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
]

def search(req,html):
     text = re.search(req,html)
     if text:
         data = text.group(1)
     else:
         data = 'no'
     return data



csvfile = file('/Users/sunjian/Desktop/hc项目/domain_xsjl/二轮过滤.csv', 'rb')         #读取二轮筛选文件
outfile = open('/Users/sunjian/Desktop/%s_域名捡漏_人肉筛选.csv' % current_time,'wb')
reader = csv.reader(csvfile)

req = open('/Users/sunjian/Desktop/hc项目/weijin.txt').read().strip()

api_url_list = []
for line in reader:
    domain = line[0]
    bd_idnex = line[1]
    daopai = line[2]
    sr = line[3]

    ''' request archive csx api '''
    archive_url = 'http://web.archive.org/cdx/search/cdx?url=%s&output=json&from=2013&to=2016&fl=timestamp,original' % domain
    api_url_list.append((domain,bd_idnex,daopai,sr,archive_url))


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
            domain = line[0]
            bd_idnex = line[1]
            daopai = line[2]
            sr = line[3]
            url = line[4]

            with self.lock: 
                self.running += 1

            html = getHtml(url,headers)
            data_tupe = re.findall(r'"(\d+)", "(http://[^"]*?)"',html)
            illegal_list = []
            if len(data_tupe) == 0:
                jieguo = '无历史快照'
                illegal_list = []
            else:
                black_url = []
                for line in data_tupe:
                    archive_url = 'http://web.archive.org/web/%s/%s' % (line[0],line[1])
                    archive_detail_html = getHtml(archive_url,headers)

                    tezheng = search('(%s)' % req,archive_detail_html)
                    if tezheng == 'no':
                        illegal = '正常'
                    else:
                        illegal = '违禁'
                        black_url.append(archive_url) #保存包含违禁内容的快照

                    print '----------->',domain,illegal,archive_url,tezheng

                    illegal_list.append(illegal)

            if len(illegal_list) == 0:
                data = []
                data.append(domain)
                data.append(bd_idnex)
                data.append(daopai)
                data.append(sr)
                data.append('无快照')
                data.append('')
                writer = csv.writer(outfile,dialect='excel')
                writer.writerow(data)                
            else:
                if '违禁' not in illegal_list:
                    data = []
                    data.append(domain)
                    data.append(bd_idnex)
                    data.append(daopai)
                    data.append(sr)
                    data.append('正常')
                    data.append('')
                    writer = csv.writer(outfile,dialect='excel')
                    writer.writerow(data)
                # else:
                #     data = []
                #     data.append(domain)
                #     data.append(bd_idnex)
                #     data.append(daopai)
                #     data.append(sr)
                #     data.append('违禁')
                #     data.append('%s' % ','.join(black_url))
                #     writer = csv.writer(outfile,dialect='excel')
                #     writer.writerow(data)
            
            self.q_ans.put(line)
            with self.lock:
                self.running -= 1
            self.q_req.task_done() # 在完成一项工作之后，Queue.task_done()
                                   # 函数向任务已经完成的队列发送一个信号
            time.sleep(0.1) # don't spam
 
'''获取api detail url'''
f = Fetcher(threads=10) #设置线程数
for url in api_url_list:
    f.push(url)         #所有url推入下载队列
while f.taskleft():     #若还有未完成的的线程
    f.pop()   #从下载完成的队列中取出结果



