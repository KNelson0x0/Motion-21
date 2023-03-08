import os
from os import listdir
import cv2
import numpy as np
import shutil

def empty():
    pass

if os.path.exists('hand_edits'):
    shutil.rmtree('hand_edits')
os.mkdir('hand_edits')

#Get directory
directory = r"C:\Users\pccin\source\repos\point_map_stuff\point_map_stuff\hand_images" #change path to user's directory
directory2 = r"C:\Users\pccin\source\repos\point_map_stuff\point_map_stuff\hand_edits" #change path to user's directory
for images in os.listdir(directory):
    if (images.endswith(".jpg")):
        print(images)
        path = os.path.join(directory, images)
        cv2.namedWindow("TrackBars")
        cv2.resizeWindow("TrackBars", 0, 0)

        #change values based on trackbar testing
        cv2.createTrackbar("Hue Min", "TrackBars", 0, 88, empty) #hue
        cv2.createTrackbar("Hue Max", "TrackBars", 88, 88, empty)
        cv2.createTrackbar("Sat Min", "TrackBars", 174, 255, empty) #saturation
        cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
        cv2.createTrackbar("Val Min", "TrackBars", 0, 255, empty) #value
        cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

        #while True:
        img = cv2.imread(path)
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #converts from BGR to HSV
        h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
        h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
        s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
        s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
        v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
        v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
        print(h_min, h_max, s_min, s_max, v_min, v_max)

        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        mask = cv2.inRange(imgHSV, lower, upper)

        imgResult = cv2.bitwise_and(img, img, mask=mask)

            # cv2.imshow("Original", img)
            # cv2.imshow("HSV", imgHSV)
            # cv2.imshow("Mask", mask)
            # cv2.imshow("Result", imgResult)

        cv2.imshow("image", imgResult)

        path2 = os.path.join(directory2, images)
        cv2.imwrite(path2, imgResult)

        cv2.waitKey(5)
