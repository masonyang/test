#!/usr/bin/env python
# coding: utf-8

import cv2
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

video_capture = cv2.VideoCapture(0)

while True:
	ret, frame = video_capture.read()

	top = 10
	right = 10
	bottom = 10
	left = 10
	name = 'test'
	font = cv2.FONT_HERSHEY_DUPLEX
	cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
	cv2.imshow('Video', frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

video_capture.release()
cv2.destroyAllWindows()