import cv2
import numpy as np


image = cv2.imread('hand_palm.jpeg')
gray = cv2.cvtColor(image ,cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray ,(5 ,5) ,0)

retr ,thresh = cv2.threshold(gray ,45 ,255 ,cv2.THRESH_BINARY)
eroded = cv2.erode(thresh ,None ,iterations = 2)
dilate = cv2.dilate(eroded ,None ,iterations = 2 )

contours ,heirarchy = cv2.findContours(dilate.copy() ,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)

c = max(contours ,key = cv2.contourArea)

extremeLeft  = tuple(c[c[: ,: ,0].argmin()][0])
extremeRight = tuple(c[c[: ,: ,0].argmax()][0])
extremeNorth = tuple(c[c[: ,: ,1].argmax()][0])
extremeSouth = tuple(c[c[: ,: ,1].argmin()][0])

cv2.drawContours(image ,[c] ,-1 ,(0 ,255 ,255) ,2)
cv2.circle(image ,extremeLeft ,7 ,(0 ,0 ,255) ,-1)
cv2.circle(image ,extremeRight ,7 ,(0 ,255 ,0) ,-1)
cv2.circle(image ,extremeNorth ,7 ,(255 ,0, 0) ,-1)
cv2.circle(image ,extremeSouth ,7 ,(255 ,255 ,0) ,-1)

cv2.imshow("extreme points" ,image)
cv2.waitKey(0)
