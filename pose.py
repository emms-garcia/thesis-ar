#!C:\Python27\python.exe
# -*- coding: utf-8 -*- 
import numpy as np
import cv2
import glob
import os

IMAGE_PATH = os.path.join(os.getcwd(), "samples")

class Camera:
 
  def __init__(self):
    self.matrix = None
    self.objPoints = np.zeros((6*7, 3), np.float32)
    self.objPoints[:,:2] = np.mgrid[0:7, 0:6].T.reshape(-1, 2)
    self.distCoeffs = None
    self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    self.objectpoints = []
    self.imagepoints = []
    self.calibratedMatrix = None
    
  def calibrateWithImages(self, images):
    for fname in images:
      img = cv2.imread(fname)
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)
      if ret:
        self.objectpoints.append(self.objPoints)
        cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)
        self.imagepoints.append(corners)
    ret, self.matrix, self.distCoeffs, _, _ = cv2.calibrateCamera(self.objectpoints, self.imagepoints, gray.shape[::-1], None, None)
    h, w = img.shape[:2]
    self.calibratedMatrix, roi = cv2.getOptimalNewCameraMatrix(self.matrix, self.distCoeffs, (w, h), 1, (w, h))
    return self.matrix
  
  def calibrateWithCamera(self, camera):
    return

def draw(img, corners, imgpts):
  corner = tuple(corners[0].ravel())
  cv2.line(img, corner, tuple(imgpts[0].ravel()), (0,255,0), 5)
  cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,0,255), 5)
  cv2.line(img, corner, tuple(imgpts[2].ravel()), (255,0,0), 5)
  return img

images = glob.glob(os.path.join(IMAGE_PATH, '*.jpg'))
camera = Camera()
camera.calibrateWithImages(images)
axis = np.float32([[3, 0, 0], [0, 3, 0], [0, 0, -3]]).reshape(-1, 3)

for fname in images:
  img = cv2.imread(fname)
  h,  w = img.shape[:2]
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  img = cv2.undistort(img, camera.matrix, camera.distCoeffs, None, camera.calibratedMatrix)
  cv2.imwrite(fname[:6]+ '_undistorted.png', img)
  ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)
  if ret:
    cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), camera.criteria)
    rvecs, tvecs, inliers = cv2.solvePnPRansac(camera.objPoints, corners, camera.calibratedMatrix, camera.distCoeffs)
    imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, camera.calibratedMatrix, camera.distCoeffs)
    img = draw(img, corners, imgpts)
    cv2.imwrite(fname[:6]+ '.png', img)

cv2.destroyAllWindows()