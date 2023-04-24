import cv2
import mediapipe
import os
from os import listdir
import numpy as np
import uuid

class UserModel():

    #Allows user to put in their own hand data

    def data_collect(self, letter, take_picture, stop_data_collect):

        print("NOTE: Take care to only input data that is correct! Inputting incorrect signs can potentially break the detection system \n")

        print("Running data collect for " + letter + "...")

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT,360)
        #cap.set(10,100) #for brightness

        dir = os.path.dirname(__file__) #directory of this file
        #print(dir)
        path = dir + '\point_mapping\hand_images_' + letter
        counter = 0

        while True:

            success, img = cap.read()

            img = cv2.rectangle(img, (100,100), (300,300), (0,255,0), 2) #image, start_point, end_point, color, thickness
            crop_img = img[100:300, 100:300]

            cv2.imshow("Image", img)
            cv2.imshow("Cropped Image", crop_img)

            key = cv2.waitKey(1)

            if key == ord(take_picture):
                counter += 1
                cv2.imwrite(os.path.join(path, '{}.jpg'.format(uuid.uuid1())), crop_img)
                print(counter)

            if key == ord(stop_data_collect):
                break

        cv2.destroyAllWindows()

        print("Finished collecting data!")

    #Flips images in folder

    def flip_image(self, letter):

        print("Flipping images...")

        dir = os.path.dirname(__file__)

        directory = dir + '\point_mapping\hand_images_' + letter

        for image in os.listdir(directory):
            image_flipped_name = image.replace(".jpg", "_flipped.jpg")
            if image_flipped_name not in os.listdir(directory): #doesn't already have a flipped version
                if "flipped" not in image: #not already a flipped image (don't want to flip twice)
                    img = cv2.imread(os.path.join(directory, image))
                    img_flip = cv2.flip(img, 1) #flips image horizontally
                    cv2.imwrite(os.path.join(directory, image.replace(".jpg", "_flipped.jpg")), img_flip)

        print("Finished flipping images!")

    #ML Calculations

    def compute_covariance_matrix(self, Z):
    
        # Uses numpy to calculate the covariance of Z
        covariance = np.cov(Z.T)

        return covariance

    def find_pcs(self, cov):

        # Saves eigenvalues to L and eigenvectors to pcs
        (L, pcs) = np.linalg.eig(cov)

        # Create temp variables for moving eigenvalues and eigenvectors into largest to smallest
        tempL = L[0]
        tempPCS = pcs[0]

        # Sorts the index so it is now greatest to smallest
        # This will only work with 2D arrays      
        if(L[0] < L[1]):
            L[0] = L[1]
            L[1] = tempL

            pcs[0] = pcs[1]
            pcs[1] = tempPCS

        return pcs, L

    def project_data(self, Z, pcs, L):

        # Declaration of Z_star for manipulation
        Z_star = []

        # Grabs all the values from the first column
        data = pcs[:, 0]

        # Creates projection data and appends it to Z_star
        for i in Z:
            projection = np.dot(i, data)
            Z_star.append(projection)

        return Z_star

    #Calculates and writes in 1d arrays into base letter files

    def generate_files(self, letter):

        print("Generating files...")

        dir = os.path.dirname(__file__)

        directory = dir + '\point_mapping\hand_images_' + letter
        filePath = dir + '\\base_letters\\' + letter + '.txt'

        drawingModule = mediapipe.solutions.drawing_utils
        handsModule = mediapipe.solutions.hands

        #erases current contents
        f = open(filePath, 'w')
        f.close()

        for images in os.listdir(directory):

                coordinates_arr = [] #array to store x,y coordinates
                #print(coordinates_arr)

                if (images.endswith(".jpg")):
                    #print("\n"+ images + "\n")
                    path = os.path.join(directory, images)

                with handsModule.Hands(static_image_mode=True) as hands:
        
                    #finds initial landmarks to detect just image of hand
                    image = cv2.imread(path)
                    #cv2.imshow("img", image)
                    #cv2.waitKey(0)
                    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                    imageHeight, imageWidth, _ = image.shape

                    #cv2.imshow("img", image)
    
                    if results.multi_hand_landmarks != None:
                        for handLandmarks in results.multi_hand_landmarks:
                            for point in handsModule.HandLandmark:
    
                                drawingModule.draw_landmarks(image, handLandmarks, handsModule.HAND_CONNECTIONS)

                                normalizedLandmark = handLandmarks.landmark[point]
                                pixelCoordinatesLandmark = drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, imageWidth, imageHeight)
    
                                #print(point) #name of landmark

                                #note: name of landmarks is in the same order as mediapipe framework

                                #print(str(pixelCoordinatesLandmark)) #coordinates of landmark

                                coordinates_arr.append(pixelCoordinatesLandmark)
                                #print(normalizedLandmark)

                                base_arr = np.array(coordinates_arr)

                    #Ensures that the base_arr doesn't contain "None"
                    has_none = False

                    if None in base_arr:
                        has_none = True

                    if has_none == False:

                        covarianceBase = UserModel().compute_covariance_matrix(base_arr)
                        pcsBase, LBase = UserModel().find_pcs(covarianceBase)
                        Z_star_base = UserModel().project_data(base_arr, pcsBase, LBase)

                        Z_star_base_arr = []

                        for i in range(len(Z_star_base) - 1):
                            temp = Z_star_base[i] - Z_star_base[i+1]
                            Z_star_base_arr.append(temp)

                        #writes in 1D arrays
                        with open(filePath, 'a') as f2:
                            f2.write(str(Z_star_base_arr)+"\n")
                        f2.close()

        print("Finished generating files!")

    #Runs flip_image and generate_files

    def run_user_model(self, letter):

        print("Starting user train for " + letter + "...")

        UserModel().flip_image(letter)
        UserModel().generate_files(letter)

        print("Finished user training!")

#EOF