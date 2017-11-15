#!/usr/bin/env python
# coding: utf-8

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os
import json
import sys
import datetime
import time

reload(sys)
sys.setdefaultencoding('utf-8')

def SendEmail(fromAdd, toAdd, subject, attachfile, htmlText):
  strFrom = fromAdd;
  strTo = toAdd;
  msg =MIMEText(htmlText);
  msg['Content-Type'] = 'Text/HTML';
  msg['Subject'] = Header(subject,'gb2312');
  msg['To'] = strTo;
  msg['From'] = strFrom;
  
  smtp = smtplib.SMTP('smtp.qq.com');

  try:
    smtp.sendmail(strFrom,strTo,msg.as_string());
  finally:
    smtp.close;

def getInfo(toAdd):
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

  if(toAdd == '530369682@qq.com'):
    text='当前室内温度{temp}℃，室内湿度{humidity}%.明天{tomorrow_weather},最高温度{tomorrow_temp_hig}℃,最低温度{tomorrow_temp_low}℃'.format(**data)
  else:  
    text='明天{tomorrow_weather},最高温度{tomorrow_temp_hig}℃,最低温度{tomorrow_temp_low}℃'.format(**data)

  return text

if __name__ == "__main__":

  arr = {}
  time_now = datetime.datetime.now()
  date_string = time_now.strftime('%Y年%m月%d日')

  for i in arr:
    text = getInfo(arr[i]);
    SendEmail();
    time.sleep(5)
