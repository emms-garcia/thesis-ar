#!/usr/bin/python

# Librerias usadas
import cv2
import qr
import numpy as np
import three
import pygame
import os
import MeshViewer
import random

random.seed()

class Env3D:
  def __init__(self, screen, winsize):
    self.winsize= winsize
    self.zoom_factor = 1
    self.light_vector_1 = MeshViewer.Point3D (random.random(),random.random(),random.random())
    self.light_vector_1.normalize()
    self.light_vector_2 = MeshViewer.Point3D (random.random(),random.random(),random.random())
    self.light_vector_2.normalize()
    self.screen = screen
    self.wincenter = [winsize[0]/2, winsize[1]/2]
    self.colorize = True

# Utils
SAMPLES_DIR = os.path.join("samples", "models")
VIDEO_DIR = os.path.join("samples", "videos")
models = {
  "1": os.path.join(SAMPLES_DIR, "1.obj"),
  "2": os.path.join(SAMPLES_DIR, "2.obj")
}

# OpenCV
FRAME_SIZE = (400, 300)
DEBUG_CV = False
video_capture = cv2.VideoCapture(os.path.join(VIDEO_DIR, "test_qr.mp4"))

# Pygame
pygame.init()
pygame.display.set_caption("Main")
screen = pygame.display.set_mode(FRAME_SIZE)
fps = 60
dt = 1.0/fps
clock = pygame.time.Clock()
black = (0, 0, 0)
env3d = Env3D(screen, [FRAME_SIZE[0], FRAME_SIZE[1]])
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
      cv2.rectangle(frame, (bb.min.x, bb.min.y), (bb.max.x, bb.max.y), (255, 0, 0))
      #cv2.putText(frame, data.data, (bb.center.x, bb.center.y), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
      try:
        object = MeshViewer.Object(models[str(data.data)])
        mesh_center = object.getCenter()
        # Normalizar, se dibuja desde el centro
        center = three.Vector2((mesh_center.x + FRAME_SIZE[0]/2.0, mesh_center.y + FRAME_SIZE[1]/2.0))
        offset = bb.center.sub(center)
        object.translate(MeshViewer.Point3D(offset.x, offset.y, 0))
        #print object.getCenter()
        #print object.getCenter()
      except Exception as e:
        print e
        object = None
        print "No model found for marker: "+data.data
    else:
      object = None
    if DEBUG_CV: cv2.imshow("Camera Feed", frame)
  else:
    print "Video terminado"
  if DEBUG_CV: cv2.waitKey(30) 
  # Pygame
  pygame_image = pygame.image.frombuffer(frame.tostring(), frame.shape[1::-1], "RGB")
  screen.blit(pygame_image, (0, 0))
  if object: object.display(env3d)
  pygame.display.update()
  clock.tick(fps)