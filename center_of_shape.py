import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-i' ,'--image' ,required=True ,help = 'path to the input image')
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
gray = cv2.cvtColor(image ,cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray ,(5 ,5) ,0)
#last argument in blurring is corresponding to the standard deviation along x and y direction of
#filter. if not provided separatelty both are taken as 0.
retr ,thresh = cv2.threshold(blurred ,60 ,255 ,cv2.THRESH_BINARY)

cntrs ,heirarchy = cv2.findContours(thresh.copy() ,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)

for c in cntrs:

    M = cv2.moments(c)
    cX = int(M['m10'] / M['m00'])
    cY = int(M['m01'] / M['m00'])
    cv2.drawContours(image ,[c] ,-1 ,(0 ,0 ,255) ,2)
    cv2.circle(image ,(cX ,cY) ,7 ,(255,255,255) ,-1)
    cv2.putText(image ,"center" ,(cX -10 ,cY -10) ,cv2.FONT_HERSHEY_TRIPLEX ,0.5 ,(255 ,255 ,255) ,2)

    cv2.imshow('center drawn' ,image)
    cv2.waitKey(0)
    
