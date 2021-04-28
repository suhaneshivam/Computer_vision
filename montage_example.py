
from imutils import paths
#from imutils import build_montages
import argparse
import random
import numpy as np
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('-i' ,'--images' ,required=True ,help = 'path to the input images directory')
ap.add_argument('-s' ,'--sample' ,type = int ,default = 21 ,help = 'no of images to sample')
args = vars(ap.parse_args())

# grab the paths to the images, then randomly select a sample of
# them
imagespaths = list(paths.list_images(args['images']))
random.shuffle(imagespaths)
imagespaths = imagespaths[:args['sample']]

# initialize the list of images

images = []
for imagePath in imagespaths:
     image = cv2.imread(imagePath)
     images.append(image)


def build_montages(images_list ,image_shape ,montage_shape):
    #image_shape : (width ,hieght)
    #montage_shape :(width ,height)

    image_montages = []
    montage_image = np.zeros(shape=(image_shape[1] * (montage_shape[1]), image_shape[0] * montage_shape[0], 3),dtype=np.uint8)
    cursor_pos = [0 ,0]
    start_new_image = False

    for image in images_list:

        start_new_image = False
        image = cv2.resize(image ,image_shape)
        montage_image[cursor_pos[1]:cursor_pos[1] + image_shape[1], cursor_pos[0]:cursor_pos[0] + image_shape[0]] = image

        cursor_pos[0] += image_shape[0] #update x coordinate

        if cursor_pos[0] >= image_shape[0] * montage_shape[0]:
            cursor_pos[1] += image_shape[1] #update y coordinate and reset x coordinate to 0
            cursor_pos[0] = 0

            if cursor_pos[1] >= image_shape[1] * montage_shape[1]:
                cursor_pos = [0 ,0] #resetting both x and y to 0
                image_montages.append(montage_image)
                montage_image = np.zeros(shape=(image_shape[1] * (montage_shape[1]), image_shape[0] * montage_shape[0], 3),dtype=np.uint8)

                start_new_image = True

    if start_new_image == False:
        image_montages.append(montage_image)  #appending unfinished montage

    return image_montages

montages = build_montages(images, (128, 196), (7, 3))

for montage in montages:
    cv2.imshow("Montage" ,montage)
    cv2.waitKey(0)
