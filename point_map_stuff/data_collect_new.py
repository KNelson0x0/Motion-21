import cv2
import shutil
import os
import uuid

cap = cv2.VideoCapture(0)

if os.path.exists('hand_images'):
    shutil.rmtree('hand_images')

os.mkdir('hand_images')
counter = 0

while True:
    success, img = cap.read()
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord("s"):
        counter += 1
        cv2.imwrite(os.path.join('hand_images', '{}.jpg'.format(uuid.uuid1())), img)
        print(counter)