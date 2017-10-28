#!/usr/bin/env python
# coding: utf-8

import commands
import json
import os
import time

defget_cpu_temp():
    tempFile=open("/sys/class/thermal/thermal_zone0/temp")
    cpu_temp=tempFile.read()
    tempFile.close()
    return float(cpu_temp)/1000
    # Uncomment the next line if you want the temp in Fahrenheit
    #return float(1.8*cpu_temp)+32
 
defget_gpu_temp():
    gpu_temp=commands.getoutput('/opt/vc/bin/vcgencmd measure_temp').replace('temp=','').replace('\'C','')
    return float(gpu_temp)
    # Uncomment the next line if you want the temp in Fahrenheit
    # return float(1.8* gpu_temp)+32
 
result = {'cpu_temp': defget_cpu_temp(), 'gpu_temp': defget_gpu_temp(), 'update': int(time.time())}
data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'linux_temp.json')
with open(data_file, 'w') as out_file:
    json.dump(result, out_file)
