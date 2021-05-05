from imutils import paths
import cv2
import imutils
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-i' ,'--images' ,type = str ,required = True ,help = 'path to the input image directory')
ap.add_argument('-o' ,'--output' ,type = str ,required = True ,help ='path to the output')
args = vars(ap.parse_args())

imagePaths = sorted(list(paths.list_images(args['images'])))
images = []

for imagePath in imagePaths:
    image = cv2.imread(imagePath)
    images.append(image)

stitcher = cv2.Stitcher_create()
(status ,stitched) = stitcher.stitch(images)

if status == 0:
    cv2.imwrite(args['output'] ,stitched)
    cv2.imshow("pano" ,stitched)
    cv2.waitKey(0)

else:
    print("panorama can not be formed. status :{}".format(status))
