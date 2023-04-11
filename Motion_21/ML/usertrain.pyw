import cv2
import time
import numpy
import customtkinter
from   os.path  import exists
from   os       import mkdir
from   os       import remove
import os
from   Utils.utils import *
from   Utils.camera import Camera
from   Utils.constants import *
from sklearn.preprocessing                import LabelBinarizer
from sklearn.model_selection              import train_test_split
from tensorflow.keras                     import backend as be
from tensorflow.keras.models              import Sequential
from tensorflow.keras.layers              import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from tensorflow.keras.optimizers          import Adam 
from tensorflow.keras.preprocessing.image import ImageDataGenerator



class UserTrain:
    def __init__(self, username, symbol, main_window = None):
        self.user_name = username
        self.symbol = symbol
        self.main_window = main_window
        self.label = None
        self.frames_collected = 0

        if self.main_window == None: return;

        self.main_path = os.path.abspath(os.path.join(file, os.pardir))
        self.higher_p = os.path.abspath(os.path.join(self.main_path, os.pardir))
        self.main_train = self.higher_p + r"\UserData"

        if not exists(self.main_train):
            mkdir(self.main_train)

        if not exists(self.main_train + r"\ML"): # bad but i need it to work just for now)
            mkdir(self.main_train + r"\ML") # change path to actually be dynamic

        if not exists(self.main_train + r"\ML\train"):
            mkdir(self.main_train + r"\ML\train")

        if not exists(self.main_train + r"\ML\test"):
            mkdir(self.main_train + r"\ML\test")

    def augment(self):
        train_datagen = ImageDataGenerator(rescale=1./255, rotation_range=30, width_shift_range=0.3, height_shift_range=0.3, horizontal_flip=False, fill_mode='nearest')
        validation_datagen = ImageDataGenerator(rescale=1./255)

        train_generator = train_datagen.flow_from_directory('./UserData/{}/ML/{}/train'.format(self.user_name, self.symbol), target_size=(28, 28), batch_size=32, color_mode = 'grayscale', class_mode='binary')
        validation_generator = validation_datagen.flow_from_directory( './UserData/{}/ML/{}/test'.format(self.user_name, self.symbol), target_size=(28, 28), batch_size=32, color_mode = 'grayscale', class_mode='binary')

        model = Sequential()
        model.add(Conv2D(64, kernel_size=(3,3), activation = 'relu', input_shape=(28,28,1) ))
        model.add(MaxPooling2D(pool_size = (2, 2)))

        model.add(Conv2D(64, kernel_size = (3, 3), activation = 'relu'))
        model.add(MaxPooling2D(pool_size = (2, 2)))

        model.add(Conv2D(64, kernel_size = (3, 3), activation = 'relu'))
        model.add(MaxPooling2D(pool_size = (2, 2)))

        model.add(Flatten())
        model.add(Dense(128, activation = 'relu'))
        model.add(Dropout(0.20))

        model.add(Dense(1, activation = 'sigmoid'))

        model.compile(loss = 'binary_crossentropy', optimizer = 'rmsprop', metrics = ['accuracy'])

        model.save("user_model_{}.h5".format(self.symbol))

    def collect(self):
        crop = cv2.cvtColor(Camera().cropped_frame, cv2.COLOR_BGR2GRAY)
        crop = cv2.resize(crop, (28,28), interpolation = cv2.INTER_AREA)

        if (self.frames_collected <= 150):
            cv2.imwrite("Replace with your path{}.jpg".format(self.user_name, symbol, self.frames_collected))
        else:
            cv2.imwrite("Replace with your path{}.jpg".format(self.user_name, symbol, self.frames_collected-150))

    def on_begin(self):
        try:
            self.label = find_element(self.main_window, 'Please sign the letter "{}" that you want \nMotion 21 to use as an example!'.format(self.symbol))
            self.label.configure(text = "Configuration started!")
            return True
        except:
            debug_log("OnBegin failed")
        return False
       
