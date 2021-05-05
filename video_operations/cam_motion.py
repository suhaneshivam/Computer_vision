from helper.basicmotiondetector import BasicMotionDetector
from helper.videoutils import WebcamVideoStream
import numpy as np
import datetime
import imutils
import time
import cv2

print("[INFO] : Starting camera")

webcam = WebcamVideoStream(src = 0).start()
time.sleep(2.0)

camMotion = BasicMotionDetector()

total = 0

while True:

    frame = webcam.read()
    frame = imutils.resize(frame ,width = 400)

    gray = cv2.cvtColor(frame ,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray ,(21 ,21) ,0)
    locs = camMotion.update(gray)


    if total > 32:
        if len(locs) > 0:

            (minX ,minY) = (np.inf ,np.inf)
            (maxX ,maxY) = (-np.inf ,-np.inf)

            for c in locs:
                (x ,y ,w ,h) = cv2.boundingRect(c)
                (minX ,minY) =(min(x ,minX) ,min(y ,minY))
                (maxX ,maxY) =(max(x + w ,maxX) ,max(y + h ,maxY))

            cv2.rectangle(frame ,(minX ,minY) ,(maxX ,maxY) ,(0 ,0 ,255) ,2)

    total += 1
    timestamp = datetime.datetime.now()
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")

    cv2.putText(frame ,ts ,(10 ,frame.shape[0] - 10) ,cv2.FONT_HERSHEY_SIMPLEX ,0.35 ,(0 ,0 ,255) ,1)
    cv2.imshow("Webcame" ,frame)
    key = cv2.waitKey(1) & 0xFF
    cv2

    if key == ord('q'):
        break

print('[INFO] : Cleaning up all windows')
webcam.stop()
cv2.destroyAllWindows()
