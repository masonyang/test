#!/usr/bin/env python
# coding: utf-8

import urllib
import urllib2
import os
import sys
import datetime
import json

reload(sys)
sys.setdefaultencoding('utf-8')

def post(url, data): 
  req = urllib2.Request(url) 
  data = urllib.urlencode(data) 
  #enable cookie 
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor()) 
  response = opener.open(req, data) 

  result = response.read()

  return result

def getRili():

  time_now = datetime.datetime.now()
  date_string = time_now.strftime('%Y年%m月')

  data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rili.json')
  wdata = {}

  with open(data_file, 'r') as in_file:
      wdata = json.load(in_file)

  if(wdata['data'][0]['key'] == date_string):
    return True

  posturl = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php" 
  data = {'query':date_string, 'resource_id':'6018','ie':'utf8','oe':'utf8','format':'json','tn':'baidu'} 
  result = post(posturl, data)


  _file = file(data_file, 'w')
  _file.write(result)
  _file.close()
  pass

if __name__ == '__main__': 
  getRili()
