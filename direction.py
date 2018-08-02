# -*- coding: utf-8-*-
# 路线查询
import sys
import os
import re
import json, urllib
from urllib import urlencode

reload(sys)
sys.setdefaultencoding('utf8')

class Direction(object):
	"""docstring for Direction"""
	def __init__(self):
		pass

	def run(self,text):

	    app_key = 'tzWgCACxPuNInF9LxklKVea3miAclbuf'

	    city = '上海'

	    or_igin,distine = self.fenxiText(text)

	    origin = self.suggestion(or_igin,city,app_key)

	    if origin == True:
	        return ''

	    destination = self.suggestion(distine,city,app_key)

	    if destination == True:
	        return ''

	    url_direction = "http://api.map.baidu.com/direction/v2/transit"
	    params_direction = {
	        "origin" : origin,
	        "destination" : destination,
	        "page_size" : 1,
	        "ak" : app_key,
	    }

	    res = self.request(url_direction, params_direction)
	    if res:
	        status = res["status"]
	        if status == 0:
	            if len(res['result']['routes']) > 0:
	                direction = ""
	                for step in res['result']['routes'][0]['steps']:
	                    direction = direction + step[0]["instructions"] + "."
	                    result = u"参考路线:" + direction

	                return result
	            else:
	                return ''
	        else:
	            return ''
	    else:
	        return ''

	def fenxiText(self,text):
		PATTERN = ur'([a-zA-Z0-9_\u4e00-\u9fa5]{1,10}?(?:到))([a-zA-Z0-9_\u4e00-\u9fa5]{1,10}?(?:怎么走)){0,3}'

		# data = '新疆维吾尔到伊犁州怎么走'

		data_utf8 = text.decode('utf8')

		pattern = re.compile(PATTERN)

		m = pattern.search(data_utf8)

		if m.lastindex >= 1:
			origin = m.group(1).replace('到','')
		if m.lastindex >= 2:
			distine = m.group(2).replace('怎么走','')

		return origin,distine

	def request(self,url, params):
	    params = urlencode(params)

	    f = urllib.urlopen("%s?%s" % (url, params))

	    content = f.read()
	    return json.loads(content)

	def suggestion(self,keyword,city,app_key):
	    url_place = "http://api.map.baidu.com/place/v2/suggestion"
	    params_place = {
	        "query" : keyword,
	        "region" : city,
	        "city_limit" : "true",
	        "output" : "json",
	        "ak" : app_key,
	    }

	    res = self.request(url_place, params_place)

	    if res:
	        status = res["status"]
	        if status == 0:
	            if len(res['result']) > 0:
	                # place_name = res['result'][0]["name"]
	                return "%f,%f" % (res['result'][0]["location"]['lat'], res['result'][0]["location"]['lng'])
	            else:
	                return ''
	        else:
	            return ''
	    else:
	        return ''
		