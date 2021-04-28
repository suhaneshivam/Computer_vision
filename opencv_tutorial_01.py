import imutils
import cv2
# load the input image and show its dimensions, keeping in mind that
# images are represented as a multi-dimensional NumPy array with
# shape no. rows (height) x no. columns (width) x no. channels (depth)

image = cv2.imread('jp.png')
(h ,w ,d) = image.shape
print(f'height:{h}  width:{w}  channels:{d}')

# cv2.imshow("image" ,image)
# cv2.waitKey(0)

B ,G ,R = image[100 ,50]
print(f'R:{R}  G:{G}  B:{B}')

# extract a 100x100 pixel square ROI (Region of Interest) from the
# input image starting at x=320,y=60 at ending at x=420,y=160
roi = image[60:160 ,250:350]
# cv2.imshow('ROI' ,roi)
#cv2.waitKey(0)

# resize the image to 200x200px, ignoring aspect ratio
resized = cv2.resize(image ,(200,200))
# cv2.imshow('fixed resizing' ,resized)
#cv2.waitKey(0)

# fixed resizing and distort aspect ratio so let's resize the width
# to be 300px but compute the new height based on the aspect ratio
width = 300
height = int(h / w * width)
resized_aspect = cv2.resize(image ,(width ,height))
# cv2.imshow('resized with aspect ration' ,resized_aspect)
#cv2.waitKey(0)

# manually computing the aspect ratio can be a pain so let's use the
# imutils library instead
resized_imutils = imutils.resize(image ,width = 300)
# cv2.imshow('resized with imutils' ,resized_imutils)
# cv2.waitKey(0)

# let's rotate an image 45 degrees clockwise using OpenCV by first
# computing the image center, then constructing the rotation matrix,
# and then finally applying the affine warp
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center = center ,angle = -45 ,scale = 1.0)
# we have added minus sigh before the angle we are dealing in terms of coordinate axis and
#clockwise would be minus angle.
rotated = cv2.warpAffine(image ,M ,(w,h))
# cv2.imshow('cv2 rotation' ,rotated)
# cv2.waitKey(0)

# rotation can also be easily accomplished via imutils with less code
rotated = imutils.rotate(image ,-45)
cv2.imshow('rotation imutils' ,rotated)
cv2.waitKey(0)

# OpenCV doesn't "care" if our rotated image is clipped after rotation
# so we can instead use another imutils convenience function to help
# us out
rotated = imutils.rotate_bound(image ,-45)
cv2.imshow('screen bound rotation imutils' ,rotated)
cv2.waitKey(0)


# apply a Gaussian blur with a 11x11 kernel to the image to smooth it,
# useful when reducing high frequency noise
blurred = cv2.GaussianBlur(image ,(5 ,5) ,0) #the last argument ie 0 is corresponding to standard deviation of kernal
#in x and y direction if we pass single value both sigmaX and sigmaY would be taken as 0.We can pass separate values
#for both sigmaX and sigmaY.

cv2.imshow("blurred" ,blurred)
cv2.waitKey(0)

# draw a 2px thick red rectangle surrounding the face
output = image.copy()
cv2.rectangle(img = output ,pt1 = (250 ,50) ,pt2 = (350 ,150) ,color = (0 ,0 ,255) ,thickness = 2)
cv2.imshow("rectangle" ,output)
cv2.waitKey(0)

# draw a blue 20px (filled in) circle on the image centered at
# x=300,y=150
output = image.copy()
cv2.circle(img = output ,center = (300 ,150) ,radius = 20 ,color = (255 ,0 ,0) ,thickness = -1)
cv2.imshow("filled" ,output)
cv2.waitKey(0)

# draw a 5px thick red line from x=60,y=20 to x=400,y=200
output = image.copy()
cv2.line(output ,(60 ,55) ,(400 ,235) ,(0 ,0 ,255) ,5)
cv2.imshow('line' ,output)
cv2.waitKey(0)

# draw green text on the image
output = image.copy()
cv2.putText(output ,'openCV + Jurrasic Park !!!!' ,(10 ,25) ,cv2.FONT_HERSHEY_TRIPLEX ,fontScale = 0.7 ,color = (0 ,255 ,0) ,thickness = 2)
cv2.imshow("text" ,output)
cv2.waitKey(0)
