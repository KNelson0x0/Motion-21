import cv2
import shutil
import os
import uuid

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,360)
#cap.set(10,100) #for brightness


if os.path.exists('hand_images'):
    shutil.rmtree('hand_images')

os.mkdir('hand_images')
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
        cv2.imwrite(os.path.join('hand_images', '{}.jpg'.format(uuid.uuid1())), crop_img)
        print(counter)