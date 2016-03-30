#coding:utf-8

import os,time,csv,re

'''提取原始域名中不可访问的域名'''
print '---------------》从domain_original表中提取查询域名，检测域名可访问性'
os.system('cd /Users/sunjian/Desktop/hc项目/domain_xsjl ; python domain_request.py')

time.sleep(10)

'''检测域名可否注册'''
print '---------------》检测域名是否被注册'
os.system('cd /Users/sunjian/Desktop/hc项目/domain_xsjl/domain_zhuce ; rm jieguo.csv ; scrapy crawl zhuce -o jieguo.csv')

time.sleep(10)

'''提取可注册的域名'''
print '---------------》过滤可注册的域名'
csvfile = file('/Users/sunjian/Desktop/hc项目/domain_xsjl/domain_zhuce/jieguo.csv', 'rb')
zhucefile = open('/Users/sunjian/Desktop/hc项目/domain_xsjl/可注册.txt','w')
reader = csv.reader(csvfile)

for line in reader:
    domain = line[0]
    zhuce = line[1]

    if zhuce == '可注册':
    	zhucefile.write('%s\n' % domain)
csvfile.close()

time.sleep(10)


'''检查百度、搜狗数据'''
print '---------------》查询百度索引，泛解析、敏感词，查询搜狗SR'
os.system('cd /Users/sunjian/Desktop/hc项目/domain_xsjl/domain_filter ; rm jieguo.csv ; scrapy crawl domain -o jieguo.csv')

time.sleep(10)


'''进行一轮过滤'''
print '---------------》一轮过滤，删除包含敏感词、泛解析、英文站，提取收录>0或SR>2的域名'
csvfile = file('/Users/sunjian/Desktop/hc项目/domain_xsjl/domain_filter/jieguo.csv', 'rb')
outfile = open('/Users/sunjian/Desktop/hc项目/domain_xsjl/一轮过滤.csv','w')
reader = csv.reader(csvfile)

def search(req,html):
     text = re.search(req,html)
     if text:
         data = text.group(1)
     else:
         data = 'no'
     return data

n = 0
m = 0
for line in reader:
	shijian = line[0]
	word = line[1]
	bd_index = line[2]
	reverse_index = line[3]
	chinese = line[4]
	illegal = line[6]
	pan_analysis = line[7]
	sgsr = line[8]

	m += 1


	if search('^(\d+)$',bd_index) == 'no' or search('^(\d+)$',sgsr) == 'no':
		continue

	if chinese != 'english' and pan_analysis != '泛解析' and illegal != '包含违禁词':
		if int(sgsr) > 1 or int(bd_index) > 0:

			data = []
			data.append(word)
			data.append(bd_index)
			data.append(reverse_index)
			data.append(sgsr)
			writer = csv.writer(outfile,dialect='excel')
			writer.writerow(data)
			n += 1
csvfile.close()
print '一轮过滤数据：查询总数：%s，提取：%s' % (m,n)

time.sleep(10)


'''抓取360安全数据'''
print '---------------》抓取360安全数据'
os.system('cd /Users/sunjian/Desktop/hc项目/domain_xsjl/so360/ ; rm 360.csv ; scrapy crawl 360 -o 360.csv')

time.sleep(10)

'''删除360有安全提示的域名'''
print '---------------》删除被黑、被攻击、不安全的域名'
csvfile = file('/Users/sunjian/Desktop/hc项目/domain_xsjl/so360/360.csv', 'rb')
reader = csv.reader(csvfile)

outfile = open('/Users/sunjian/Desktop/hc项目/domain_xsjl/二轮过滤.csv','wb')

def search(req,html):
     text = re.search(req,html)
     if text:
         data = text.group(1)
     else:
         data = 'no'
     return data

n = 0
m = 0
for line in reader:
	sr = line[0]
	bd_index = line[1]
	daopai = line[2]
	score = line[3]
	word = line[4]

	m += 1
	if score != '不安全':
		data = []
		data.append(word)
		data.append(bd_index)
		data.append(daopai)
		data.append(sr)
		writer = csv.writer(outfile,dialect='excel')
		writer.writerow(data)
		n += 1
csvfile.close()
print '二轮过滤数据：查询总数：%s，删除：%s' % (m,m-n)


time.sleep(10)

'''检查archive历史快照'''
os.system(' cd /Users/sunjian/Desktop/hc项目/domain_xsjl ; python archive_url.py ')


