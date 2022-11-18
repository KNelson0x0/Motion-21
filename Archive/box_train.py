# Load our libaries
import cv2
import numpy as np
import pandas as pd
from random import randint
import matplotlib.pyplot as plt
from Python.Utilities.utils import debug_log
from sklearn.preprocessing   import LabelBinarizer
from sklearn.model_selection import train_test_split
from tensorflow.keras import backend
from tensorflow.keras.optimizers import Adam 
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout

# Get our Training and Test Data

class MLSys:
    def __init__(self):
        self.train = 0
        self.test_data = 0
        self.images = []
        self.model = Sequential()

    def train_mst_data(self):
        self.train = pd.read_csv('C:/Users/Resu/Documents/Dev/C stuff stuff/Motion 21/Motion 21/Python/ML/sign_mnist_train/sign_mnist_train.csv')
        self.test = pd.read_csv('C:/Users/Resu/Documents/Dev/C stuff stuff/Motion 21/Motion 21/Python/ML/sign_mnist_test/sign_mnist_test.csv')

        self.train.head()
        labels = self.train['label'].values

        self.train.drop('label', axis = 1, inplace = True)
        self.images = self.train.values
        self.images = np.array([np.reshape(i, (28, 28)) for i in self.images])
        self.images = np.array([i.flatten() for i in self.images])

        label_binrizer = LabelBinarizer()
        labels = label_binrizer.fit_transform(labels)

        x_train, x_test, y_train, y_test = train_test_split(self.images, labels, test_size = 0.3, random_state = 101)

        x_train = x_train / 255 # scaling
        x_test = x_test / 255 # scaling

        x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
        x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)


        # Model Configing:
        self.model.add(Conv2D(64, kernel_size=(3,3), activation = 'relu', input_shape=(28, 28 ,1) ))
        self.model.add(MaxPooling2D(pool_size = (2, 2)))

        self.model.add(Conv2D(64, kernel_size = (3, 3), activation = 'relu'))
        self.model.add(MaxPooling2D(pool_size = (2, 2)))

        self.model.add(Conv2D(64, kernel_size = (3, 3), activation = 'relu'))
        self.model.add(MaxPooling2D(pool_size = (2, 2)))

        self.model.add(Flatten())
        self.model.add(Dense(128, activation = 'relu'))
        self.model.add(Dropout(0.20))

        self.model.add(Dense(24, activation = 'softmax'))

        self.model.compile(loss = 'categorical_crossentropy',
              optimizer= Adam(),
              metrics=['accuracy'])

        print(self.model.summary())

        EPOCHS = 10
        history = self.model.fit(x_train, y_train, validation_data = (x_test, y_test), epochs=EPOCHS, batch_size=128) # this will take time
        self.model.save("drippy_mnist_model.h5")
        debug_log("[-] Model Training Completed.")


    def show_rand_img(self):
        if self.images == []:
            debug_log("[X] No Images, train and then call this.")
            return

        cv2.imshow(self.images[randint(0,len(self.images)-1)])
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
def get_letter(result):
    letters = { 0: 'A',
                    1: 'B',
                    2: 'C',
                    3: 'D',
                    4: 'E',
                    5: 'F',
                    6: 'G',
                    7: 'H',
                    8: 'I',
                    9: 'K',
                    10: 'L',
                    11: 'M',
                    12: 'N',
                    13: 'O',
                    14: 'P',
                    15: 'Q',
                    16: 'R',
                    17: 'S',
                    18: 'T',
                    19: 'U',
                    20: 'V',
                    21: 'W',
                    22: 'X',
                    23: 'Y'}
    try:
        res = int(result)
        return letters[res]
    except:
        return "Nigga Whut"


def custom_data():
    cap = cv2.VideoCapture(0)
    i=0
    image_count = 0
    
    while i < 7:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        #define region of interest
        roi = frame[100:400, 320:620]
        cv2.imshow('roi', roi)
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        roi = cv2.resize(roi, (28, 28), interpolation = cv2.INTER_AREA)

        cv2.imshow('roi sacled and gray', roi)
        copy = frame.copy()
        cv2.rectangle(copy, (320, 100), (620, 400), (255,0,0), 5)
    
        if i == 0:
            image_count = 0
            cv2.putText(copy, "Hit Enter to Record when ready", (100 , 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
        if i == 1:
            image_count+=1
            cv2.putText(copy, "Recording 1st gesture - Train", (100 , 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
            cv2.putText(copy, str(image_count), (400 , 400), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
            gesture_one = 'C:/Users/Resu/Documents/Dev/C stuff stuff/Motion 21/Motion 21/Python/ML/custom_data/gesture_1/train'
            cv2.imwrite(gesture_one + str(image_count) + ".jpg", roi)
        if i == 2:
            image_count+=1
            cv2.putText(copy, "Recording 1st gesture - Test", (100 , 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
            cv2.putText(copy, str(image_count), (400 , 400), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
            gesture_one = 'C:/Users/Resu/Documents/Dev/C stuff stuff/Motion 21/Motion 21/Python/ML/custom_data/gesture_1/test'
            cv2.imwrite(gesture_one + str(image_count) + ".jpg", roi)
        if i == 3:
            cv2.putText(copy, "Hit Enter to Record when ready to Record 2nd gesture", (100 , 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
        if i == 4:
            image_count+=1
            cv2.putText(copy, "Recording 2nd gesture - Train", (100 , 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
            cv2.putText(copy, str(image_count), (400 , 400), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
            gesture_two = 'C:/Users/Resu/Documents/Dev/C stuff stuff/Motion 21/Motion 21/Python/ML/custom_data/gesture_2/train'
            cv2.imwrite(gesture_two + str(image_count) + ".jpg", roi)
        if i == 5:
            image_count+=1
            cv2.putText(copy, "Recording 2nd gesture - Test", (100 , 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
            cv2.putText(copy, str(image_count), (400 , 400), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
            gesture_two = 'C:/Users/Resu/Documents/Dev/C stuff stuff/Motion 21/Motion 21/Python/ML/custom_data/gesture_2/test'
            cv2.imwrite(gesture_two + str(image_count) + ".jpg", roi)
        if i == 6:
            cv2.putText(copy, "Hit Enter to Exit", (100 , 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
        cv2.imshow('frame', copy)    

        if cv2.waitKey(1) == 13: #13 is the Enter Key
            image_count = 0
            i+=1


def _main():

    sys = MLSys();
    sys.train_mst_data();

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
    
        frame=cv2.flip(frame, 1)

        #define region of interest
        roi = frame[100:400, 320:620]
        cv2.imshow('roi', roi)
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        roi = cv2.resize(roi, (28, 28), interpolation = cv2.INTER_AREA)
    
        cv2.imshow('roi sacled and gray', roi)
        copy = frame.copy()
        cv2.rectangle(copy, (320, 100), (620, 400), (255,0,0), 5)
    
        roi = roi.reshape(1, 28, 28, 1) 

        # Frick!
        result = str(sys.model.predict(roi > 0.3)[0])
        print(result)

        cv2.putText(copy, get_letter(result), (300 , 100), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
        cv2.imshow('frame', copy)    
    
        
        if cv2.waitKey(1) == 13: #13 is the Enter Key
            break
        
        """
        num_classes = 2
        img_rows, img_cols = 28, 28
        batch_size = 32

        train_data_dir = 'C:/Users/Resu/Documents/Dev/C stuff stuff/Motion 21/Motion 21/Python/ML/custom_data/gesture_1/train'
        validation_data_dir = 'C:/Users/Resu/Documents/Dev/C stuff stuff/Motion 21/Motion 21/Python/ML/custom_data/gesture_1/test'

        train_datagen = ImageDataGenerator(
              rescale=1./255,
              rotation_range=30,
              width_shift_range=0.3,
              height_shift_range=0.3,
              horizontal_flip=True,
              fill_mode='nearest')
 
        validation_datagen = ImageDataGenerator(rescale=1./255)
 
        train_generator = train_datagen.flow_from_directory(
                train_data_dir,
                target_size=(img_rows, img_cols),
                batch_size=batch_size,
                color_mode = 'grayscale',
                class_mode='binary')
 
        validation_generator = validation_datagen.flow_from_directory(
                validation_data_dir,
                target_size=(img_rows, img_cols),
                batch_size=batch_size,
                color_mode = 'grayscale',
                class_mode='binary')

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

        print(model.summary())


        model.compile(loss = 'binary_crossentropy',
              optimizer = 'rmsprop',
              metrics = ['accuracy'])

        nb_train_samples = 1206 
        nb_validation_samples = 301 
        epochs = 10

        history = model.fit(
            train_generator,
            steps_per_epoch = nb_train_samples // batch_size,
            epochs = epochs,
            validation_data = validation_generator,
            validation_steps = nb_validation_samples // batch_size)

        model.save("my_drippy_model.h5")


        if cv2.waitKey(1) == 13: #13 is the Enter Key
            break
    """
        
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__': _main()