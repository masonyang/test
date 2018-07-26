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

class touTiao(object):

	search_url='https://www.toutiao.com/search_content/?offset=0&format=json&autoload=true&from=search_tab&count=20&'

	"""docstring for touTiao"""
	def __init__(self):
		pass

	def makeUrl(self,url,params):
		return url+params;
		pass

	def request(self,url):
		# print(url)
		request = urllib2.Request(url)

		f = urllib2.urlopen(request)

		return f.read()
		pass

	def post(self,url,data):

		cj=cookielib.CookieJar()

		opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

		headers = {
			'Host':'www.toutiao.com',
			'Referer':'http://www.toutiao.com',
			'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
			'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:57.0) Gecko/20100101 Firefox/57.0'
		}

		# opener.addheaders.append(('Cookie', 'cookiename=from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1514459685,1516864283; BAIDUID=141FBB37BF5CC999AEA7D0FFCE0EEFDA:FG=1; BIDUPSID=141FBB37BF5CC999AEA7D0FFCE0EEFDA; PSTM=1515216865; H_PS_PSSID=25576_1430_13701_21106_17001; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1516864283; PSINO=2; locale=zh; FP_UID=53b38a306486510e9fecf7834ddd5259'))
		
		req=urllib2.Request(url,data,headers)
		f=opener.open(req)

		return f.read()
		pass

	def _get_results(self, context):
		p = json.loads(context)
		return p
		pass

	def query(self,sentence):

		params={'keyword':sentence,'cur_tab':4}

		params = urllib.urlencode(params)

		url=self.makeUrl(self.search_url,params)

		result=self._get_results(self.request(url))

		arr=''

		try:
			for data in result['data']:
				if data.has_key('title') and data.has_key('share_url'):
					if data.has_key('has_video'):
						if data['has_video'] == True:
							continue
							# tag = '[视频]'
						else:
							tag = '[文章]'
					else:
						tag = ''

					arr = arr + tag + " " + data['title'] + ":" + data['share_url'] + "\n"
		except Exception:
			arr = '获取异常，请联系mason'

		return arr
