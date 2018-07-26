# -*- coding: utf-8-*-
# 路线查询
import sys
import os
import re
import json, urllib
from urllib import urlencode
import socket

reload(sys)
sys.setdefaultencoding('utf8')

class linuxCommand(object):
	

	"""docstring for linuxCommand"""
	def __init__(self):

		self.data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/linux_command/data.json')

		pass

	def run(self,text,use_local=False):

		t_text = self.fenxiText(text)

		try:
			with open(self.data_file, 'r') as in_file:
			    command_data = json.load(in_file)
		except IOError:
			return ''

		result = ''
		desc = ''

		if command_data:
			if command_data.has_key(t_text):
				result = command_data[t_text]['n']
				desc = '命令:'+command_data[t_text]['n']+'\n说明:'+command_data[t_text]['d']
		try:
			if result=='':
				return ''
			else:
				if use_local:
					myname = socket.getfqdn(socket.gethostname(  ))
					#获取本机ip
					myaddr = socket.gethostbyname(myname)
					return desc+'\n更多查看:http://'+myaddr+'/wap/quicksearch.html?f='+result+'&s=linux&ip='+myaddr
				else:
					return desc+'\n更多查看:http://wangchujiang.com/linux-command/c/'+result+'.html'

		except IOError:
			return ''

	def fenxiText(self,text):
		PATTERN = ur'((?:linux )?[a-zA-Z\u4e00-\u9fa50-9]{0,5})'
		data_utf8 = text.decode('utf8')

		pattern = re.compile(PATTERN)

		m = pattern.search(data_utf8)

		return m.group(1).replace('linux ','').strip()