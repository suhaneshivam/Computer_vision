from pyimagesearch.shapedetector import ShapeDetector
import argparse
import  imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,help="path to the input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
resized = imutils.resize(image ,width=300)
ratio = image.shape[0] /float(resized.shape[0])

gray = cv2.cvtColor(resized ,cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray ,(5 ,5) ,0)
retr ,thresh = cv2.threshold(blurred ,60 ,255 ,cv2.THRESH_BINARY)

cnts ,heirarchy = cv2.findContours(thresh ,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)

detector = ShapeDetector()

for c in cnts:
    shape = detector.detect(c)

    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"] * ratio)
    cY = int(M["m01"] / M["m00"] * ratio)

    cv2.putText(image ,shape ,(cX ,cY) ,cv2.FONT_HERSHEY_SIMPLEX ,0.5,(255 ,255 ,255) ,2)
    cv2.imshow("Shape detected" ,image)
    cv2.waitKey(0)
