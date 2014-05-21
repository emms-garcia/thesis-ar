#!/usr/bin/python
# -*- coding: utf-8
# Librerias usadas
import cv2
import lib.qr as qr
import lib.three as three
import lib.MeshViewer as MeshViewer
import pygame
import os
import math
import sys
import time

INPUT_VIDEO_FILE = sys.argv[1]

# Utils
MODELS_DIR = os.path.join("samples", "models")
VIDEO_DIR = os.path.join("samples", "videos")
EXPERIMENTS_DIR = os.path.join("experiments")
TTEST = "0"
NSAMPLES = 30
TDATA = {
  "ALL" : {
    "filename" : "all.dat",
  },
  "IPROCESS" : {
    "filename" : "image_processing.dat",
  },
  "QR_DETECT" : {
    "filename" : "qr_detect.dat",
  },
  "3D_OVERLAP" : {
    "filename" : "3d_overlap.dat"
  }
}
# Check if video file exists
if not os.path.isfile(os.path.join(VIDEO_DIR, INPUT_VIDEO_FILE)) and not os.path.isfile(INPUT_VIDEO_FILE):
  print "File %s not found in samples or in specified directory"%INPUT_VIDEO_FILE
  print "Run instructions:"
  print "python %s videopath timetest"%sys.argv[0]
  print "-videopath: Path to video file."
  print "-timetest: 0 to ignore, 1 to take samples for overall frame loop, 2 to take samples for every individual processing step. 0 by default."
  sys.exit()

#Check if measuring of time samples was defined
if len(sys.argv) > 2: TTEST = sys.argv[2]
if TTEST == "1":
  TDATA["ALL"]["file"] = open(os.path.join(EXPERIMENTS_DIR, TDATA["ALL"]["filename"]), "w")
elif TTEST == "2":
  for test in TDATA:
    TDATA[test]["file"] = open(os.path.join(EXPERIMENTS_DIR, TDATA[test]["filename"]), "w")
    
INPUT_VIDEO_FILE = INPUT_VIDEO_FILE if os.path.isfile(INPUT_VIDEO_FILE) else os.path.join(VIDEO_DIR, INPUT_VIDEO_FILE)

models = {
  "1": os.path.join(MODELS_DIR, "cube.obj"),
  "2": os.path.join(MODELS_DIR, "cube.obj"),
  "3": os.path.join(MODELS_DIR, "cube.obj"),
  "4": os.path.join(MODELS_DIR, "cube.obj"),
  "5": os.path.join(MODELS_DIR, "cube.obj"),
  "6": os.path.join(MODELS_DIR, "cube.obj"),
  "7": os.path.join(MODELS_DIR, "cube.obj"),
  "8": os.path.join(MODELS_DIR, "cube.obj"),
}
found_markers = {}

# OpenCV
FRAME_SIZE = (500, 400)
DEBUG_CV = False

# False
fps = 60
dt = 1.0/fps
black = (0, 0, 0)
white = (255, 255, 255)

# Main Loop
def main():
  # Pygame
  pygame.init()
  pygame.display.set_caption("Main")
  clock = pygame.time.Clock()
  screen = pygame.display.set_mode(FRAME_SIZE)
  env3d = MeshViewer.Env3D(screen, [FRAME_SIZE[0], FRAME_SIZE[1]])
  # OpenCV
  video_capture = cv2.VideoCapture(INPUT_VIDEO_FILE)
  N_FRAMES = int(video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
  CUR_FRAME = 0
  ret, frame = video_capture.read()
  while ret:
    T_INITIAL = time.time()
    # OpenCV
    # Arreglar inversion de color
    T_INITIAL_IPROCESS = time.time()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    CUR_FRAME += 1
    # Se encontro un frame en el video
    # OpenCV
    frame = cv2.resize(frame, FRAME_SIZE)
    bw_frame = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    if TTEST == "2": TDATA["IPROCESS"]["file"].write("%s %s\n"%(str(CUR_FRAME), str(time.time() - T_INITIAL_IPROCESS)))
    T_INITIAL_QR_DETECT = time.time()
    data_list = qr.scanAll(bw_frame)
    if TTEST == "2": TDATA["QR_DETECT"]["file"].write("%s %s\n"%(str(CUR_FRAME), str(time.time() - T_INITIAL_QR_DETECT)))
    
    T_INITIAL_3DOVERLAP = time.time()
    displayed_objects = []
    # QR's encontrados
    if data_list:
      # Recorrer cada uno y marcarlo
      for data in data_list:
        v1, v2, v3, v4 = three.Vector2(data.location[0]), three.Vector2(data.location[1]), three.Vector2(data.location[2]), three.Vector2(data.location[3])
        bb = three.Box2()
        bb.setFromVectors([v1, v2, v3, v4])
        cv2.rectangle(frame, (bb.min.x, bb.min.y), (bb.max.x, bb.max.y), (255, 0, 0), 5)
        try:
          new = False
          if data.data in found_markers:
            object = found_markers[data.data]
          else:
            object = MeshViewer.Object(models[str(data.data)])
            found_markers[str(data.data)] = object
            new = True
          displayed_objects.append(object)
          mesh_center = object.getCenter()
          # Normalizar, se dibuja desde el centro
          center = three.Vector2((mesh_center.x + FRAME_SIZE[0]/2.0, mesh_center.y + FRAME_SIZE[1]/2.0))
          offset = bb.center.sub(center)
          object.translate(MeshViewer.Point3D(offset.x + 50/2, offset.y + 50/2, 0))
          object.rotateX(math.pi/5)
          object.rotateY(math.pi/5)
          new = False
        except Exception as e:
          pass#print "No model found for marker: " + data.data
    
    if TTEST == "2": TDATA["3D_OVERLAP"]["file"].write("%s %s\n"%(str(CUR_FRAME), str(time.time() - T_INITIAL_3DOVERLAP)))
    # Pygame
    pygame_image = pygame.image.frombuffer(frame.tostring(), frame.shape[1::-1], "RGB")
    screen.blit(pygame_image, (0, 0)) 
    #screen.fill(white)
    for object in displayed_objects:
      object.display(env3d)
    pygame.display.update()
    clock.tick(fps)
    if TTEST == "2" or TTEST == "1": TDATA["ALL"]["file"].write("%s %s\n"%(str(CUR_FRAME), str(time.time() - T_INITIAL)))
    ret, frame = video_capture.read()
    # No mas frames

if __name__ == "__main__":
  main()