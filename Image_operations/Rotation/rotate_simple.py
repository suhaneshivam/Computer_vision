import numpy as np
import cv2
import argparse
import imutils


ap = argparse.ArgumentParser()
ap.add_argument('-i' ,'--image' ,required = True ,help = 'path to the input image')
args = vars(ap.parse_args())

image = cv2.imread(args['image'])

for angle in np.arange(0 ,360 ,15):
    rotate = imutils.rotate(image ,angle)
    cv2.imshow('rotate incorrect' ,rotate)
    cv2.waitKey(0)

for angle in np.arange(0 ,360 ,15):
    rotate = imutils.rotate_bound(image ,angle)
    cv2.imshow('rotate correct' ,rotate)
    cv2.waitKey(0)

def correct_rotation(image ,angle):

    (h ,w) = image.shape[:2]
    (cY ,cX) = (h // 2 ,w // 2)

    M = cv2.getRotationMatrix2D((cX ,cY) ,angle ,scale = 1)
    cos = np.abs(M[0 ,0])
    sin = np.abs(M[0 ,1])

    nH = int(h * cos + w * sin)
    nW = int(h * sin + w * cos)

    #we need to substract centre from new centre to account for the translation
    #in the image and add this to the original value.
    M[0 ,2] += (nW / 2) - cX
    M[1 ,2] += (nH / 2) - cY

    rotated = cv2.warpAffine(image ,M , (nW ,nH))
    return rotated

for angel in np.arange(0 ,360 ,15):
    rotated = correct_rotation(image ,angel)
    cv2.imshow("correctly rotated" ,rotated)
    cv2.waitKey(0)
