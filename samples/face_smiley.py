#!/usr/bin/env python2
 
"""
OpenCV example. Show webcam image and detect face.

Small edit. Show smiley on detected face
"""
 
import cv2
 
TRAINSET = "data/lbpcascade_frontalface.xml"
DOWNSCALE = 4
smiley = cv2.imread("data/smiley.png", -1)
 
webcam = cv2.VideoCapture(0)
cv2.namedWindow("preview")
classifier = cv2.CascadeClassifier(TRAINSET)
 
 
if webcam.isOpened(): # try to get the first frame
    rval, frame = webcam.read()
else:
    rval = False
 
while rval:
  # detect faces and draw bounding boxes
  minisize = (frame.shape[1]/DOWNSCALE,frame.shape[0]/DOWNSCALE)
  miniframe = cv2.resize(frame, minisize)
  faces = classifier.detectMultiScale(miniframe)
  for f in faces:
    x, y, w, h = [ v*DOWNSCALE for v in f ]
    smiley = cv2.resize(smiley, (w, h))
    # add alpha channel to frame and "overlay" smiley in detected position
    for c in range(0, 3):
      frame[y: y+smiley.shape[0], \
            x: x+smiley.shape[1], \
            c] = smiley[:,:,c] * (smiley[:,:,3]/255.0) + \
                 frame[y:y+smiley.shape[0], x:x+smiley.shape[1], c] * \
                 (1.0 - smiley[:,:,3]/255.0)

  cv2.putText(frame, "Press ESC to close.", (5, 25),
              cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255))
  cv2.imshow("preview", frame)

  # get next frame
  rval, frame = webcam.read()
  key = cv2.waitKey(20)
  if key in [27, ord('Q'), ord('q')]: # exit on ESC
    break
