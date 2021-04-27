import cv2
import imutils
import numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-i' ,'--image' ,required = True ,help = 'path to the input image' )
args = vars(ap.parse_args())

image = cv2.imread(args['image'])

gray = cv2.cvtColor(image ,cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray ,(3 ,3) ,0)
#the last argument 0 is corresponding to the standard deviation of filter along x and y
#both are taken as zero if not supplies individually
edged = cv2.Canny(blurred ,20 ,100)

# cv2.imshow("edged" ,edged)
# cv2.waitKey(0)
contours ,heirarchy = cv2.findContours(edged.copy() ,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

# ensure at least one contour was found
if len(contours) > 0:

    # grab the largest contour, then draw a mask for the pill
    c = max(contours ,key = cv2.contourArea)
    mask = np.zeros(image.shape[:2] ,dtype = "uint8")
    cv2.drawContours(mask ,[c] ,-1 ,255 ,-1)

    # compute its bounding box of pill, then extract the ROI,
	# and apply the mask
    (x, y, w, h) = cv2.boundingRect(c)
    #x ,y : x coordinate corresponding to the top left corner of bounding box
    #w,h : width and height of the bounding box
    imageROI = image[y:y + h ,x: x + w]
    maskROI = mask[y:y + h ,x: x + w]
    imageROI = cv2.bitwise_and(imageROI ,imageROI ,mask = maskROI)

    for angle in np.arange(0 ,360 ,15):
        rotated = imutils.rotate_bound(imageROI ,angle)
        cv2.imshow('rotated' ,rotated)
        cv2.waitKey(0)
