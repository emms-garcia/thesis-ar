#!/usr/bin/python

# Librerias usadas
import cv2
import qr
import numpy as np
import three
import pygame

# OpenCV
FRAME_SIZE = (400, 300)
DEBUG_CV = False
PYGAME_INPUT = "input.png"
video_capture = cv2.VideoCapture("samples/test_qr.mp4")

# Pygame
pygame.init()
pygame.display.set_caption("Main")
screen = pygame.display.set_mode(FRAME_SIZE)
fps = 60
dt = 1.0/fps
clock = pygame.time.Clock()
black = (0, 0, 0)

# Main Loop
ret = True
while ret:
  # OpenCV
  ret, frame = video_capture.read()
  if ret:
    frame = cv2.resize(frame, FRAME_SIZE)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    (thresh, bw_frame) = cv2.threshold(gray_frame, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    data = qr.scan(bw_frame)
    if data:
      v1, v2, v3, v4 = three.Vector2(data.location[0]), three.Vector2(data.location[1]), three.Vector2(data.location[2]), three.Vector2(data.location[3])
      bb = three.Box2()
      bb.setFromVectors([v1, v2, v3, v4])
      if DEBUG_CV: cv2.rectangle(frame, (bb.min.x, bb.min.y), (bb.max.x, bb.max.y), (255, 0, 0))
      if DEBUG_CV: cv2.putText(frame, data.data, (bb.center.x, bb.center.y), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
    if DEBUG_CV: cv2.imshow("Camera Feed", frame)
  else:
    print "Video terminado"
  if DEBUG_CV: cv2.waitKey(30) 
  # Pygame
  image = pygame.image.frombuffer(frame.tostring(), frame.shape[1::-1], "RGB")
  #screen.fill(black)
  screen.blit(image, (0, 0))
  pygame.display.update()
  clock.tick(fps)