#!/usr/bin/env python
# coding: utf-8

import urllib
import urllib2
import json
import requests
import execjs
import cookielib
import serverapi
import os
import qqmail
import datetime
import infoparsing
import time

transapi_url='http://fanyi.baidu.com/v2transapi?'

def makeUrl(url,params):
	return url+params;
	pass

def post(url,data):
	# request = urllib2.Request(url)

	cj=cookielib.CookieJar()

	opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

	headers = {
		'Host':'fanyi.baidu.com',
		'Referer':'http://fanyi.baidu.com/translate?aldtype=16047&query=&keyfrom=baidu&smartresult=dict&lang=auto2zh',
		'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:57.0) Gecko/20100101 Firefox/57.0'
	}

	opener.addheaders.append(('Cookie', 'cookiename=from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1514459685,1516864283; BAIDUID=141FBB37BF5CC999AEA7D0FFCE0EEFDA:FG=1; BIDUPSID=141FBB37BF5CC999AEA7D0FFCE0EEFDA; PSTM=1515216865; H_PS_PSSID=25576_1430_13701_21106_17001; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1516864283; PSINO=2; locale=zh; FP_UID=53b38a306486510e9fecf7834ddd5259'))

	req=urllib2.Request(url,data,headers)
	f=opener.open(req)

	return f.read()
	pass

def get_js():  
    # f = open("D:/WorkSpace/MyWorkSpace/jsdemo/js/des_rsa.js",'r',encoding='UTF-8')  
    f = open("/Users/yangminsheng/masonInPython/epaper_clock/baidu_transapi_sign.js", 'r')  
    line = f.readline()  
    htmlstr = ''  
    while line:  
        htmlstr = htmlstr + line  
        line = f.readline()  
    return htmlstr  

def _get_results(context):
	p = json.loads(context)
	return p
	pass

def readConfig(key):
	f=open('/Users/yangminsheng/masonInPython/epaper_clock/readJson.json')

	setting = json.load(f)

	commonNotice = setting[key]

	time_now = datetime.datetime.now()
	time_string = time_now.strftime('%H:%M')
	week_string = [1,2,3,4,5,6,0][time_now.isoweekday() - 1]
	for items in commonNotice:
		if(items['scheduleType']=='notice_week'):
			for week in items['timeSlot']:
				if(week == week_string):
					print week
		elif(items['scheduleType'] == 'notice_everyday'):#每日提醒任务
			if week_string in items['timeSlot']:#依周几和时间点为判断
				if time_string in items['timeDot']:
					if(items['sayNotice']):
						
						if(items['action']=='timebroadcast'):
							items['sayNotice'] = items['sayNotice'] + time_string

						url = u'http://tts.baidu.com/text2audio?idx=1&tex={0}&cuid=baidu_speech_' \
						u'demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=4&vol=5&pit=5'.format(items['sayNotice'])
						os.system('mplayer "%s"' % url)
						time.sleep(5)
					if(items['noticeMusic']):
						os.system('mplayer "%s"' % items['noticeMusic'])
			elif time_string in items['timeDot']:#只依据时间点为判断
					if(items['sayNotice']):
						url = u'http://tts.baidu.com/text2audio?idx=1&tex={0}&cuid=baidu_speech_' \
						u'demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=4&vol=5&pit=5'.format(items['sayNotice'])
						os.system('mplayer "%s"' % url)
						time.sleep(5)
					if(items['noticeMusic']):
						os.system('mplayer "%s"' % items['noticeMusic'])
		pass

	return True


a='现在'

a = a + '哈哈'

print a
# print readConfig('commonNotice')

# obj = infoparsing.textParsing('新功能')
# print obj.done()
# jsstr = get_js()  
# ctx = execjs.compile(jsstr)  

# sentence = '我是谁'

# sign = ctx.call('hash',sentence,'320305.131321201')

# params={'query':sentence,'from':'zh','to':'en','simple_means_flag':'3','transtype':'translang','sign':sign,'token':'928fa64f0d8b452bf2ceba669c2e9244'}

# params = urllib.urlencode(params)

# # url=makeUrl(transapi_url,params)

# result=_get_results(post(transapi_url,params))

# api = serverapi.serverapi()

# output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'friends.json')

# try:
# 	with open(output_file, 'r') as in_file:
# 		wdata = json.load(in_file)
# except IOError:
# 	wdata = ''
# 	pass

# api.saveMemberInfo('wechat',output_file)


# time_now = datetime.datetime.now()
# date_string = time_now.strftime('%Y年%m月%d日')
# text = qqmail.getInfo('530369682@qq.com')
# qqmail.SendEmail("530369682@qq.com",'530369682@qq.com',date_string+"气温报告","hello",text+'---来自Mason')




