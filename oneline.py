#!/usr/bin/env python
# coding: utf-8

import os
import sys
import random

reload(sys)
sys.setdefaultencoding('utf-8')

print(''.join(random.choice('/\\') for i in range(50*24)))

# print(' '.join([''.join([('LoveYou'[(x-y)%7]if((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3<=0 else' ')for x in range(-30,30)])for y in range(15,-15,-1)]))

# print (' '.join([' '.join(['%s*%s=%-2s' % (y,x,x*y) for y in range(1,x+1)]) for x in range(1,10)]))