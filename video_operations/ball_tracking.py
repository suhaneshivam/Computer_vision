from collections import deque
from videoutils import WebcamVideoStream
import numpy as np
import cv2
import imutils
import argparse
import time

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower =(29 ,86 ,6)
greenUpper =(64 ,255 ,255)

pts = deque(maxlen=args['buffer'])

if not args.get('video' ,False):
	vs = WebcamVideoStream(src = 0).start()
else:
	vs = cv2.VideoCapture(args['video'])

time.sleep(2.0)

while True:

	frame = vs.read()
	frame = frame[1] if args.get("video", False) else frame

	if frame is None:
		break

	frame = imutils.resize(frame ,width = 600)
	blurred = cv2.GaussianBlur(frame ,(5 ,5) ,0)
	hsv = cv2.cvtColor(blurred ,cv2.COLOR_BGR2HSV)

	mask = cv2.inRange(hsv ,greenLower ,greenUpper)
	mask = cv2.erode(mask ,None ,iterations = 2)
	mask = cv2.dilate(mask ,None ,iterations =2)
	#cv2.imshow("mask" ,mask)


	cnts ,heirarchy = cv2.findContours(mask.copy() ,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	center = None
	if len(cnts) > 0 :
		c = max(cnts ,key = cv2.contourArea)
		((x ,y) ,radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M['m10']/M['m00']) ,int(M['m01']/M['m00']))

		if radius > 10:
			cv2.circle(frame ,(int(x) ,int(y)) ,int(radius) ,(0 ,255 ,255) ,2)
			cv2.circle(frame ,center ,5 ,(0 , 0 ,255) ,-1)


	pts.appendleft(center)

	for i in range(1 ,len(pts)):
		if pts[i] == None or pts[i -1] == None:
			continue
		thickness = int((np.sqrt(args['buffer']/float(i + 1))) * 2.5)
		cv2.line(frame ,pts[i-1] ,pts[i] ,(0 ,0 ,255) ,thickness)

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord('q'):
		break

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()

#otherwise release the camera
else:
	vs.relaese()

cv2.destroyAllWindows()
