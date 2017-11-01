#!/usr/bin/env python
# coding: utf-8

import os
import sys
import datetime
import json
import time

reload(sys)
sys.setdefaultencoding('utf-8')


def alarmClock():
	time_now = datetime.datetime.now()
	time_string = time_now.strftime('%H:%M')
	current_data = time_now.strftime('%Y-%m-%d')

	data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rili.json')
	wdata = {}
	try:
	    with open(data_file, 'r') as in_file:
	        wdata = json.load(in_file)
	except IOError:
	    print "日历加载失败"
	    pass

	week_string = [1,2,3,4,5,6,0][time_now.isoweekday() - 1]

	if(isHoliday(current_data,wdata.get('data'),week_string)):
		url_mp3 = playVoice('holiday')
		if(time_string == '9:00'):
			text='今天是休息天'
		else:
			text=''

		url = u'http://tts.baidu.com/text2audio?idx=1&tex={0}&cuid=baidu_speech_' \
      u'demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=4&vol=5&pit=5'.format(text)
		os.system('mplayer "%s"' % url)
		time.sleep(5)
		os.system('mplayer "%s"' % url_mp3)
	else:
		url_mp3 = playVoice('work')
		if(time_string == '23:15'):
			text='该睡觉啦，明天还要上班'
		elif(time_string == '7:10'):
			text='起床啦，上班快迟到啦'
		else:
			text=''
		url = u'http://tts.baidu.com/text2audio?idx=1&tex={0}&cuid=baidu_speech_' \
      u'demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=4&vol=5&pit=5'.format(text)
		os.system('mplayer "%s"' % url)
		time.sleep(5)
		os.system('mplayer "%s"' % url_mp3)

def isHoliday(date,holidaylist,day):
	holidayResult={}
	weekEndButWork={}

	for i in holidaylist:
		for d in i.get('holiday'):
			for t in d.get('list'):
				if(t.get('status')=='1'):
					holidayResult[t.get('date')] = t.get('date')
				else:
					weekEndButWork[t.get('date')] = t.get('date')

	if(holidayResult.has_key(date)):
		return True
	else:
		if((day==6) or (day==0)):
			return True
		else:
			return False

def playVoice(otype):

	if(otype == 'holiday'):
		url = 'http://yinyueshiting.baidu.com/data2/music/34cf9ae4699054beaebcdc4f7bda1a9f/541957761/268081981219600128.mp3?xcode=4493b51a4cfc6fb338b319dd5c3c046e'
	else:
		url = 'http://yinyueshiting.baidu.com/data2/music/012ade6e82faf9105a86db57d77f2c1d/306963306/306962394151200320.mp3?xcode=86dde52bcbd00e5ab169a51e193c0fa9'

	return url	

if __name__ == '__main__': 
  alarmClock()