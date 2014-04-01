#!/usr/bin/python

# Librerias usadas
import cv2
import qr
import three
import pygame
import os
import MeshViewer

# Utils
SAMPLES_DIR = os.path.join("samples", "models")
VIDEO_DIR = os.path.join("samples", "videos")
models = {
  "1": os.path.join(SAMPLES_DIR, "1.obj"),
  "2": os.path.join(SAMPLES_DIR, "2.obj"),
  "3": os.path.join(SAMPLES_DIR, "3.obj"),
  "4": os.path.join(SAMPLES_DIR, "4.obj"),
  "5": os.path.join(SAMPLES_DIR, "5.obj"),
  "6": os.path.join(SAMPLES_DIR, "6.obj")
}
found_markers = {}

# OpenCV
FRAME_SIZE = (400, 300)
DEBUG_CV = False

# Pygame
fps = 60
dt = 1.0/fps
black = (0, 0, 0)

# Main Loop
def main():
  # Pygame
  pygame.init()
  pygame.display.set_caption("Main")
  clock = pygame.time.Clock()
  screen = pygame.display.set_mode(FRAME_SIZE)
  env3d = MeshViewer.Env3D(screen, [FRAME_SIZE[0], FRAME_SIZE[1]])
  # OpenCV
  video_capture = cv2.VideoCapture(os.path.join(VIDEO_DIR, "test_qr.mp4"))
  ret = True
  while ret:
    # OpenCV
    ret, frame = video_capture.read()
    # Se encontro un frame en el video
    if ret:
      objects = []
      frame = cv2.resize(frame, FRAME_SIZE)
      gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      (thresh, bw_frame) = cv2.threshold(gray_frame, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
      data_list = qr.scanAll(bw_frame)
      # QR's encontrados
      if data_list:
        # Recorrer cada uno y marcarlo
        for data in data_list:
          v1, v2, v3, v4 = three.Vector2(data.location[0]), three.Vector2(data.location[1]), three.Vector2(data.location[2]), three.Vector2(data.location[3])
          bb = three.Box2()
          bb.setFromVectors([v1, v2, v3, v4])
          cv2.rectangle(frame, (bb.min.x, bb.min.y), (bb.max.x, bb.max.y), (255, 0, 0))
          #cv2.putText(frame, data.data, (bb.center.x, bb.center.y), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
          try:
            if data.data in found_markers:
              object = found_markers[data.data]
            else:
              object = MeshViewer.Object(models[str(data.data)])
              found_markers[str(data.data)] = object
            mesh_center = object.getCenter()
            # Normalizar, se dibuja desde el centro
            center = three.Vector2((mesh_center.x + FRAME_SIZE[0]/2.0, mesh_center.y + FRAME_SIZE[1]/2.0))
            offset = bb.center.sub(center)
            object.translate(MeshViewer.Point3D(offset.x, offset.y, 0))
          except Exception as e:
            print "No model found for marker: " + data.data
      # Pygame
      pygame_image = pygame.image.frombuffer(frame.tostring(), frame.shape[1::-1], "RGB")
      screen.blit(pygame_image, (0, 0))
      if len(found_markers) > 0:
        for key in found_markers:
          found_markers[key].display(env3d)
      pygame.display.update()
      clock.tick(fps)
    # No mas frames
    else:
      print "Video terminado"
      sys.exit()

if __name__ == "__main__":
  main()