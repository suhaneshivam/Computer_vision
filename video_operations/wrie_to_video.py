from videoutils import WebcamVideoStream
import numpy as np
import imutils
import argparse
import time
import cv2


ap = argparse.ArgumentParser()
ap.add_argument('-o' ,'--output' ,required = True ,help = 'path to the output video file')
ap.add_argument('-p' ,'--pi' ,type = int ,default=-1 ,help = 'wheteher take stream from raspberry pi or not')
ap.add_argument('-f' ,'--fps' ,type = int ,default = 20 ,help = 'frames per second')
ap.add_argument('-c' ,'--codec' ,type = str ,default = 'MJPG' ,help = 'Codec to be used')
args = vars(ap.parse_args())

print("[INFO] warming up camera...")
vs = WebcamVideoStream().start()
time.sleep(2.0)

fourcc = cv2.VideoWriter_fourcc(*args['codec'])
#we have a star before argument beacuse we want to pass the argument as 'M','J','P','G'.
writer = None
(h ,w) = (None ,None)
zeros = None

while True:
    frame = vs.read()
    frame = imutils.resize(frame ,width=300)

    if writer is None:
        (h ,w) = frame.shape[:2]
        writer = cv2.VideoWriter(args['output'] ,fourcc ,args['fps'] ,(w * 2 ,h * 2) ,True)
        #last agrument is to tell whether we want to write color frames to file or not.
        zeros = np.zeros((h ,w) ,dtype = 'uint8')

    (B ,G ,R) = cv2.split(frame)
    R = cv2.merge([zeros ,zeros ,R])
    G = cv2.merge([zeros ,G ,zeros])
    B = cv2.merge([B ,zeros ,zeros])

    output = np.zeros((h * 2,w * 2 ,3) ,dtype = 'uint8')
    output[0:h ,0:w] = frame
    output[0:h ,w:w*2] = R
    output[h:h*2 ,w:w*2] = G
    output[h:h*2 ,0:w] = B

    writer.write(output)

    cv2.imshow("frame" ,frame)
    cv2.imshow("output" ,output)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

# do a bit of cleanup
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
vs.stop()
writer.release()
