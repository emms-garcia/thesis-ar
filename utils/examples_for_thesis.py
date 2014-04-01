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
  
def main():
  if os.path.isfile(img_filename):
    img = cv2.imread(img_filename)
    gray = grayscale(img)
    binarizar(gray)
    
if __name__ == "__main__":
  main()
