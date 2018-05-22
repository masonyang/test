#!/usr/bin/env python
# coding: utf-8

import itchat,time
import datetime
import json
import os
import sys
import tesseract
import translate
import infoparsing
import serverapi
from apscheduler.schedulers.background import BackgroundScheduler

reload(sys)
sys.setdefaultencoding('utf-8')

def lc():
	rb = wxRot()

	friends = rb.getFriends()

	output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'friends.json')

	with open(output_file, 'w') as out_file:
		json.dump(friends, out_file)

	api = serverapi.serverapi()

	api.saveMemberInfo('wechat',output_file)

	print 'lc'
	pass

def ec():
	print 'ec'
	os.system("kill -s `ps aux|grep -v grep|grep 'wechat_push.py'|awk '{print $2}'`")
	pass

def tick():
	rb = wxRot()
	lists = rb.getFriends()

	obj = infoparsing.textParsing('新功能',lists)
	func_tip = "\n\n【可以通过回复'功能提示'来获取更多功能使用说明】"
	# newTip = obj.done()
	# msg+="\n("+rb.transMutiLangMsg(msg,'en')+" —— From Baidu)"

	msg_common = rb.TipMsg() + rb.weatherInfo() + func_tip

	msg_special = rb.TipMsg() + rb.weatherWuHanInfo() + func_tip

	for i in range(len(lists)):
		if(lists[i]['PYQuanPin'] == 'Qiqi'):
			rb.sendNormalMsg(lists[i]['UserName'],msg_special)
		elif(lists[i]['PYQuanPin'] == 'tiande'):
			rb.sendNormalMsg(lists[i]['UserName'],msg_common)
		elif(lists[i]['PYQuanPin'] == 'Jason' and lists[i]['RemarkPYQuanPin']==''):
			rb.sendNormalMsg(lists[i]['UserName'],msg_common)
		elif(lists[i]['PYQuanPin'] == 'guofang'):
			rb.sendNormalMsg(lists[i]['UserName'],msg_common)
	pass

# msg+="\n("+rb.transMutiLangMsg(msg,'en')+")"
# elif(lists[i]['PYQuanPin'] == 'ekkispanclassemojiemoji1f43espan'):
# rb.sendNormalMsg(lists[i]['UserName'],msg)	
# if(lists[i]['RemarkPYQuanPin']=='chenlei'):
# rb.sendNormalMsg(lists[i]['UserName'],msg)
# elif(lists[i]['PYQuanPin'] == 'LiLi'):
# rb.sendNormalMsg(lists[i]['UserName'],msg)
# if(lists[i]['PYQuanPin']=='MasonDoraemonYoung'):
# rb.sendNormalMsg(lists[i]['UserName'],msg)
# if(lists[i]['PYQuanPin'] == 'Pearllaojiang'):
# rb.sendNormalMsg(lists[i]['UserName'],msg)
# elif(lists[i]['PYQuanPin'] == 'mengmeng' and lists[i]['RemarkPYQuanPin']=='xuhui'):
# rb.sendNormalMsg(lists[i]['UserName'],msg)
# elif(lists[i]['PYQuanPin'] == 'guobaqiangsen'):
# rb.sendNormalMsg(lists[i]['UserName'],msg)
# elif(lists[i]['PYQuanPin'] == 'Pearllaojiang'):
# rb.sendNormalMsg(lists[i]['UserName'],msg)
# elif(lists[i]['PYQuanPin'] == 'mengmeng' and lists[i]['RemarkPYQuanPin']=='xuhui'):
# rb.sendNormalMsg(lists[i]['UserName'],msg)
# elif(lists[i]['PYQuanPin'] == 'tongyuwei'):
# rb.sendNormalMsg(lists[i]['UserName'],msg)

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

	def transMutiLangMsg(self,msg,to):
		trans = translate.Translate()

		if(to == 'en'):
			f = 'zh'
		elif(to == 'zh'):
			f = 'en'
		# f = trans.langdetect(msg)
		sentence = trans.trans(msg,f)

		return sentence
		pass

	def getFriends(self):
		lists = itchat.get_friends(update=True)
		return lists

	def scheduler(self):
		now = datetime.datetime.now() # 获取当前时间
		nextTickTime = now#+ dt.timedelta(days=1) #下一个问候时间为明天的现在
		nextTickTime = nextTickTime.strftime("%Y-%m-%d 22:08:00") # 把下一个问候时间设定为明天的零点
		self.myScheduler(nextTickTime)

	def run(self):
		itchat.run()
		pass

	def myScheduler(self,runTime):
		scheduler = BackgroundScheduler() # 生成对象
		scheduler.add_job(tick, 'date', run_date=runTime)  # 在指定的时间，只执行一次
		scheduler.start()

	def TipMsg(self):
		now = datetime.datetime.now()
		nextTickTime = now + datetime.timedelta(days=1)
		nextTime=nextTickTime.strftime("%Y.%m.%d")

		if(nextTime == '2018.01.01'):
			return "\n (元旦快乐，2018加油！)"
		elif(nextTime == '2018.01.03' or nextTime == '2018.01.04' or nextTime == '2018.01.05' or nextTime == '2018.01.06' or nextTime == '2018.01.07'):
			return "\n (本周开启阴雨模式,记得带伞，注意保暖！)"
		elif(nextTime == '2018.02.14' or nextTime == '2018.02.15' or nextTime == '2018.02.16'):

			otherInfo = ""

			if(nextTime == '2018.02.14'):
				otherInfo = '明天是小年夜，'
			else:
				otherInfo = "新年快乐！"

			return "("+otherInfo+" Mason给您拜年啦～ 祝 阖家幸福，事业有成，万事如意，岁岁平安，Happy New Year！) \n"
		else:
			return ""
		pass

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


		tomorrow_temp_hig=float(wdata['tomorrow_temp_hig'])

		tomorrow_temp_low=float(wdata['tomorrow_temp_low'])
		
		otherInfo=''

		if(tomorrow_temp_hig>35):
			otherInfo="\n(已经进入高温烘烤模式，注意防暑降温....)"
		elif(tomorrow_temp_hig>30):
			otherInfo="\n(天气开始热起来....)"
		elif(tomorrow_temp_low<=0):
			otherInfo="\n(温度已跌破零点，注意防寒保暖，全副武装....)"

		text = text+"\n更多信息请登录http://m.nmc.cn/publish/forecast/ASH/shanghai.html"+otherInfo
		return text
		pass

	def weatherWuHanInfo(self):

		weather_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weather_wuhan.json')
		try:
			with open(weather_file, 'r') as in_file:
				wdata = json.load(in_file)
		except IOError:
			pass

		now = datetime.datetime.now()
		nextTickTime = now + datetime.timedelta(days=1)
		text= '【武汉】'+nextTickTime.strftime("%Y.%m.%d")+'天气情况: {tomorrow_weather},最高温度{tomorrow_temp_hig}℃,最低温度{tomorrow_temp_low}℃'.format(**wdata)


		tomorrow_temp_hig=float(wdata['tomorrow_temp_hig'])

		tomorrow_temp_low=float(wdata['tomorrow_temp_low'])
		
		otherInfo=''

		if(tomorrow_temp_hig>35):
			otherInfo="\n(已经进入高温烘烤模式，注意防暑降温....)"
		elif(tomorrow_temp_hig>30):
			otherInfo="\n(天气开始热起来....)"
		elif(tomorrow_temp_low<=0):
			otherInfo="\n(温度已跌破零点，注意防寒保暖，全副武装....)"

		text = text+"\n更多信息请登录http://m.nmc.cn/publish/forecast/AHB/wuhan.html"+otherInfo

		return text
		pass

@itchat.msg_register(['Text','Map','Picture'])
def text_reply(msg):
	friends=itchat.get_friends(update=True)
	obj = infoparsing.textParsing(msg['Text'],friends)
	return obj.done()

@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def download_files(msg):
	msginfo = ''
	# pic = os.path.join(os.path.dirname(os.path.abspath(__file__)), msg['FileName'])
	# with open(pic, 'wb') as f:
	# 	f.write(msg['Text']())

	# if(msg['Type'] == 'Picture'):
	# 	friends=itchat.get_friends(update=True)

	# 	for i in range(len(friends)):
	# 		if((friends[i]['PYQuanPin'] == 'MasonDoraemonYoung') and (msg['User']['PYQuanPin'] == 'MasonDoraemonYoung')):
	# 			ocr = tesseract.Tesseract()
	# 			msginfo = ocr.run_jpn(pic)#日语

	# os.system('rm '+pic)
		# itchat.send(msginfo, msg['FromUserName'])
	return msginfo