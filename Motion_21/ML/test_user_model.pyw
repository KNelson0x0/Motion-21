import cv2
import mediapipe
import os
from usermodel import UserModel

#Pass in letter from GUI here
letter = "10"

#Pass in button presses from GUI here
take_picture = "s"
stop_data_collect = "d"

UserModel().data_collect(letter, take_picture, stop_data_collect)
UserModel().run_user_model(letter)