import imutils
import cv2

class BasicMotionDetector:
    def __init__(self ,accWeight = 0.5 ,deltaThresh = 5 ,minArea = 5000):

        self.accWeight = accWeight
        self.deltaThresh = deltaThresh
        self.minArea = minArea

        #initialize the average image for motion detection
        self.average = None

    def update(self ,image):

        #initializing the list of locations containing motion
        locs = []

        #if average image is none than initialize it.
        if self.average is None:
            self.average = image.astype('float')
            return locs

        cv2.accumulateWeighted(image ,self.average ,self.accWeight)
        frameDelta = cv2.absdiff(image ,cv2.convertScaleAbs(self.average))
        #cv2.imshow("delta" ,frameDelta)

        retr ,thresh = cv2.threshold(frameDelta ,self.deltaThresh ,255 ,cv2.THRESH_BINARY)
        thresh = cv2.dilate(thresh ,None ,iterations=2)

        cnts ,heirarchy = cv2.findContours(thresh ,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            if cv2.contourArea(c) > self.minArea:
                locs.append(c)

        return locs
