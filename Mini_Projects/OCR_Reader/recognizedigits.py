import sys
sys.path.append("C:/Users/HP ELITEBOOK 820G3/Documents/GitHub/Computer_vision/Mini_Projects/Helper_classes")

from transform import four_point_transform
from imutils import contours
import imutils
import cv2

DIGIT_LOOKUPS = {
        (1 ,1 ,1 ,0 ,1 ,1 ,1) : 0,
        (0 ,1 ,0 ,0 ,1 ,0 ,0) : 1,
        (1 ,0 ,1 ,1 ,1 ,1 ,0) : 2,
        (1 ,0 ,1 ,1 ,0 ,1 ,1) : 3,
        (0 ,1 ,1 ,1 ,0 ,1 ,0) : 4,
        (1 ,1 ,0 ,1 ,0 ,1 ,1) : 5,
        (1 ,1 ,0 ,1 ,1 ,1 ,1) : 6,
        (1 ,0 ,1 ,0 ,0 ,1 ,0) : 7,
        (1 ,1 ,1 ,1 ,1 ,1 ,1) : 8,
        (1 ,1, 1 ,1 ,0 ,1 ,1) : 9
}

image = cv2.imread("example.jpeg")
image = imutils.resize(image ,height = 500)
gray = cv2.cvtColor(image ,cv2.COLOR_BGRA2GRAY)
blurred = cv2.GaussianBlur(gray ,(5 ,5) ,0)
edged = cv2.Canny(blurred ,50 ,200)


cnts = cv2.findContours(edged.copy() ,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)[0]
cnts = sorted(cnts ,key = cv2.contourArea ,reverse = True)

screenCnt = None

for c in cnts:
    peri = cv2.arcLength(c ,closed = True)
    approx = cv2.approxPolyDP(c ,peri * 0.02 , closed = True)

    if len(approx) == 4:
        screenCnt = approx
        break
warped = four_point_transform(gray ,screenCnt.reshape(4 ,2))
output = four_point_transform(image ,screenCnt.reshape(4 ,2))


thresh = cv2.threshold(warped ,0 ,255 ,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE ,(1 ,5))
thresh = cv2.morphologyEx(thresh ,cv2.MORPH_OPEN ,kernel)
# cv2.imshow("thresh" ,thresh)
# cv2.waitKey(0)

cnts = cv2.findContours(thresh.copy() ,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE )[0]
digitCnts = []

for c in cnts:
    (x ,y ,w ,h) = cv2.boundingRect(c)

    if w >= 15 and (h >=30 and h <= 40):
        digitCnts.append(c)



digitCnts = contours.sort_contours(digitCnts ,method= "left-to-right")[0]
digits = []

for c in digitCnts:
    (x ,y ,w ,h) = cv2.boundingRect(c)
    roi = thresh[y :y + h ,x :x + w]

    (roiH ,roiW) = roi.shape
    (dW ,dH) = (int(0.25 * roiW) ,int(0.15 * roiH) )
    dHC = int(0.05 * roiH)

    #segment contains the (x ,y) coordinate of top-left and botom-right point each of 7 segments rectangles.
    segments = [ ((0 ,0) ,(w ,dH)), #top
                ((0 ,0) ,(dW ,h // 2)), #top-left
                ((w - dW ,0) ,(w ,h //2)), #top-right
                ((0 ,(h //2) - dHC) ,(w ,(h //2) + dHC)), #center
                ((0 ,h //2) ,(dW ,h)), #bottom-left
                ((w - dW ,h //2) ,(w ,h)), #bottom-right
                ((0 ,h - dH) ,(w ,h))] #bottom

    on = [0] * len(segments)

    for (i ,((xA ,yA) ,(xB ,yB))) in enumerate(segments):

        segRoi = roi[yA : yB ,xA : xB]
        total = cv2.countNonZero(segRoi)
        segArea = (xB - xA) * (yB - yA)

        if total/float(segArea) > 0.5:
            on[i] = 1

    digit = DIGIT_LOOKUPS[tuple(on)]
    digits.append(digit)
    cv2.rectangle(output ,(x ,y) ,(x + w ,y + h) ,(0 ,0 ,255) ,1)
    cv2.putText(output ,str(digit) ,(x -10 ,y -10) ,cv2.FONT_HERSHEY_SIMPLEX ,0.65 ,(0 ,0 ,255) ,2)

print(u"{}{}.{} \u00b0C".format(*digits))
cv2.imshow("Input", image)
cv2.imshow("Output", output)
cv2.waitKey(0)
