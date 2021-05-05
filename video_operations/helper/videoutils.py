import datetime
from threading import Thread
import cv2

class FPS:
    def __init__(self):
        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        self._end = datetime.datetime.now()

    def update(self):
        self._numFrames += 1

    def elapsed(self):
        return (self._end - self._start).total_seconds()

    def fps(self):
        return self._numFrames/self.elapsed()

class WebcamVideoStream:
    def __init__(self ,src = 0):
        # initialize the video camera stream and read the first frame
		# from the stream
        #self.grabbed is either true or false.It determines whether flamed was grabbed or not.
        #self.frame is the actual grabbed frame.
        self.stream = cv2.VideoCapture(src)
        (self.grabbed ,self.frame) = self.stream.read()

        # initialize the variable used to indicate if the thread should
		# be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update ,args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped == True:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed ,self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        self.stopped = True
