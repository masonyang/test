#!/usr/bin/env python
# coding: utf-8

import json
import os
import re
import sys
import time

import requests
from lxml import etree

output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weather.json')

def fail_exit(msg):
    with open(output_file, 'w') as out_file:
        json.dump({'error': msg}, out_file)
    sys.exit(1)
#上海 58367
#武汉 57494
html = ''
try:
    weather_file='http://www.nmc.cn/f/rest/weather/58367'

    r = requests.get(weather_file, timeout=10)
    r.encoding = 'utf-8'
    html = json.loads(r.text)[0]
except Exception, e:
    fail_exit(unicode(e))

result = {field: None for field in '''city_name current_temp current_weather
          current_wind current_humidity current_aq current_aq_desc
          today_weather today_temp_low today_temp_hig tomorrow_weather
          tomorrow_temp_low tomorrow_temp_hig tomorrow_wind tomorrow_aq
          tomorrow_aq_desc'''.split()}

result['city_name'] = html['station']['city']
result['current_temp'] = html['temperature']
result['current_weather'] = html['detail'][0]['day']['weather']['info']
result['current_wind'] = html['detail'][0]['day']['wind']['direct']
result['current_humidity'] = 0
result['current_aq'] = 0
result['current_aq_desc'] = 0
result['today_weather'] = html['detail'][0]['day']['weather']['info']
result['today_temp_hig'] = html['detail'][0]['day']['weather']['temperature']
result['today_temp_low'] = html['detail'][0]['night']['weather']['temperature']

result['tomorrow_weather'] = html['detail'][1]['day']['weather']['info']
result['tomorrow_temp_hig'] = html['detail'][1]['day']['weather']['temperature']
result['tomorrow_temp_low'] = html['detail'][1]['night']['weather']['temperature']
result['tomorrow_wind'] = html['detail'][1]['day']['wind']['direct']
result['tomorrow_aq'] = 0
result['tomorrow_aq_desc'] = 0

# for key in keys_require:
#     if not result.get(key):
#         fail_exit('can not get key %s' % key)

result['update'] = int(time.time())

# print json.dumps(result)
with open(output_file, 'w') as out_file:
    json.dump(result, out_file)