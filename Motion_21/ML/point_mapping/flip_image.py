import cv2
import os
from os import listdir

dir_list = ["Z"]#["A", "B", "C", "D", "E", "F", "G", "H", "I", "J_1", "J_2", "J_3", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
dir = os.path.dirname(__file__)

for i in range(len(dir_list)):
    directory = dir + '\hand_images_' + dir_list[i]
    for image in os.listdir(directory):
        image_flipped_name = image.replace(".jpg", "_flipped.jpg")
        if image_flipped_name not in os.listdir(directory): #doesn't already have a flipped version
            if "flipped" not in image: #not already a flipped image (don't want to flip twice)
                img = cv2.imread(os.path.join(directory, image))
                img_flip = cv2.flip(img, 1) #flips image horizontally
                cv2.imwrite(os.path.join(directory, image.replace(".jpg", "_flipped.jpg")), img_flip)
                #print("Image changed")

print("Success!")