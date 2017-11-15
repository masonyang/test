#!/usr/bin/env python
# coding: utf-8

import sys
import urllib
import urllib2
import json
import requests

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

		params={'query':sentence,'from':f,'to':t,'simple_means_flag':'3','transtype':'translang'}

		params = urllib.urlencode(params)

		url=self.makeUrl(self.transapi_url,params)

		result=self._get_results(self.request(url))

		try:
			return result['trans_result']['data'][0]['dst']
		except:
			return result['query']