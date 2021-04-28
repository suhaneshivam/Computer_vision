import cv2

class ShapeDetector():
    def __init__(self):
        pass

    def detect(self ,c):

        #perimeter
        shape = "Unidentified"
        peri = cv2.arcLength(c , closed = True)
        approx = cv2.approxPolyDP(c ,epsilon = 0.04 * peri, closed = True)

        if len(approx) == 3 :
            shape = "Triangle"

        elif  len(approx) == 4:
            (x ,y ,w ,h) = cv2.boundingRect(approx)
            aspect_ratio = w /float(h)
            shape = "square" if aspect_ratio >= 0.95 and aspect_ratio <= 1.05 else "Rectangle"

        elif  len(approx) == 5:
            shape = "Pentagon"

        else :
            shape = "Circle"

        return shape
