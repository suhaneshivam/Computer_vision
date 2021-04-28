import cv2
import argparse
import numpy as np
import imutils

def sort_contours(contours ,method = "left-to-right"):
    reverse = False
    i = 0

    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    boundingBoxes = [cv2.boundingRect(c) for c in contours]
    (cntrs ,boundingBoxes) = zip(*sorted(zip(contours ,boundingBoxes) ,key=lambda b : b[1][i] ,reverse=reverse))

    return (cntrs ,boundingBoxes)

def draw_contour(image ,c ,i):

    M= cv2.moments(c)
    cX = int(M['m10'] / M['m00'])
    cY = int(M['m01'] / M['m00'])

    cv2.putText(image ,f'#{i+1}' ,(cX-10 ,cY) ,cv2.FONT_HERSHEY_DUPLEX ,1.0 ,(255 ,255 ,255) ,2)

    return image

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the input image")
ap.add_argument("-m", "--method", required=True, help="Sorting method")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
accumEdged = np.zeros(image.shape[:2], dtype="uint8")

# blurred = cv2.medianBlur(image, 11)
# edged = cv2.Canny(blurred, 50, 200)
#
# cv2.imshow("Edge Map", edged)
# cv2.waitKey(0)

for chan in cv2.split(image):
	# blur the channel, extract edges from it, and accumulate the set
	# of edges for the image
	chan = cv2.medianBlur(chan, 11)
	edged = cv2.Canny(chan, 50, 200)
	accumEdged = cv2.bitwise_or(accumEdged, edged)

cv2.imshow("Edge Map", accumEdged)
cv2.waitKey(0)

cnts = cv2.findContours(accumEdged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:4]
orig = image.copy()

(cnts, boundingBoxes) = sort_contours(cnts, method=args["method"])

for (i, c) in enumerate(cnts):
	draw_contour(image, c, i)

cv2.imshow("Sorted", image)
cv2.waitKey(0)
