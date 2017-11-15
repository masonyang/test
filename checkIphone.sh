#!/bin/sh

#我的iPhone进入wifi后自动启动

IPHONE_MAC="64:b0:a6:db:3e:5b"
ADDRESS="192.168.1.0/24"


#判断手机是否在线,不在线返回空""
check_device()
{
  result=$(uname -a |grep "Darwin"|wc -l)

  nmap -sP $1 >/dev/null

  if [ $result -eq 1 ]; then
    return $(/usr/sbin/arp -a|grep $2|wc -l)
  else
    return $(grep $2 /proc/net/arp|wc -l)
  fi
}

is_online()
{
  return $(grep "1" /tmp/checkiphone.log|wc -l)
}

play()
{
  is_online
  result=$?

  if [ $result -eq 1 ];then
    echo "已在线"
  else
    echo "欢迎登录"
    writelog "1"
    
    mplayer "http://tts.baidu.com/text2audio?idx=1&tex=终于到家了&cuid=baidu_speech_demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=4&vol=5&pit=5"
    sleep 2
    /usr/bin/python /home/pi/masonInPython/epaper_clock/voice.py
    /usr/bin/python /home/pi/masonInPython/epaper_clock/weather_fetcher.py
  fi

}

writelog()
{
  echo $1 > /tmp/checkiphone.log
}

stop()
{
  writelog "0"
}

check_device $ADDRESS $IPHONE_MAC
result=$?

if [ $result -eq 1 ]; then
  play
else
  echo "bye"
  stop
fi
