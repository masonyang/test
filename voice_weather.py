#!/usr/bin/env python
# coding: utf-8

import os
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

home_air_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'home_air.json')

weather_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weather.json')

hadata = {}

wdata = {}

data = {}

try:
    with open(home_air_file, 'r') as in_file:
        hadata = json.load(in_file)
except IOError:
    pass

try:
    with open(weather_file, 'r') as in_file:
        wdata = json.load(in_file)
except IOError:
    pass

data = dict(hadata,**wdata)

text='当前室内温度{temp}度，室内湿度{humidity}度.明天{tomorrow_weather},最高温度{tomorrow_temp_hig}度,最低温度{tomorrow_temp_low}度'.format(**data)

url = u'http://tts.baidu.com/text2audio?idx=1&tex={0}&cuid=baidu_speech_' \
      u'demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=4&vol=5&pit=5'.format(text)
os.system('mplayer "%s"' % url)