#!/usr/bin/env python
# coding: utf-8

import sys
import urllib
import urllib2
import json
import requests
import cookielib

reload(sys)
sys.setdefaultencoding('utf-8')

class serverapi(object):

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

		req=urllib2.Request(url,data)

		f=urllib2.urlopen(req)

		return f.read()
		pass

	def saveMemberInfo(self,source,data):

		url = 'http://www.god.com/index.php/openapi/b2c.memberinfo.'+source+'.update/save'

		params = {'_data':data}

		params = urllib.urlencode(params)

		return self.post(url,params)
		pass