import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('-i' ,'--image' ,required=True ,help = 'path to the input image')
args = vars(ap.parse_args())

# load the input image (whose path was supplied via command line
# argument) and display the image to our screen
image = cv2.imread(args['image'])
cv2.imshow('image' ,image)
cv2.waitKey(0)

#convert the image into grayscale
gray = cv2.cvtColor(image ,cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray' ,gray)
cv2.waitKey(0)

# applying edge detection we can find the outlines of objects in
# images
edged = cv2.Canny(image ,30 ,150)
# img : The gray image.
# minVal : A minimum threshold, in our case 30 .
# maxVal : The maximum threshold which is 150 in our example.
# aperture_size : The Sobel kernel size. By default this value is 3 and hence is not shown on Line 25.
cv2.imshow('edged' ,edged)
cv2.waitKey(0)

# threshold the image by setting all pixel values less than 225
# to 255 (white; foreground) and all pixel values >= 225 to 0
# (black; background), thereby segmenting the image
# The function cv.threshold is used to apply the thresholding.
# The first argument is the source image, which should be a grayscale image.
# The second argument is the threshold value which is used to classify the pixel values.
# The third argument is the maximum value which is assigned to pixel values exceeding the threshold.
# OpenCV provides different types of thresholding which is given by the fourth parameter of the function.
# Basic thresholding as described above is done by using the type cv.THRESH_BINARY.
threshold = cv2.threshold(gray ,225 ,255 ,cv2.THRESH_BINARY_INV)[1]
cv2.imshow('threshed' ,threshold)
cv2.waitKey(0)

# find contours (i.e., outlines) of the foreground objects in the
# thresholded image
# In OpenCV, finding contours is like finding white object from black background.
# So remember, object to be found should be white and background should be black.
cnts ,heirarchy= cv2.findContours(threshold.copy() ,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)
#first argument is image itself
#second argument determines the heirarchy to be used and retured
#third argument determines the no of point of same intensity along the boundary to be retured
#return : image,contours,heirarchy
output = image.copy()

for cnt in cnts:
    cv2.drawContours(output ,[cnt] ,-1 ,(240 ,0 ,159) ,3)
    cv2.imshow('output' ,output)
    cv2.waitKey(0)
text = f'I have found {len(cnts)} contours in the image'
cv2.putText(output ,text ,(10 ,25) ,cv2.FONT_HERSHEY_COMPLEX ,fontScale = 0.7 ,color = (240 ,0 ,159) ,thickness = 3)
cv2.imshow('text' ,output)
cv2.waitKey(0)


# we apply erosions to reduce the size of foreground objects
mask = threshold.copy()
mask = cv2.erode(mask ,kernel = None ,iterations = 5)
cv2.imshow('eroded' ,mask)
cv2.waitKey(0)

# similarly, dilations can increase the size of the ground objects
mask = cv2.dilate(mask ,kernel = None ,iterations = 5)
cv2.imshow('dilated' ,mask)
cv2.waitKey(0)

# a typical operation we may want to apply is to take our mask and
# apply a bitwise AND to our input image, keeping only the masked
# regions
mask = threshold.copy()
output = cv2.bitwise_and(image ,image ,mask = mask)
cv2.imshow('masked' ,output)
cv2.waitKey(0)
