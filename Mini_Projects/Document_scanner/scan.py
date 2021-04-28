from Helper_classes.transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import cv2
import argparse
import imutils

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,help = "Path to the image to be scanned")
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
aspect_ratio = image.shape[0] /500.0
orig = image.copy()

image = imutils.resize(image ,height= 500)
gray = cv2.cvtColor(image ,cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray ,(5 ,5) ,0)
edged = cv2.Canny(gray ,75 ,200)

cnts ,heirarchy = cv2.findContours(edged ,cv2.RETR_LIST ,cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts ,key = cv2.contourArea ,reverse= True)[:5]

for c in cnts:
    peri = cv2.arcLength(c ,closed = True)
    approx = cv2.approxPolyDP(c, 0.02 *peri, closed = True)

    if len(approx) == 4:
        screenContour = approx
        break

cv2.drawContours(image ,[screenContour] ,-1 ,(0 ,255 ,0) ,2)

# apply the four point transform to obtain a top-down
# view of the original image
warped = four_point_transform(orig ,screenContour.reshape(4 ,2) * aspect_ratio)

# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
warped = cv2.cvtColor(warped ,cv2.COLOR_BGR2GRAY)
T = threshold_local(warped ,block_size = 11 , method= 'gaussian' , offset= 10)
warped = (warped > T).astype("uint8") * 255

cv2.imshow("Original", imutils.resize(orig, height = 650))
cv2.imshow("Scanned", imutils.resize(warped, height = 650))
cv2.waitKey(0)
