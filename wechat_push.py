#!/usr/bin/env python
# coding: utf-8
#https://github.com/PP8818/Python-Projects
#https://segmentfault.com/a/1190000009420701
#kill -s `ps -ef | grep "wechat_push.py"|awk '{print $2}'`
# ps aux|grep -v grep|grep "wechat_push.py"
import sys
import wxRot
import datetime as dt

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    robot = wxRot.wxRot()
    robot.auto_login()
    robot.scheduler()
    robot.run()
