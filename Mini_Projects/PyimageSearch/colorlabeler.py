from scipy.spatial import distance
from collections import OrderedDict
import numpy as np
import cv2

class ColorLabeler:
    def __init__(self):
        colors = OrderedDict({'red' : (255 , 0 ,0) ,'green' : (0 ,255 ,0) ,'blue' : (0 ,0 ,255)})
        self.colorNames = []
        self.lab = np.zeros((len(colors) ,1 ,3) , dtype = 'uint8')

        for (i ,(name ,rgb)) in enumerate(colors.items()):
            self.lab[i] = rgb
            self.colorNames.append(name)

        self.lab = cv2.cvtColor(self.lab ,cv2.COLOR_RGB2LAB)

    def label(self ,image ,c):
        mask = np.zeros(image.shape[:2] , dtype = "uint8")
        cv2.drawContours(mask ,[c] ,-1 ,255 ,-1)
        mask = cv2.erode(mask ,None ,iterations=2)
        mean = cv2.mean(image , mask = mask)[:3]
        #mean is nothing but a tuple containing the mean for individual color channels.

        minDist = (np.inf ,None) #second argument is present to keep track of index.

        for (i ,row) in enumerate(self.lab):
            dist = distance.euclidean(row[0] ,mean)

            if dist < minDist[0]:
                minDist = (dist ,i)

        return self.colorNames[minDist[1]]
