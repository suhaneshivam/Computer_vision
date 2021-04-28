from pyimagesearch.colorlabeler import ColorLabeler
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('-i' ,'--image' ,required = True ,help = 'path to the input image')
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
resized = imutils.resize(image ,width = 300)
aspect_ratio = image.shape[0] /float(resized.shape[0])

blurred = cv2.GaussianBlur(resized ,(5 ,5) ,0)
gray = cv2.cvtColor(blurred ,cv2.COLOR_BGR2GRAY)
lab = cv2.cvtColor(blurred ,cv2.COLOR_BGR2LAB)
retr ,thresh = cv2.threshold(gray ,60 ,255 ,cv2.THRESH_BINARY)

cnts ,heirarchy = cv2.findContours(thresh.copy() ,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)

sd = ShapeDetector()
cl = ColorLabeler()

for c in cnts:
    shape = sd.detect(c)
    color = cl.label(lab ,c)

    M = cv2.moments(c)
    cX = int(M['m10'] / M['m00'] *aspect_ratio)
    cY = int(M['m01'] / M['m00'] *aspect_ratio)

    c = c.astype("float")
    c *= aspect_ratio
    c = c.astype("int")

    cv2.drawContours(image, [c], -1, (255, 0, 0), 2)
    cv2.putText(image ,f'{color} {shape}' ,(cX ,cY) ,cv2.FONT_HERSHEY_TRIPLEX ,0.5 ,(255 ,255 ,255) ,2)
    cv2.imshow("image" ,image)
    cv2.waitKey(0)
