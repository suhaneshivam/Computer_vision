from videoutils import WebcamVideoStream
from videoutils import FPS
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('-n' ,'--number' ,type = int ,default = 100 ,help = 'no of frames to loop over for FPS test')
ap.add_argument('-d' ,'--display' ,type = int ,default = -1 ,help = 'whether or not frames should be display')
args = vars(ap.parse_args())

 #grab a pointer to the video stream and initialize the FPS counter
print("[INFO] sampling frames from webcam...")
stream = cv2.VideoCapture(0)
fps = FPS()
fps.start()


while fps._numFrames <args['number']:
    (grabbed ,frame) = stream.read()
    frame = imutils.resize(frame ,width = 400)

    if args['display'] > 0:
        cv2.imshow("frame" ,frame)
        key = cv2.waitKey(1) & 0xFF

    fps.update()

fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

stream.release()
cv2.destroyAllWindows()

print("[INFO] sampling THREADED frames from webcam...")
vs = WebcamVideoStream(src = 0).start()
fps = FPS().start()

while fps._numFrames < args['number']:
    #read the frame using run() method defined within WebcamVideoStream class.
    frame = vs.read()

    if args['display'] > 0:
        cv2.imshow('frame' ,frame)
        key = cv2.waitKey(1) & 0xFF
    fps.update()

fps.stop()

print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()
