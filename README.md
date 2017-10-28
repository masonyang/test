### 所用的硬件
* 树莓派3
* 微雪4.3寸串口电子墨水屏
* DHT22温湿度传感模块

#### 硬件连接
屏幕  | 树莓派
------------- | -------------
DIN  | TX(GPIO14)
DOUT  | RX(GPIO15)
GND  | GND
VCC  | 3V

DHT22|树莓派
------------- | -------------
DOUT  | 1-Wire(BCM4)
GND  | GND
VCC  | 3V
DHT22 DOUT引脚也可以接到其他gpio脚上，不过要相应的修改home_air_sensor.py中read_retry第二个参数

```bash
sudo apt-get update
sudo apt-get upgrade
```
编辑 /boot/config.txt 添加一行
```
dtoverlay=pi3-miniuart-bt
```

```
运行脚本

sudo ./home_air_sensor.py  室内温度湿度检测
./weather_fetcher.py  		最近两天天气获取
./linux_temp.py  			pi的cpu+gpu温度检测
./voice_weather.py   语音播报
./qqmail.py 	发送邮件
node ./blessed_new/test/widget-temp.js   显示天气公告
```


