#!/usr/bin/python
import cv2
import qr
import numpy as np
import three


FRAME_SIZE = (600, 400)
NFRAMES_CALIBRATION = 10
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)

objectpoints = []
imagepoints = []

objPoints = np.zeros((6*7, 3), np.float32)
objPoints[:,:2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)

video_capture = cv2.VideoCapture("samples/qr_test.mp4")
ret, frame = video_capture.read()
calibration_frames = [video_capture.read()[1] for i in range(NFRAMES_CALIBRATION)]





ret = True
while ret:
	ret, frame = video_capture.read()
	if ret:
		frame = cv2.resize(frame, FRAME_SIZE)
		gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		(thresh, bw_frame) = cv2.threshold(gray_frame, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
		data = qr.scan(bw_frame)
		if data:
			cv2.rectangle(frame, data.location[0], data.location[2], (255, 0, 0))
			v1, v2, v3, v4 = three.Vector2(data.location[0]), three.Vector2(data.location[1]), \
							 three.Vector2(data.location[2]), three.Vector2(data.location[3])
			bb = three.Box2((v1, v2))

			cv2.putText(frame, data.data, (bb.center.x, bb.center.y), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
		cv2.imshow("Camera Feed", frame)
	else:
		print "Video terminado"
	cv2.waitKey(30)