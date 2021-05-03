import argparse
import cv2
import imutils
import time

ap = argparse.ArgumentParser()
ap.add_argument('-v' ,'--video' ,required=True ,help = "path to the video")
args = vars(ap.parse_args())

vs = cv2.VideoCapture(args['video'])

while(True):
    grabbed ,frame = vs.read()

    if not grabbed:
        break

    status = "Not found"

    gray = cv2.cvtColor(frame ,cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray ,(5 ,5) ,0)
    edged = cv2.Canny(blurred ,50 ,150)

    cnts,heirarchy = cv2.findContours(edged ,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        peri = cv2.arcLength(c)
        approx = cv2.approxPolyDP(c ,0.02 * peri ,True)

        if len(approx) => 4 and len(approx) <= 6:
            (x ,y ,w ,h) = cv2.boundingRect(c)
            aspectRatio = w / float(h)
            contourArea = cv2.contourArea(c)
            hullArea = cv2.contourArea(cv2.convexHull(c))
            solodity = contourArea /float(hullArea)

            keepDim = w > 25 and h > 25
            keepSolidity = solodity > 0.95
            keepAspectRatio = aspectRatio >= 0.8 and aspectRatio <= 1.2

            if keepDim and keepSolidity and keepAspectRatio:

                cv2.drawContours(frame ,[approx] ,-1 ,(0 ,0 ,255) ,4)
                status = " Target(s) found"

                M = cv2.moments(c)
                (cX ,cY) = (int(M['m10'] / M['m00']) ,int(M['m01'] / M['m00']))
                cv2.line(frame ,(cX - 0.15 * w ,cY) ,(cX + 0.15 * w ,cY) ,(0 ,0 ,255) ,3)
                cv2.line(frame ,(cx ,cY - 0.15 * h) ,(cx ,cY + 0.15 * h) ,(0 ,0 ,255) ,3)

        cv2.putText(frame ,status ,(20 ,30) ,cv2.FONT_HERSHEY_SIMPLEX ,0.5 ,(0 ,0 ,255) ,2 )

        cv2.imshow("Frame" ,frame)
        key = cv2.waitKey(1) & 0xFF

        if key = ord('q'):
            break

vs.release()
cv2.destroyAllWindows()
