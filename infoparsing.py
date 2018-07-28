#!/usr/bin/env python
# coding: utf-8
import sys,os
import jieba
import translate
import json
import urllib
import	platform
import qqmail
import datetime
import direction
import jplearn
import toutiao
import nmc_weather
import linuxcommand

reload(sys)
sys.setdefaultencoding('utf-8')

class textParsing(object):
	"""docstring for textParsing"""
	def __init__(self, arg, friends='',askerName=''):
		self.keyWordList()
		self.text=arg
		self.friends=friends
		self.queryType = ''
		self.askerName = askerName
		self.myself = 'MasonPioneerYoung'

		self.result = self.weatherQuery(arg)
		if(self.result == ''):
			self.result = self.notJiebaParsing(arg)
			if(self.result == ''):
				self.result = self.masonServicesParsing(arg)
				if(self.result == ''):
					self.result = self.normalParsing(arg)
					if(self.result == ''):
						self.result = self.jbParsing(arg)
						if(self.result == ''):
							self.result = ''		
		pass

	def weatherQuery(self,text):
		nmcObj = nmc_weather.nmcWeather()

		result = nmcObj.has_cityinfo_by_cityname(text)

		if result == 'not_weather':
			self.queryType = ''
			return ''
		else:
			self.queryType = 'nmcWeatherQuery'
			return result

	def normalParsing(self,text):
		self.seg_list = text
		if text in self.otherKw:
			return text
		return ''

	def keyWordList(self):
		self.notJieba=['怎么走','日语初级文法','日语初级单词','日语初级场景','日语手册','linux']
		self.kw=['日文翻译','翻译','日文','买','视频','头条']
		self.otherKw=['英语天气','好友','功能提示','查找充电桩']
		self.masonServices=['开启','关闭','关电脑','关机','休眠','重启','发送']
		self.mappings={'日文':'jpTranslate','日文翻译':'jpTranslate','翻译':'translate','英语天气':'enWeather','买':'jdBuy','好友':'getFriends','视频':'videoSearch','功能提示':'newTip','怎么走':'useDirection','日语初级文法':'juniorJpGrammar','日语初级单词':'juniorJpWord','日语场景':'jpScene','日语手册':'jpManual','头条':'touTiaoQuery','linux':'linux_command','查找充电桩':'findElecStation'}
		self.masonServicesMappings={'开启':'masonComputerServices','关闭':'masonComputerServices','关电脑':'masonComputerServices','关机':'masonComputerServices','休眠':'masonComputerServices','重启':'masonComputerServices','发送':'masonComputerServices'}
		pass

	def jbParsing(self,text):
		seg_list1=jieba.cut(text,cut_all=False)

		self.seg_list = seg_list1

		for i in seg_list1:
			if i in self.kw:
				return i
		return ''

	def masonServicesParsing(self,text):
		seg_list1=jieba.cut(text,cut_all=False)

		self.seg_list = seg_list1

		for i in seg_list1:
			if i in self.masonServices:
				return i
		return ''

	def notJiebaParsing(self,text):
		for k in self.notJieba:
			if text.find(k) == -1:
				continue;
			else:
				return k
		return ''

	def done(self):
		if(self.result and self.queryType == ''):
			try:
				method_name = self.mappings[self.result.encode("utf8")]
			except Exception, e:
				method_name = self.masonServicesMappings[self.result.encode("utf8")]

			method = getattr(self, method_name, lambda: "nothing")
			#根据fromUserName的permission来决定是否执行
			return method(self.result)
		elif (self.result and self.queryType != ''):
			
			method_name = self.queryType

			method = getattr(self, method_name, lambda: "nothing")
			#根据fromUserName的permission来决定是否执行
			return method(self.result)
		else:
			return ''

	def nmcWeatherQuery(self,code):

		nmcObj = nmc_weather.nmcWeather()

		return nmcObj.get_weather_by_cityname(code,self.text)

	def translate(self,prefix):
		trans = translate.Translate()

		s = self.text.decode('utf8')[2:].encode('utf8')

		sentence = s.strip()

		if(sentence == ''):
			return ''
		else:
			f = trans.langdetect(sentence)

			text = trans.trans(sentence,f)

			return text

	def weather(self,prefix):
		weather_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weather.json')
		try:
			with open(weather_file, 'r') as in_file:
				wdata = json.load(in_file)
		except IOError:
			pass
		if(wdata['today_weather'] == '9999'):
			text='当前气温{current_temp}℃. 明天{tomorrow_weather},最高温度{tomorrow_temp_hig}℃,最低温度{tomorrow_temp_low}℃'.format(**wdata)
		else:
			text='今天{today_weather},最高温度{today_temp_hig}℃,最低温度{today_temp_low}℃. 明天{tomorrow_weather},最高温度{tomorrow_temp_hig}℃,最低温度{tomorrow_temp_low}℃'.format(**wdata)

		tomorrow_temp_hig=float(wdata['tomorrow_temp_hig'])

		tomorrow_temp_low=float(wdata['tomorrow_temp_low'])

		if(tomorrow_temp_hig>35):
			otherInfo='(已经进入高温烘烤模式，注意防暑降温....)'
		elif(tomorrow_temp_hig>30):
			otherInfo='(天气开始热起来....)'
		elif(tomorrow_temp_low<=0):
			otherInfo='(温度已跌破零点，注意防寒保暖，全副武装....)'
		else:
			otherInfo=''

		text = text+"\n更多信息请登录http://m.nmc.cn/publish/forecast/ASH/shanghai.html\n"+otherInfo

		# text+="\n("+self.transMutiLangMsg(text,'en')+")"

		return text

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

	def enWeather(self,prefix):
		weather_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weather.json')
		try:
			with open(weather_file, 'r') as in_file:
				wdata = json.load(in_file)
		except IOError:
			pass
		if(wdata['today_weather'] == '9999'):
			text='当前气温{current_temp}℃. 明天{tomorrow_weather},最高温度{tomorrow_temp_hig}℃,最低温度{tomorrow_temp_low}℃'.format(**wdata)
		else:
			text='今天{today_weather},最高温度{today_temp_hig}℃,最低温度{today_temp_low}℃. 明天{tomorrow_weather},最高温度{tomorrow_temp_hig}℃,最低温度{tomorrow_temp_low}℃'.format(**wdata)

		trans = translate.Translate()

		f = trans.langdetect(text)

		sentence = trans.trans(text,f)

		return sentence

	def jpTranslate(self,prefix):
		trans = translate.Translate()

		length = len(prefix)
		s = self.text.decode('utf8')[length:].encode('utf8')

		sentence = s.strip()

		if(sentence == ''):
			return ''
		else:
			f = trans.langdetect(sentence)
			
			text = trans.jpTrans(sentence,f)

			return text

	def touTiaoQuery(self,prefix):
		length = len(prefix)
		s = self.text.decode('utf8')[length:].encode('utf8')

		text = s.strip()

		if(text == ''):
			return ''
		else:
			tt = toutiao.touTiao()

			return tt.query(text)

	def getFriends(self,prefix):
		output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'friends.json')

		if os.path.exists(output_file):
			return '已获取过'
		else:	
			with open(output_file, 'w') as out_file:
				json.dump(self.friends, out_file)
			return '获取成功'

	def masonComputerServices(self,prefix):

		openCommand={'QQ':'/Applications/QQ.app','qq':'/Applications/QQ.app','火狐':'/Applications/Firefox.app','谷歌':'/Applications/Google\ Chrome.app','微信':'/Applications/WeChat.app','phpstorm':'/Applications/PhpStorm.app','sublime':'/Applications/Sublime\ Text\ 2.app'}

		closeCommand={'QQ':'QQ','qq':'QQ','火狐':'firefox','谷歌':'Google\ Chrome','微信':'WeChat','phpstorm':'phpstorm','sublime':'Sublime\ Text\ 2'}

		re_turn = '出现异常,执行失败'
		if platform.system() == 'Darwin':
			if prefix == '开启':
				for i in self.seg_list:
					try:
						command = openCommand[i.encode("utf8")]
						if command:
							os.system('open '+openCommand[i.encode("utf8")])
							re_turn = '已开启'+i
					except Exception, e:
						return ''
			elif prefix == '关闭':
				for i in self.seg_list:
					try:
						command = closeCommand[i.encode("utf8")]
						if command:
							os.system('killall '+closeCommand[i.encode("utf8")])
							re_turn = '已关闭'+i
					except Exception, e:
						return ''
			elif (prefix == '关电脑' or prefix == '关机'):
				os.system('sudo /sbin/shutdown -h now')
				re_turn = '已'+prefix
			elif (prefix == '休眠'):
				os.system('sudo /sbin/shutdown -s now')
				re_turn = '已'+prefix
			elif (prefix == '重启'):
				os.system('sudo /sbin/shutdown -r now')
				re_turn = '已'+prefix
			elif (prefix == '发送'):
				for i in self.seg_list:
					try:
						command = i.encode("utf8")
						if command == '邮件':
							# 'guofang':'244241235@qq.com','jason':'313588655@qq.com',
							arr = {'mason':'530369682@qq.com'}
							for j in arr:
								time_now = datetime.datetime.now()
								date_string = time_now.strftime('%Y年%m月%d日')
								text = qqmail.getInfo(arr[j])
								qqmail.SendEmail("530369682@qq.com",arr[j],date_string+"气温报告","hello",text+'---来自Mason')
							re_turn = '已发送'+i
					except Exception, e:
						return ''
		return re_turn

	def newTip(self,prefix):

		msg = "新功能:\n"
		# msg+="1.查看今明天气,输入:天气\n\n"
		msg+="1.查看某个城市地区的天气,输入:***天气。\n 【其他城市地区: 省市+地区，如:湖北省武汉、黑龙江省齐齐哈尔】\n【上海地区支持: 崇明、嘉定、闵行、南汇、宝山、上海、奉贤、金山、松江、浦东、青浦】\n\n"
		msg+="2.中译英、英译中,输入:翻译 我是谁/who am I \n【日文翻译使用: 日文翻译 我是谁】\n\n"
		msg+="3.买衣服、3c产品,输入:(想/打算/准备)买iphone\n\n"
		msg+="4.搜索电视剧、电影,输入:视频 星球大战\n\n"
		msg+="5.问路,输入:人民公园到淮海路怎么走\n\n"
		msg+="6.新能源车充电桩查询,输入:查找充电桩\n\n"
		msg+="7.搜索查找新闻、视频、文章、资料信息,输入:头条 什么是区块链\n\n"
		msg+="8.liunx命令速查,输入:linux ls\n\n"
		if(self.askerName == self.myself):
			msg+="通过输入:日语初级文法第N课.来学习\n\n"
			msg+="通过输入:日语初级场景第N课.来学习\n\n"
			msg+="通过输入:日语初级单词第N课.来学习\n\n"
			msg+="通过输入:日语手册片假名.来学习\n\n"
		return msg

	def findElecStation(self,prefix):
		return "请访问: https://www.powerlife.com.cn/pile/ops/map/default.html"

	def videoSearch(self,prefix):
		url = 'http://m.iqiyi.com/search.html?source=input&vfrm=2-3-0-1&'

		s = self.text.decode('utf8')[2:].encode('utf8')

		sentence = s.strip()

		return url+urllib.urlencode({'key':sentence})

	def juniorJpGrammar(self,prefix):
		if(self.askerName == self.myself):
			use_local = True
		else:
			use_local = False
		learn = jplearn.JpLearn()
		return learn.run(self.text,'','grammar',use_local)

	def juniorJpWord(self,prefix):
		if(self.askerName == self.myself):
			use_local = True
		else:
			use_local = False
		learn = jplearn.JpLearn()
		return learn.run(self.text,'','word',use_local)

	def jpScene(self,prefix):
		if(self.askerName == self.myself):
			use_local = True
		else:
			use_local = False
		learn = jplearn.JpLearn()
		return learn.run(self.text,'','scene',use_local)

	def jpManual(self,prefix):
		if(self.askerName == self.myself):
			use_local = True
		else:
			use_local = False
		learn = jplearn.JpLearn()
		return learn.run(self.text,'','manual',use_local)

	def useDirection(self,prefix):
		direct = direction.Direction()
		return direct.run(self.text)

	def linux_command(self,prefix):
		if(self.askerName == self.myself):
			use_local = True
		else:
			use_local = False
		lc = linuxcommand.linuxCommand()
		return lc.run(self.text,use_local)

	def jdBuy(self,prefix):
		url = 'https://so.m.jd.com/ware/search.action?'

		exp_words = ['打算','想','准备']

		for j in exp_words:
			if self.text.find(j) == -1:
				continue
			else:	
				for i in self.seg_list:
					return url+urllib.urlencode({'keyword':i})
