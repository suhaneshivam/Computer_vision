from imutils import paths
import numpy as np
import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-i' ,'--images' ,type = str ,required = True ,help = "path to the input image directory")
ap.add_argument('-o' ,'--output' ,type = str ,required = True ,help = "path to the output")
ap.add_argument('-c' , '--crop' ,type = int ,default=0 ,help = "whether to crop the panorama or not")
args = vars(ap.parse_args())

imagePaths = sorted(list(paths.list_images(args['images'])))
images = []

for imagePath in imagePaths:
    image = cv2.imread(imagePath)
    images.append(image)

stitcher = cv2.Stitcher_create()
(status,stitched) = stitcher.stitch(images)

if status == 0:
    if args['crop'] >0:

        stitched = cv2.copyMakeBorder(stitched, 10, 10, 10, 10,cv2.BORDER_CONSTANT, (0, 0, 0))
        gray = cv2.cvtColor(stitched ,cv2.COLOR_BGR2GRAY)
        retr ,thresh = cv2.threshold(gray ,0 ,255 ,cv2.THRESH_BINARY)
        # cv2.imshow('thresh' ,thresh)
        # cv2.waitKey(0)

        cnts ,heirarchy = cv2.findContours(thresh.copy() ,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)
        c = max(cnts ,key = cv2.contourArea)
        (x ,y ,w ,h) = cv2.boundingRect(c)

        mask = np.zeros(thresh.shape ,dtype='uint8')
        cv2.rectangle(mask ,(x ,y) ,(x + w ,y + h) ,255 ,-1)

        minRect = mask.copy()
        sub = mask.copy()

        while cv2.countNonZero(sub) > 0:

            minRect = cv2.erode(minRect ,None)
            sub = cv2.subtract(minRect ,thresh)


        cnts ,heirarchy = cv2.findContours(minRect.copy() ,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)
        print(len(cnts))

        c = max(cnts ,key = cv2.contourArea)
        (x ,y ,w ,h) = cv2.boundingRect(c)

        stitched = stitched[y : y + h ,x : x +w]

        cv2.imwrite(args['output'] ,stitched)
        cv2.imshow("better panorama" ,stitched)
        cv2.waitKey(0)


    else:
        print("no stitching happen. staus : {}" .format(status))
