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
  smtp.login('530369682@qq.com','njksqixizpdycajf');
  try:
    smtp.sendmail(strFrom,strTo,msg.as_string());
  finally:
    smtp.close;

if __name__ == "__main__":

  arr = {'mason':'530369682@qq.com','mason1':'530369682@qq.com','mason2':'530369682@qq.com'}

  for i in arr:
    SendEmail("530369682@qq.com",arr[i],"aaa","hello",'来自Mason');
    time.sleep(5)
