import numpy as np
import cv2
import glob

def draw(img, corners, imgpts):
  corner = tuple(corners[0].ravel())
  cv2.line(img, corner, tuple(imgpts[0].ravel()), (0,255,0), 5)
  cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,0,255), 5)
  cv2.line(img, corner, tuple(imgpts[2].ravel()), (255,0,0), 5)
  return img

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('*.jpg')

for fname in images:
  img = cv2.imread(fname)
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  ret, corners = cv2.findChessboardCorners(gray, (7,6),None)
  if ret == True:
    objpoints.append(objp)
    corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
    imgpoints.append(corners)
    
ret, mtx, dist, _, _ = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)

for fname in glob.glob('left*.jpg'):
  img = cv2.imread(fname)
  h,  w = img.shape[:2]
  newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  img = cv2.undistort(img, mtx, dist, None, newcameramtx)
  cv2.imwrite(fname[:6]+'_undistorted.png', img)
  ret, corners = cv2.findChessboardCorners(gray, (7,6),None)

  if ret == True:
    cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
    rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners, newcameramtx, dist)
    imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, newcameramtx, dist)

    print "it works"
    img = draw(img,corners,imgpts)
    cv2.imwrite(fname[:6]+'.png', img)

cv2.destroyAllWindows()