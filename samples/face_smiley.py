#!/usr/bin/env python2
 
"""
OpenCV example. Show webcam image and detect face.

Small edit. Show smiley on detected face
"""
 
import cv2
import math
import cv
import numpy as np 

TRAINSET = "data/lbpcascade_frontalface.xml"
DOWNSCALE = 4
smiley = cv2.imread("data/smiley.png", -1)
dist_umb = 100
webcam = cv2.VideoCapture(0)
cv2.namedWindow("preview")
classifier = cv2.CascadeClassifier(TRAINSET)
 
 
if webcam.isOpened(): # try to get the first frame
    rval, frame = webcam.read()
else:
    rval = False
lines = []
while rval:
  rval, frame = webcam.read()
  cv2.flip(frame,1,frame)

  # get next frame
  gray = cv2.cvtColor(frame, cv.CV_RGB2GRAY)
  blur = cv2.GaussianBlur(gray, (0,0), 2)
  result =  cv2.HoughCircles(blur, cv2.cv.CV_HOUGH_GRADIENT, 2, 10, np.array([]), 40, 80, 5, 100)
  if result is not None:
   #Ignorar repetidos
    for c1 in result[0]:
      cv2.circle(frame, (c1[0],c1[1]), c1[2], (0,255,0),2)
      for c2 in result[0]:
        if math.sqrt(math.pow(c2[1] - c1[1], 2) + math.pow(c2[0] - c1[0], 2)) > dist_umb:
          lines.append([c1[0],c1[1],c2[0],c2[1]])

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

  for line in lines:
    cv2.line(frame, (line[0],line[1]), (line[2],line[3]), (0,0,255), 3)

  cv2.imwrite("%s.png"%len(lines),frame)
  cv2.putText(frame, "Press ESC to close.", (5, 25),
            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255))
  cv2.imshow("preview", frame)
  key = cv2.waitKey(20)
  if key in [27, ord('Q'), ord('q')]: # exit on ESC
    break
