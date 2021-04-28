from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('-i' ,'--image' ,required=True ,help = "path to the image")
args = vars(ap.parse_args())

# define the answer key which maps the question number
# to the correct answer
ANSWER_KEY = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}

image = cv2.imread(args['image'])
gray = cv2.cvtColor(image ,cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray ,(5, 5) ,0)
edged = cv2.Canny(blurred ,75 ,200)

cnts, heirarchy = cv2.findContours(edged.copy() ,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts ,key = cv2.contourArea ,reverse= True)

docCnt = None
for c in cnts:
    peri = cv2.arcLength(c ,closed = True)
    approx = cv2.approxPolyDP(c ,0.02 * peri ,closed = True)

    if len(approx) == 4:
        docCnt = approx
        break

paper = four_point_transform(image ,docCnt.reshape(4 ,2))
warped = four_point_transform(gray ,docCnt.reshape(4 ,2))

# cv2.imshow("warped" ,warped)
# cv2.imshow('paper' ,paper)
# cv2.waitKey(0)

retr ,thresh = cv2.threshold(warped ,0 ,255 ,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
#we pass 0 as threshold because we dont know the optimal value, the let THRESH_OTSU calcualte the value.
#we are applying both THRESH_BINARY and THRESH_OTSU simultaneously.
cnts = cv2.findContours(thresh ,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)[0]
questionContours = []

for c in cnts:
    (x ,y ,w ,h) = cv2.boundingRect(c)
    aspect_ratio = w /float(h)

    if w >= 20 and h >= 20 and aspect_ratio >= 0.9 and aspect_ratio <= 1.1:
        questionContours.append(c)

questionContours = contours.sort_contours(questionContours ,method = "top-to-bottom")[0]
#remember this function returns a tuple of sorted contours and bounding boxes.

correct = 0

for (q ,i) in enumerate(np.arange(0 ,len(questionContours) ,5)):
    cnts = contours.sort_contours(questionContours[i : i+5])[0]
    bubbled = None

    #loop over the sorted contours
    for (j ,c) in enumerate(cnts):
        mask = np.zeros(thresh.shape ,dtype = 'uint8' )
        cv2.drawContours(mask ,[c] ,-1 ,255,-1)
        mask = cv2.bitwise_and(thresh ,thresh ,mask = mask)
        total = cv2.countNonZero(mask)

        if bubbled == None or total > bubbled[0]:
            bubbled = (total ,j)

    color = (0 ,0 ,255)
    k = ANSWER_KEY[q]

    if bubbled[1] == k:
        color = (0 ,255 ,0)
        correct += 1

    cv2.drawContours(paper ,[cnts[k]] ,-1 ,color ,3)

score = (correct / 5.0) * 100
print("[INFO] score: {:.2f}%".format(score))
cv2.putText(paper, "{:.2f}%".format(score), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
cv2.imshow("Original", image)
cv2.imshow("Exam", paper)
cv2.waitKey(0)
