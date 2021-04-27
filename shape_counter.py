import argparse
import cv2
import imutils

ap = argparse.ArgumentParser()
ap.add_argument('-i' ,'--input' ,required = True , help = 'path to the uinput image')
ap.add_argument('-o' ,'--output' ,required = True , help = 'path to the output image')
args = vars(ap.parse_args())

#load the input image from the disk
image = cv2.imread(args['input'])

#convert the image into gray scale ,blur it and threshold it.
gray = cv2.cvtColor(image ,cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray ,(5,5) ,0)
thresh = cv2.threshold(blurred ,60 ,255 ,cv2.THRESH_BINARY)[1]

#extract the contours from the image
cnts = cv2.findContours(thresh.copy() ,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

#loop over the contours and draw them over the image
for c in cnts:
    cv2.drawContours(image ,[c] ,-1 ,(0 ,0 ,255) ,2)

#Display the total number of shapes on the image
text = f' I found {len(cnts)} no of shape '
cv2.putText(image ,text ,(10 ,20) ,cv2.FONT_HERSHEY_SIMPLEX ,0.5 ,(0 ,0 ,255) ,2)

#write the output iamge to the disk
cv2.imwrite(args['output'] ,image)
