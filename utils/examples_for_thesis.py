#!/usr/bin/python
# -*- coding: utf-8
import cv2
import os
import math
import sys

# Para importar librerias custom
root = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.append(os.path.join(root, "lib"))

import qr
import three
import MeshViewer

img_filename = sys.argv[1]
img = cv2.imread(img_filename)

def resize(image, size = (600, 400)):
  image = cv2.resize(image, size)
  return image

def grayscale(image, save = "grayscale.png"):
  gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  cv2.imwrite(save, gray_frame)
  return gray_frame

def binarizar(image, save = "bw.png"):
  (thresh, bw_frame) = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
  cv2.imwrite(save, bw_frame)
  return bw_frame

def mark_qr(image, save = "qr.png"):
  data = qr.scan(image)
  if data:
    v1, v2, v3, v4 = three.Vector2(data.location[0]), three.Vector2(data.location[1]), three.Vector2(data.location[2]), three.Vector2(data.location[3])
    bb = three.Box2()
    bb.setFromVectors([v1, v2, v3, v4])
    cv2.rectangle(img, (bb.min.x, bb.min.y), (bb.max.x, bb.max.y), (0, 0, 255))
    cv2.putText(img, "Data:"+str(data.data), (bb.center.x, bb.center.y), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255))
    cv2.imwrite(save, img)
  else:
    print "QR not found"
  return image

def blur(image, save = "blur.png"):
  gaussian_blur = cv2.GaussianBlur(image, (29, 29),0)
  cv2.imwrite(save, gaussian_blur)
  return gaussian_blur
    
def main():
  if os.path.isfile(img_filename):
    gray = grayscale(img)
    blur(gray)
    #bw = binarizar(gray)
    #mark_qr(bw)
  
if __name__ == "__main__":
  main()
