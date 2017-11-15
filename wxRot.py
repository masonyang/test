#!/usr/bin/env python
# coding: utf-8

import itchat,time
import datetime
import json
import os
import sys
import tesseract
import translate
from apscheduler.schedulers.background import BackgroundScheduler

reload(sys)
sys.setdefaultencoding('utf-8')

def lc():
	print 'lc'
	pass

def ec():
	print 'ec'
	os.system("kill -s `ps aux|grep -v grep|grep 'wechat_push.py'|awk '{print $2}'`")
	pass

def tick():
	rb = wxRot()
	msg = rb.weatherInfo()
	lists = rb.getFriends()

	for i in range(len(lists)):

	pass

class wxRot(object):
	"""docstring for wxRot"""
	def __init__(self):
		pass

	def auto_login(self):
		itchat.auto_login(hotReload=True,loginCallback=lc, exitCallback=ec)
		pass

	def sendNormalMsg(self,userName,msg):
		itchat.send(msg,toUserName=userName)
		pass

	def getFriends(self):
		lists = itchat.get_friends(update=True)
		return lists

	def scheduler(self):
		now = datetime.datetime.now() # 获取当前时间
		nextTickTime = now#+ dt.timedelta(days=1) #下一个问候时间为明天的现在
		nextTickTime = nextTickTime.strftime("%Y-%m-%d 22:00:00") # 把下一个问候时间设定为明天的零点
		self.myScheduler(nextTickTime)

	def run(self):
		itchat.run()
		pass

	def myScheduler(self,runTime):
		scheduler = BackgroundScheduler() # 生成对象
		scheduler.add_job(tick, 'date', run_date=runTime)  # 在指定的时间，只执行一次
		scheduler.start()

	def weatherInfo(self):
		weather_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weather.json')
		try:
			with open(weather_file, 'r') as in_file:
				wdata = json.load(in_file)
		except IOError:
			pass

		now = datetime.datetime.now()
		nextTickTime = now + datetime.timedelta(days=1)
		text=nextTickTime.strftime("%Y.%m.%d")+'天气情况: {tomorrow_weather},最高温度{tomorrow_temp_hig}℃,最低温度{tomorrow_temp_low}℃'.format(**wdata)

		return text
		pass

@itchat.msg_register(['Text','Map','Picture'])
def text_reply(msg):
	if(msg['Text'] == '天气'):
		weather_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weather.json')
		try:
			with open(weather_file, 'r') as in_file:
				wdata = json.load(in_file)
		except IOError:
			pass
		if(wdata['today_temp_hig']):
			text='今天{today_weather},最高温度{today_temp_hig}℃,最低温度{today_temp_low}℃. 明天{tomorrow_weather},最高温度{tomorrow_temp_hig}℃,最低温度{tomorrow_temp_low}℃'.format(**wdata)
		else:
			text='今天{today_weather},当前气温{current_temp}℃. 明天{tomorrow_weather},最高温度{tomorrow_temp_hig}℃,最低温度{tomorrow_temp_low}℃'.format(**wdata)
		return text
	elif(msg['Text'] == '音乐'):
		
		return ''
	elif(msg['Text'] == '视频'):
		
		return ''

	find = msg['Text'].find('翻译')

	if(find>=0):
		
		trans = translate.Translate()

		sentence = msg['Text'].replace('翻译','')

		f = trans.langdetect(sentence)

		text = trans.trans(sentence,f)

		return text
	else:
		return ''

@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def download_files(msg):

	pic = os.path.join(os.path.dirname(os.path.abspath(__file__)), msg['FileName'])
	with open(pic, 'wb') as f:
		f.write(msg['Text']())

	msginfo = ''

	if(msg['Type'] == 'Picture'):
		ocr = tesseract.Tesseract()
		msginfo = ocr.run_chi_en(pic)
		os.system('rm '+pic)
		# itchat.send(msginfo, msg['FromUserName'])
	return msginfo