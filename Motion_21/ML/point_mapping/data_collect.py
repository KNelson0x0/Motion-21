import cv2
import shutil
import os
import uuid

################################# CHANGE THIS BASED ON WHICH LETTER YOU ARE DOING ####################################

letter = "A"
letter_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J_1", "J_2", "J_3", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,360)
#cap.set(10,100) #for brightness

dir = os.path.dirname(__file__) #directory of this file
#print(dir)
path = dir + '\hand_images_' + letter

#if os.path.exists(path):
#    shutil.rmtree(path)
#os.mkdir(path)

counter = 0

while True:

    success, img = cap.read()

    img = cv2.rectangle(img, (100,100), (300,300), (0,255,0), 2) #image, start_point, end_point, color, thickness
    crop_img = img[100:300, 100:300]

    cv2.imshow("Image", img)
    cv2.imshow("Cropped Image", crop_img)

    key = cv2.waitKey(1)
    if key == ord("s"):
        counter += 1
        cv2.imwrite(os.path.join(path, '{}.jpg'.format(uuid.uuid1())), crop_img)
        print(counter)