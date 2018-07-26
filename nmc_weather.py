#!/usr/bin/env python
# coding: utf-8
import re
import sys
import datetime
import os
import json
import time
import requests

#http://www.nmc.cn/f/rest/province

#http://www.nmc.cn/f/rest/province/ASH

#http://www.nmc.cn/f/rest/weather/58367

reload(sys)
sys.setdefaultencoding('utf8')

class nmcWeather(object):

    cityname_alias = {
        '崇明':'上海市崇明',
        '嘉定':'上海市嘉定',
        '闵行':'上海市闵行',
        '南汇':'上海市南汇',
        '宝山':'上海市宝山',
        '上海':'上海市上海',
        '奉贤':'上海市奉贤',
        '金山':'上海市金山',
        '松江':'上海市松江',
        '浦东':'上海市浦东',
        '青浦':'上海市青浦',
    }

    """docstring for nmcWeather"""
    def __init__(self):
        self.nmc_province_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/weather/nmc_province.json')

        self.city_province_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/weather/nmc_city_province.json')

    def save_city_info(self):
        try:
            with open(self.nmc_province_file, 'r') as in_file:
                nmc_province_data = json.load(in_file)
        except IOError:
            nmc_province_data = ''

        if nmc_province_data:
            result = {}
            for province in nmc_province_data:
                province_url = 'http://www.nmc.cn/f/rest/province/'+province['code']
                province_data = self.weather_request(province_url)
                if province_data:
                    for city in province_data:
                        result.setdefault(city['province']+city['city'],city['code'])
            with open(self.city_province_file, 'w') as out_file:
                json.dump(result, out_file)

        return True

    def weather_request(self,url):
        try:
            r = requests.get(url, timeout=10)
            r.encoding = 'utf-8'
            html = json.loads(r.text)
        except Exception, e:
            html=''
        return html

    def has_cityinfo_by_cityname(self,cityname):
        try:
            with open(self.city_province_file, 'r') as in_file:
                nmc_city_data = json.load(in_file)
        except IOError:
            nmc_city_data = ''

        PATTERN = ur'([\u4e00-\u9fa5]{1,10}?(?:天气)){0,2}$'

        data_utf8 = cityname.decode('utf8')

        pattern = re.compile(PATTERN)

        m = pattern.search(data_utf8)

        if m.lastindex == 1:
            city = m.group(1).replace('天气','')
            if city == '':
                return 'not_weather'
        else:
            return 'not_weather'

        result = {}

        if self.cityname_alias.has_key(cityname.replace('天气','').encode('utf8')):
            city = self.cityname_alias[cityname.replace('天气','').encode('utf8')].decode('utf8')

        if nmc_city_data.has_key(city):
            return nmc_city_data[city]
        else:
            return 'not_match'

    def get_weather_by_cityname(self,citycode,city):

        result = {}

        city = city.replace('天气','')

        if citycode == 'not_match':
            return '没有查到'+city+'天气信息'
        elif citycode == 'not_weather':
            return ''
        else:
            city_url = 'http://www.nmc.cn/f/rest/weather/'+citycode
            city_data = self.weather_request(city_url)
            if city_data[0]:
                html = city_data[0]
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

                # text= '【'+city+'】今天{today_weather},最高温度{today_temp_hig}℃,最低温度{today_temp_low}℃. 明天{tomorrow_weather},最高温度{tomorrow_temp_hig}℃,最低温度{tomorrow_temp_low}℃'.format(**result)

                if(result['today_weather'] == '9999'):
                    text='【'+city+'】当前气温{current_temp}℃. 明天{tomorrow_weather},最高温度{tomorrow_temp_hig}℃,最低温度{tomorrow_temp_low}℃'.format(**result)
                else:
                    text='【'+city+'】今天{today_weather},最高温度{today_temp_hig}℃,最低温度{today_temp_low}℃. 明天{tomorrow_weather},最高温度{tomorrow_temp_hig}℃,最低温度{tomorrow_temp_low}℃'.format(**result)

                return text

# nmcObj = nmcWeather()

# code = nmcObj.has_cityinfo_by_cityname('青浦天气')
# print(nmcObj.get_weather_by_cityname(code,'青浦天气'))
#normalParsing
