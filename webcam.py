#!/usr/bin/env python
# coding: utf-8

import face_recognition
import cv2
import sys

# reload(sys)
# sys.setdefaultencoding('utf-8')

video_capture = cv2.VideoCapture(0)

while True:
	ret, frame = video_capture.read()

	# Find all the faces and face enqcodings in the frame of video
	face_locations = face_recognition.face_locations(frame)
	face_encodings = face_recognition.face_encodings(frame, face_locations)

	# Loop through each face in this frame of video
	for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
		name = 'test'
		font = cv2.FONT_HERSHEY_DUPLEX

		# Draw a box around the face
		cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

		# Draw a label with a name below the face
		cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
		cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
		cv2.imshow('Video', frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

video_capture.release()
cv2.destroyAllWindows()