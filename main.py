import cv2

FRAME_SIZE = (600, 400)


video_capture = cv2.VideoCapture("samples/qr_test.mp4")

ret, frame = video_capture.read()

while ret:
	ret, frame = video_capture.read()
	if ret:
		cv2.imshow("Camera Feed", cv2.resize(frame, FRAME_SIZE))
	else:
		print "Video terminado"
	cv2.waitKey(30)