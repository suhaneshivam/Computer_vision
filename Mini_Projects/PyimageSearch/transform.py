import numpy as np
import cv2
from scipy.spatial import distance as dist

def order_points_old(pts):
    # initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4 ,2) ,dtype="float32")

    s = pts.sum(axis = 1)

    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    d = np.diff(pts ,axis = 1) #difference is calculated by substracting x from y i.e. (y -x) not (x - y)

    rect[1] = pts[np.argmin(d)]
    rect[3] = pts[np.argmax(d)]

    return rect

def order_points(pts):

    #sort the pts from left to right according to their x cordinate
    xSorted = pts[np.argsort(pts[: ,1]) , :]

    leftMost = xSorted[ : 2]
    rightMost = xSorted[2 : ]

    #now we have the two leftmost points les us sort their y cordinate to get top left and bottom left
    leftMost = leftMost[np.argsort(leftMost[ : ,1]) ,:]
    (tl ,bl) = leftMost

    # now that we have the top-left coordinate, use it as an
	# anchor to calculate the Euclidean distance between the
	# top-left and right-most points; by the Pythagorean
	# theorem, the point with the largest distance will be
	# our bottom-right point
    d = dist.cdist(tl[np.newaxis] ,rightMost ,'euclidean')[0]
    # dist.cdist return a array of order m1 x m2 if we input m1 x n and m2 x n arrays. here
    # we input 1 x 2 and 2 x 2 array as tl[np,newaxis] and rightMost which looks like
    #[[d1 ,d2]]
    rightMost = rightMost[np.argsort( d)[::-1] , :]
    (br ,tr) = rightMost

    return np.array([tl ,tr ,br ,bl] , dtype = "float32")

def four_point_transform(image ,pts):
    rect = order_points(pts)
    (tl ,tr ,br ,bl) =rect

    widthA = np.sqrt(((br[0] -bl[0]) **2 ) + ((br[1] -bl[1]) **2))
    widthB = np.sqrt(((tr[0] -tl[0]) **2 ) + ((tr[1] -tl[1]) **2))
    maxWidth = max(int(widthA) ,int(widthB))

    heightA = np.sqrt(((br[0] -tr[0]) **2 ) + ((br[1] -tr[1]) **2))
    heightB = np.sqrt(((bl[0] -tl[0]) **2 ) + ((br[1] -tr[1]) **2))
    maxHeight = max(int(heightA) ,int(heightB))

    #now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
    dst = np.array([[0 ,0] ,[maxWidth -1 ,0] ,[maxWidth -1 ,maxHeight -1] ,[0 ,maxHeight -1]] ,dtype= 'float32')

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect ,dst)
    warped = cv2.warpPerspective(image ,M ,(maxWidth ,maxHeight))

    return warped
