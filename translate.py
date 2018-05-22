#!/usr/bin/env python
# coding: utf-8

import sys
import urllib
import urllib2
import json
import requests
import execjs
import cookielib

reload(sys)
sys.setdefaultencoding('utf-8')

class Translate(object):

	transapi_url='http://fanyi.baidu.com/v2transapi?'

	langdetect_url='http://fanyi.baidu.com/langdetect?'

	"""docstring for Translate"""
	def __init__(self):
		pass

	def getConfig(self):
		
		pass

	def makeUrl(self,url,params):
		return url+params;
		pass

	def request(self,url):
		request = urllib2.Request(url)

		f = urllib2.urlopen(request)

		return f.read()
		pass

	def post(self,url,data):

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

	def _get_results(self, context):
		p = json.loads(context)
		return p
		pass

	def langdetect(self,sentence):

		params={'query':sentence}

		params = urllib.urlencode(params)

		url=self.makeUrl(self.langdetect_url,params)

		result=self._get_results(self.request(url))

		return result['lan']

		pass
	
	def trans(self,sentence,f):

		if(f == 'zh'):
			t = 'en'
		elif(f == 'en'):
			t = 'zh'

		jsstr = self.get_js()
		ctx = execjs.compile(jsstr)  
		sign = ctx.call('hash',sentence,'320305.131321201')

		params={'query':sentence,'from':f,'to':t,'simple_means_flag':'3','transtype':'translang','sign':sign,'token':'928fa64f0d8b452bf2ceba669c2e9244'}

		params = urllib.urlencode(params)

		# url=self.makeUrl(self.transapi_url,params)

		result=self._get_results(self.post(self.transapi_url,params))

		try:
			return result['trans_result']['data'][0]['dst']
		except:
			return result['query']

	def get_js(self):  
		f = open("/Users/yangminsheng/masonInPython/epaper_clock/baidu_transapi_sign.js", 'r')  
		line = f.readline()  
		htmlstr = ''  
		while line:
			htmlstr = htmlstr + line  
			line = f.readline()  
		return htmlstr

	def jpTrans(self,sentence,f):

		if(f == 'zh'):
			t = 'jp'
		elif(f == 'jp'):
			t = 'zh'

		jsstr = self.get_js()
		ctx = execjs.compile(jsstr)  
		sign = ctx.call('hash',sentence,'320305.131321201')

		params={'query':sentence,'from':f,'to':t,'simple_means_flag':'3','transtype':'translang','sign':sign,'token':'928fa64f0d8b452bf2ceba669c2e9244'}

		params = urllib.urlencode(params)

		# url=self.makeUrl(self.transapi_url,params)

		result=self._get_results(self.post(self.transapi_url,params))

		try:
			return result['trans_result']['data'][0]['dst']
		except:
			return result['query']