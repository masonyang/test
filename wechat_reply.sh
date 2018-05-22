#!/bin/sh

python_dir="/usr/bin/python"

run_dir="/Users/yangminsheng/masonInPython/epaper_clock"

function wechat_push(){
	# `$python_dir "$run_dir/weather_sina_shanghai.py"`

	# `$python_dir "$run_dir/weather_sina_wuhan.py"`

	`$python_dir "$run_dir/weather_moji_shanghai.py"`

	`$python_dir "$run_dir/weather_moji_wuhan.py"`

	`$python_dir "$run_dir/wechat_push.py"`
}

function checkprocess(){
    return $(ps aux|grep -v grep|grep "$1"|wc -l)
}

function checkInternet(){
	return $(ping -c 3 "www.baidu.com"|awk 'NR==7 {print $4}')
}

checkprocess "wechat_push.py"

result=$?

if [ $result -ge 1 ]; then
	checkInternet
	res=$?
	if [ $res -eq 0 ]; then
		kill -s `ps aux|grep -v grep|grep 'wechat_push.py'|awk '{print $2}'`
	fi
	echo "active"
else
	# checkInternet
	# res=$?
	# if [ $res -eq 0 ]; then
	# 	echo 'no internet'
	# else
	wechat_push
	# fi
fi