#!/bin/sh

function checkInternet(){
	return $(ping -c 3 "www.baidu.com"|awk 'NR==7 {print $4}')
}

checkInternet
res=$?

echo $res