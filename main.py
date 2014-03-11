import cv2
import qr

FRAME_SIZE = (600, 400)


video_capture = cv2.VideoCapture("samples/qr_test.mp4")

ret, frame = video_capture.read()


def get_bounding_box():
	return



while ret:
	ret, frame = video_capture.read()
	if ret:
		frame = cv2.resize(frame, FRAME_SIZE)
		gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		(thresh, bw_frame) = cv2.threshold(gray_frame, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
		data = qr.scan(bw_frame)
		if data:
			cv2.rectangle(frame, data.location[0], data.location[2], (255, 0, 0))
		cv2.imshow("Camera Feed", frame)
	else:
		print "Video terminado"
	cv2.waitKey(30)