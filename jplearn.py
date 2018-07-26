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

class JpLearn(object):
	
	mappings = {}

	scenes = {}

	"""docstring for JpLearn"""
	def __init__(self):
		self.mappings = {
			'第1课':'lesson_1',
			'第2课':'lesson_2',
			'第3课':'lesson_3',
			'第4课':'lesson_4',
			'第5课':'lesson_5',
			'第6课':'lesson_6',
			'第7课':'lesson_7',
			'第8课':'lesson_8',
			'第9课':'lesson_9',
			'第10课':'lesson_10',
			'第11课':'lesson_11',
			'第12课':'lesson_12',
			'第13课':'lesson_13',
			'第14课':'lesson_14',
			'第15课':'lesson_15',
			'第16课':'lesson_16',
			'第17课':'lesson_17',
			'第18课':'lesson_18',
			'第19课':'lesson_19',
			'第20课':'lesson_20',
			'第21课':'lesson_21',
			'第22课':'lesson_22',
			'第23课':'lesson_23',
			'第24课':'lesson_24',
			'第25课':'lesson_25',
			'第26课':'lesson_26',
			'第27课':'lesson_27',
			'第28课':'lesson_28',
			'第29课':'lesson_29',
			'第30课':'lesson_30',
			'第31课':'lesson_31',
			'第32课':'lesson_32',
			'第33课':'lesson_33',
			'第34课':'lesson_34',
			'第35课':'lesson_35',
			'第36课':'lesson_36',
			'第37课':'lesson_37',
			'第38课':'lesson_38',
			'第39课':'lesson_39',
			'第40课':'lesson_40',
			'第41课':'lesson_41',
			'第42课':'lesson_42',
			'第43课':'lesson_43',
			'第44课':'lesson_44',
			'第45课':'lesson_45',
			'第46课':'lesson_46',
			'第47课':'lesson_47',
			'第48课':'lesson_48',
		}

		self.scenes = {
		    '钢铁侠':'iron_man',
		    '蜘蛛侠':'spider_man',
		}

		pass

	def run(self,text,prefix='',l_type='',use_local=False):

		if l_type == 'grammar':
			lesson = self.fenxiGrammarText(text)
			try:
				filename = self.mappings[lesson.encode('utf8')]
			except Exception:
				return ''
		elif l_type == 'word':
			lesson = self.fenxiWordText(text)
			try:
				filename = self.mappings[lesson.encode('utf8')]
			except Exception:
				return ''
		elif l_type == 'scene':
			lesson = self.fenxiSceneText(text)
			try:
				filename = self.mappings[lesson.encode('utf8')]
			except Exception:
				return ''
		use_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/jp_'+l_type+'/'+filename+'.txt')

		try:
			if use_local:
				myname = socket.getfqdn(socket.gethostname(  ))
				#获取本机ip
				myaddr = socket.gethostbyname(myname)
				return '点击查看:http://'+myaddr+'/wap/quicksearch.html?f='+filename+'&s=jp&t='+l_type+'&ip='+myaddr
			else:
				res = ''
				for line in open(use_path):
					res = res + prefix +line
				return res
		except IOError:
			return '找不到' + lesson

	def fenxiWordText(self,text):
		# PATTERN = ur'(日语初级){0,4}?[\u4e00-\u9fa5]{1,10}'
		# data = '日语初级第N课'
		PATTERN = ur'((?:日语初级单词)?[\u4e00-\u9fa50-9]{1,10})'
		data_utf8 = text.decode('utf8')

		pattern = re.compile(PATTERN)

		m = pattern.search(data_utf8)

		return m.group(1).replace('日语初级单词','')

	def fenxiSceneText(self,text):
		PATTERN = ur'((?:日语场景)?[\u4e00-\u9fa50-9]{1,10})'
		data_utf8 = text.decode('utf8')

		pattern = re.compile(PATTERN)

		m = pattern.search(data_utf8)

		return m.group(1).replace('日语场景','')

	def fenxiGrammarText(self,text):
		# PATTERN = ur'(日语初级){0,4}?[\u4e00-\u9fa5]{1,10}'
		# data = '日语初级第N课'
		PATTERN = ur'((?:日语初级文法)?[\u4e00-\u9fa50-9]{1,10})'
		data_utf8 = text.decode('utf8')

		pattern = re.compile(PATTERN)

		m = pattern.search(data_utf8)

		return m.group(1).replace('日语初级文法','')