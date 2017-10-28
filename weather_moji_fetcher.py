#!/usr/bin/env python
# coding: utf-8

import re
import requests
import os
import sys
import time
from datetime import datetime
from bs4 import BeautifulSoup

reload(sys)  
sys.setdefaultencoding('utf8')

output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weather.json')

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit'
                      '/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safar'
                      'i/537.36',
    }

result = {field: None for field in '''city_name current_temp current_weather
          current_wind current_humidity current_aq
          today_weather today_temp_low today_temp_hig tomorrow_weather
          tomorrow_temp_low tomorrow_temp_hig tomorrow_wind
          '''.split()}


def get_weather():
    # 下载墨迹天气主页源码
    res = requests.get('http://tianqi.moji.com/weather/china/shanghai/shanghai', headers=headers)
    # 用BeautifulSoup获取所需信息
    soup = BeautifulSoup(res.text, "html.parser")

    city_name = soup.find('div', attrs={'class': 'search_default'}).em.getText()

    result['city_name'] = city_name.replace('， ','-')

    current_temp = soup.find('div', attrs={'class': 'wea_weather clearfix'}).em.getText()
    
    result['current_temp'] = current_temp

    current_weather = soup.find('div', attrs={'class': 'wea_weather clearfix'}).b.getText()

    result['current_weather'] = current_weather

    current_humidity = soup.find('div', attrs={'class': 'wea_about clearfix'}).span.getText()

    current_humidity.replace('湿度 ','').replace('%', '')

    result['current_humidity'] = current_humidity

    current_wind = soup.find('div', attrs={'class': 'wea_about clearfix'}).em.getText()

    result['current_wind'] = current_wind

    aqi = soup.find('div', attrs={'class': 'wea_alert clearfix'}).em.getText()
    current_aq = re.search(r'\d+', aqi).group()

    result['current_aq'] = current_aq

    info = soup.find('div', attrs={'class': 'wea_tips clearfix'}).em.getText()

    # 获取今天的日期
    today = datetime.now().date().strftime('%Y年%m月%d日')

    ul = soup.find('ul', attrs={'class': 'days clearfix'}).li.li.getText()


    print ul
    pass

	# result['update'] = int(time.time())
	# with open(output_file, 'w') as out_file:
	#     json.dump(result, out_file)
    

print get_weather()