import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('-i' ,'--image' ,required=True ,help = "path to the input image")
args = vars(ap.parse_args())

image = cv2.imread(args['image'])

lower = np.array([0 ,0 ,0])
upper = np.array([15 ,15 ,15])

shapeMask = cv2.inRange(image ,lower ,upper)
cntrs ,retr = cv2.findContours(shapeMask.copy() ,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)

for c in cntrs:
    cv2.drawContours(image ,[c] ,-1 ,(0 ,255 ,0) ,2)
    cv2.imshow('shapes' ,image)
    cv2.waitKey(0)
