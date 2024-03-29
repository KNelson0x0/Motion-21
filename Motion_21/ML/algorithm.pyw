# algorithm.pyw: The Machine-Learning Algorithm where the majority of the calculations and classifications are computed.
#                It uses the base_letters file as our database and uses a two-step process for classification.
#                The first step is a PCA method that reduces the size of the data and simplifying the number of calculations
#                needed while the second step is comparing a user sign with our base letters. If the algorithm detects that
#                the user successfully signed a letter it will pass that information back to the GUI.

import cv2
import mediapipe
import os
from os import listdir
import shutil
import numpy as np
import matplotlib.pyplot as plot
from Utils.camera import Camera
from Utils.states import LetterState

class UserSign(object):

    #for movement letters (J and Z)
    stage = 1
    base_xy_arr1 = []
    base_xy_arr2 = []
    base_xy_arr3 = []

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(UserSign, self).__new__(self)

        return self.instance

    def reset_stage(self):
        UserSign().stage = 1

    #eigenvalues/eigenvector stuff

    # Function that calculates the covariance matrix
    def compute_covariance_matrix(self, Z):
        #print(Z)
        # Removes empty array values
        #masked_array = np.ma.masked_array(Z, mask=np.equal(Z, None))
        #Z = np.ma.compress_rows(masked_array).data
        #print(Z)

        # Uses numpy to calculate the covariance of Z
        covariance = np.cov(Z.T)

        return covariance

    # Function that calculates the PCS from the covariance matrix
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


    # Projects the data onto a single axis
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

    # Creates our base arrays
    def base_arr_function(self, letter):

        filePath = os.path.dirname(os.path.abspath(__file__)) + "\\base_letters\\" + letter + ".txt"
        #print(filePath)
        letterArray = []

        # Opens the letter file associated with the base letter that was passed
        with open(filePath, 'r') as f:

            contents = f.read().strip()
            arrays = contents.split('\n')

            for line in arrays:

                array = eval(line.strip())

                letterArray.append(array)

            # Debug print functions to show the combined base letter array
            # ------------------------------------------------------------
            #print(letterArray)
            # ------------------------------------------------------------

        # Returns the base array for the given letter
        return letterArray

    # Creates our user array
    def user_arr_function(self):

        #need to test every letter against A to see if there are any false flags

        #different groups of images (small-large, different skin colors), compare user's images to our own set
        #if a match is found, flag it

        drawingModule = mediapipe.solutions.drawing_utils
        handsModule = mediapipe.solutions.hands

        full_arr = []

        coordinates_arr = [] #array to store x,y coordinates
        #print(coordinates_arr)

        with handsModule.Hands(static_image_mode=True) as hands: #True/False
            
            #finds initial landmarks to detect just image of hand
            #image = cv2.imread(path)


            #image = Camera().rgb_img_crop
            image = Camera().get_cropped_frame()


            #cv2.imshow("img", image)
            #cv2.waitKey(0)
            results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            imageHeight, imageWidth = 0,0
            if len(image.shape) == 3:
                imageHeight, imageWidth, _ = image.shape
            else:
                imageHeight, imageWidth = image.shape
            #imageHeight, imageWidth, _ = image.shape

            #cv2.imshow("img", image)
            
            try:
                if results.multi_hand_landmarks != None:
                    for handLandmarks in results.multi_hand_landmarks:
                        for point in handsModule.HandLandmark:
        
                            drawingModule.draw_landmarks(image, handLandmarks, handsModule.HAND_CONNECTIONS)
                            #self.frame_q.put(image)

                            normalizedLandmark = handLandmarks.landmark[point]
                            pixelCoordinatesLandmark = drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, imageWidth, imageHeight)
        
                            #print(point) #name of landmark

                            #note: name of landmarks is in the same order as mediapipe framework

                            #print(str(pixelCoordinatesLandmark)) #coordinates of landmark
                            #for i in range(21):
                                #coordinates_arr[i] = pixelCoordinatesLandmark
                            coordinates_arr.append(pixelCoordinatesLandmark)

                            full_arr.append(pixelCoordinatesLandmark)
                            #print(normalizedLandmark)
                
                #need to find which function generates/stores points
                #keep in order for later reference (avoid false flagging with similar hand signs)

                #Camera().frame_q.put(image)
                #image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                #cv2.imshow("img", image_rgb)
                #Camera().rgb_img_crop = image

                #cv2.waitKey(0)

                #print(coordinates_arr) # no
                coordinates_arr = np.array(coordinates_arr)

                user_arr = coordinates_arr

                #print(user_arr)

                #should be equal to the number of hand images
                #print(int(np.size(user_arr)/2)) #need to divide by 2 since size function works weird

                return user_arr

            except:
                print("No hand detected")

    # Creates our user array
    def user_arr_xy(self):

        #need to test every letter against A to see if there are any false flags

        #different groups of images (small-large, different skin colors), compare user's images to our own set
        #if a match is found, flag it

        drawingModule = mediapipe.solutions.drawing_utils
        handsModule = mediapipe.solutions.hands

        full_arr = []
        xy_arr = []

        coordinates_arr = [] #array to store x,y coordinates
        #print(coordinates_arr)

        with handsModule.Hands(static_image_mode=True) as hands: #True/False
            
            #finds initial landmarks to detect just image of hand
            #image = cv2.imread(path)


            #image = Camera().rgb_img_crop
            #image = Camera().get_cropped_frame()
            image = Camera().get_cropped_frame()


            #cv2.imshow("img", image)
            #cv2.waitKey(0)
            results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            imageHeight, imageWidth = 0,0
            if len(image.shape) == 3:
                imageHeight, imageWidth, _ = image.shape
            else:
                imageHeight, imageWidth = image.shape
            #imageHeight, imageWidth, _ = image.shape

            #cv2.imshow("img", image)
            
            try:
                if results.multi_hand_landmarks != None:
                    for handLandmarks in results.multi_hand_landmarks:
                        for point in handsModule.HandLandmark:
        
                            drawingModule.draw_landmarks(image, handLandmarks, handsModule.HAND_CONNECTIONS)
                            #self.frame_q.put(image)

                            normalizedLandmark = handLandmarks.landmark[point]
                            pixelCoordinatesLandmark = drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, imageWidth, imageHeight)
        
                            #print(point) #name of landmark

                            #note: name of landmarks is in the same order as mediapipe framework

                            #print(str(pixelCoordinatesLandmark)) #coordinates of landmark
                            #for i in range(21):
                                #coordinates_arr[i] = pixelCoordinatesLandmark
                            coordinates_arr.append(pixelCoordinatesLandmark)

                            full_arr.append(pixelCoordinatesLandmark)
                            #print(normalizedLandmark)
                
                #need to find which function generates/stores points
                #keep in order for later reference (avoid false flagging with similar hand signs)

                #Camera().frame_q.put(image)
                #image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                #cv2.imshow("img", image_rgb)
                #Camera().rgb_img_crop = image

                #cv2.waitKey(0)

                if len(coordinates_arr)==21:
                    has_none = False

                    if None in coordinates_arr:
                        has_none = True

                    if has_none == False:
                        xy_arr.append(coordinates_arr[5])
                        xy_arr.append(coordinates_arr[6])
                        xy_arr.append(coordinates_arr[7])
                        xy_arr.append(coordinates_arr[8])

                #print(xy_arr)

                user_arr = np.array(coordinates_arr)

                #xy_arr.append(coordinates_arr[])

                #print(user_arr)

                #should be equal to the number of hand images
                #print(int(np.size(user_arr)/2)) #need to divide by 2 since size function works weird

                return user_arr, xy_arr

            except:
                print("No hand detected")

    # Outputs the single axis data
    def show_plot(self, Z, Z_star):

        # Plots our original data points
        plot.scatter(Z[:, 0], Z[:, 1])

        # Plots our Z_stars
        plot.scatter(Z_star, np.zeros(len(Z_star)))
        
        # Outputs the plot
        plot.show()

    # Runs the comparison function between the user letter sign and the base letters
    def run_comparison(self, letter):

        #REPLACE LESSON_LETTER WITH FUNCTION PARAMETER AKA GUI STUFF
        lesson_letter = letter
        #print("LESSON LETTER: " + lesson_letter)

        matched_letter = ""
        matched = False

        #print("it's working")
        # Checks to see if user input is matched with any of our base letters
        #matched = False

        # While loop to check through all our base letters
        # Might not be needed
        
        #return Camera().rgb_img_crop

        # While loop to check through all our base letters
        # Might not be needed
        #while not matched:

        # Variable declarations
        # Letter only contains non-movement letters for now
        static_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        count_dict = {"A": 16, "B": 19, "C": 16, "D": 16, "E": 16, "F": 16, "G": 15, "H": 15, "I": 15, "K": 15, "L": 15, "M": 15, "N": 15, "O": 15, "P": 15, "Q": 15, "R": 18, 
                      "S": 15, "T": 15, "U": 18, "V": 18, "W": 15, "X": 15, "Y": 15, "0": 15, "1": 15, "2": 15, "3": 15, "4": 15, "5": 15, "6": 15, "7": 15, "8": 15, "9": 15, "10": 15}
        three_stage = ["J"]
        four_stage = ["Z"]
        count_dict2 = {"J_1": 16, "J_2": 16, "J_3": 17, "Z": 15}

        if lesson_letter in static_letters:
            # Grabs user letter input
            user_arr = self.user_arr_function()
            if type(user_arr) == type(None): 
                print("user arr was none")
                return

            if len(user_arr)==21:
                #print(user_arr)

                has_none = False
                if None in user_arr:
                    has_none = True
                if has_none == False:
                    # For loop that checks through all our base letters
                    #MIGHT NEED TO ADD THIS BACK, IDK
                    #for num_letters in range(len(letter)):

                    #chosen_letter = letter[num_letters]

                    base_arr_all = self.base_arr_function(lesson_letter) #lesson_letter

                    base_arr_all = np.array(base_arr_all)

                    for num_base_letters in range(len(base_arr_all)):

                        base_arr = base_arr_all[num_base_letters]

                        print("User Calculations")

                        #for i in range(int(np.size(user_arr))):
                        covariance = self.compute_covariance_matrix(user_arr)
                        pcs, L = self.find_pcs(covariance)
                        Z_star = self.project_data(user_arr, pcs, L)
                        #print(Z_star)
                        #print(base_arr)

                        # Grabs the difference between the user's z star points and saves them to Z_star_user_arr
                        Z_star_user_arr = []

                        for i in range(len(Z_star) - 1):
                            temp = Z_star[i] - Z_star[i + 1]
                            Z_star_user_arr.append(temp)

                        # Run a relational algorithm and see if user input matches letter A
                        # (compares Z_star_base_arr with Z_star_user_arr)
                             
                        # Declare count here so it resets every base letter  
                        count = 0

                        # Debug print function to label the match percentages
                        print("Complete Match Percentage for base letter " + lesson_letter + " No. " + str(num_base_letters + 1))

                        # Checks if user letter matches base letter
                        for i in range(len(Z_star_user_arr)):
                            temp = (Z_star_user_arr[i] / base_arr[i]) * 100
                            if ((temp >= 60 and temp <= 140) or (temp <= -60 and temp >= -140)): #change these values/original was 60, 140
                                count += 1
                            #print("[{}]: {}".format(i,count))

                            # Debug print functions to label and print the match percentages per point
                            # ------------------------------------------------------------------------              
                            #print(temp)
                            # ------------------------------------------------------------------------ 

                        #STATE 0 = no hand detected, 1 = hand detected but no sign, 2 = hand detected with sign

                        if lesson_letter in count_dict:

                            # If a set number of points are similarly related, then the user has successfully signed the base image that we compared it to
                            if(count >= count_dict[lesson_letter]): #decreased to 15, can increase for similar hand signs
                                print("Counts that matched: " + str(count))
                                print(lesson_letter + " signed correctly")
                                matched = True
                                matched_letter = lesson_letter
                                print("Congratulations, you signed the letter " + lesson_letter + " correctly!")
                                return lesson_letter
                            else:
                                print("Counts that matched: " + str(count))
                                print(lesson_letter + " was not a match")

                    # If matched has been flagged, then the user has successfully signed the lesson letter and outputs a message accordingly
                    #if(matched == True and lesson_letter == matched_letter):
                        #print("Congratulations, you signed the letter " + lesson_letter + " correctly!")
                        #return lesson_letter
                    #else:
                        #matched = True
                        #print("Sorry, you did not correctly sign the letter " + lesson_letter + ", please try again!")
                        #return None
                        #break
                    #else:
                        #print("No sign detected") #Counts that matched: " + str(count))
            #else:
                #print("Full hand not detected")
        #else:
            #print("No hand detected")

        # for J
        if lesson_letter in three_stage:

            matched_letter = ""
            matched = False
            
            lesson_letter_base = lesson_letter
            lesson_letter1 = lesson_letter + "_1"
            lesson_letter2 = lesson_letter + "_2"
            lesson_letter3 = lesson_letter + "_3"

            # Grabs user letter input, will have to change to accomodate for several different images
            user_arr, xy_arr = self.user_arr_xy()

            if type(user_arr) == type(None): 
                print("user arr was none")
                return

            if len(user_arr)==21:
                #print(user_arr)
                has_none = False

                if None in user_arr:
                    has_none = True

                if has_none == False:
                    #print("poggers")
                    
                    if UserSign().stage == 1:
                        print("stage 1")

                        base_arr_all = self.base_arr_function(lesson_letter1) #lesson_letter

                        base_arr_all = np.array(base_arr_all)
                        #print(base_arr_all)

                        for num_base_letters in range(len(base_arr_all)):

                            base_arr = base_arr_all[num_base_letters]

                            #print("User Calculations")

                            #for i in range(int(np.size(user_arr))):
                            covariance = self.compute_covariance_matrix(user_arr)
                            pcs, L = self.find_pcs(covariance)
                            Z_star = self.project_data(user_arr, pcs, L)
                            #print(Z_star)
                            #print(base_arr)

                            # Grabs the difference between the user's z star points and saves them to Z_star_user_arr
                            Z_star_user_arr = []

                            for i in range(len(Z_star) - 1):
                                temp = Z_star[i] - Z_star[i + 1]
                                Z_star_user_arr.append(temp)

                            # Run a relational algorithm and see if user input matches letter A
                            # (compares Z_star_base_arr with Z_star_user_arr)
                             
                            # Declare count here so it resets every base letter  
                            count = 0

                            # Debug print function to label the match percentages
                            #print("Complete Match Percentage for base letter " + lesson_letter1 + " No. " + str(num_base_letters + 1))

                            # Checks if user letter matches base letter
                            for i in range(len(Z_star_user_arr)):
                                temp = (Z_star_user_arr[i] / base_arr[i]) * 100
                                if ((temp >= 60 and temp <= 140) or (temp <= -60 and temp >= -140)): #change these values/original was 60, 140
                                    count += 1
                                #print("[{}]: {}".format(i,count))

                                # Debug print functions to label and print the match percentages per point
                                # ------------------------------------------------------------------------              
                                #print(temp)
                                # ------------------------------------------------------------------------ 

                            #STATE 0 = no hand detected, 1 = hand detected but no sign, 2 = hand detected with sign

                            if lesson_letter1 in count_dict2:

                                # If a set number of points are similarly related, then the user has successfully signed the base image that we compared it to
                                if(count >= count_dict2[lesson_letter1]): #decreased to 15, can increase for similar hand signs
                                    #print("Counts that matched: " + str(count))
                                    print(lesson_letter + " signed correctly")
                                    #matched = True
                                    #matched_letter = lesson_letter
                                    UserSign().stage = 2
                                    return "J_1"
                                #else:
                                    #print("Counts that matched: " + str(count))
                                    #print(lesson_letter + " was not a match")

                    if UserSign().stage == 2:
                        print("stage 2")
                        
                        base_arr_all = self.base_arr_function(lesson_letter2) #lesson_letter

                        base_arr_all = np.array(base_arr_all)
                        #print(base_arr_all)

                        for num_base_letters in range(len(base_arr_all)):

                            base_arr = base_arr_all[num_base_letters]

                            #print("User Calculations")

                            #for i in range(int(np.size(user_arr))):
                            covariance = self.compute_covariance_matrix(user_arr)
                            pcs, L = self.find_pcs(covariance)
                            Z_star = self.project_data(user_arr, pcs, L)
                            #print(Z_star)
                            #print(base_arr)

                            # Grabs the difference between the user's z star points and saves them to Z_star_user_arr
                            Z_star_user_arr = []

                            for i in range(len(Z_star) - 1):
                                temp = Z_star[i] - Z_star[i + 1]
                                Z_star_user_arr.append(temp)

                            # Run a relational algorithm and see if user input matches letter A
                            # (compares Z_star_base_arr with Z_star_user_arr)
                             
                            # Declare count here so it resets every base letter  
                            count = 0

                            # Debug print function to label the match percentages
                            #print("Complete Match Percentage for base letter " + lesson_letter2 + " No. " + str(num_base_letters + 1))

                            # Checks if user letter matches base letter
                            for i in range(len(Z_star_user_arr)):
                                temp = (Z_star_user_arr[i] / base_arr[i]) * 100
                                if ((temp >= 60 and temp <= 140) or (temp <= -60 and temp >= -140)): #change these values/original was 60, 140
                                    count += 1
                                #print("[{}]: {}".format(i,count))

                                # Debug print functions to label and print the match percentages per point
                                # ------------------------------------------------------------------------              
                                #print(temp)
                                # ------------------------------------------------------------------------ 

                            #STATE 0 = no hand detected, 1 = hand detected but no sign, 2 = hand detected with sign

                            if lesson_letter2 in count_dict2:

                                # If a set number of points are similarly related, then the user has successfully signed the base image that we compared it to
                                if(count >= count_dict2[lesson_letter2]): #decreased to 15, can increase for similar hand signs
                                    #print("Counts that matched: " + str(count))
                                    print(lesson_letter + " signed correctly")
                                    #matched = True
                                    #matched_letter = lesson_letter
                                    UserSign().stage = 3
                                    return "J_2"
                                #else:
                                    #print("Counts that matched: " + str(count))
                                    #print(lesson_letter + " was not a match")
                        

                    if UserSign().stage == 3:
                        print("stage 3")

                        base_arr_all = self.base_arr_function(lesson_letter3) #lesson_letter

                        base_arr_all = np.array(base_arr_all)
                        #print(base_arr_all)

                        for num_base_letters in range(len(base_arr_all)):

                            base_arr = base_arr_all[num_base_letters]

                            #print("User Calculations")

                            #for i in range(int(np.size(user_arr))):
                            covariance = self.compute_covariance_matrix(user_arr)
                            pcs, L = self.find_pcs(covariance)
                            Z_star = self.project_data(user_arr, pcs, L)
                            #print(Z_star)
                            #print(base_arr)

                            # Grabs the difference between the user's z star points and saves them to Z_star_user_arr
                            Z_star_user_arr = []

                            for i in range(len(Z_star) - 1):
                                temp = Z_star[i] - Z_star[i + 1]
                                Z_star_user_arr.append(temp)

                            # Run a relational algorithm and see if user input matches letter A
                            # (compares Z_star_base_arr with Z_star_user_arr)
                             
                            # Declare count here so it resets every base letter  
                            count = 0

                            # Debug print function to label the match percentages
                            #print("Complete Match Percentage for base letter " + lesson_letter3 + " No. " + str(num_base_letters + 1))

                            # Checks if user letter matches base letter
                            for i in range(len(Z_star_user_arr)):
                                temp = (Z_star_user_arr[i] / base_arr[i]) * 100
                                if ((temp >= 60 and temp <= 140) or (temp <= -60 and temp >= -140)): #change these values/original was 60, 140
                                    count += 1
                                #print("[{}]: {}".format(i,count))

                                # Debug print functions to label and print the match percentages per point
                                # ------------------------------------------------------------------------              
                                #print(temp)
                                # ------------------------------------------------------------------------ 

                            #STATE 0 = no hand detected, 1 = hand detected but no sign, 2 = hand detected with sign

                            if lesson_letter3 in count_dict2:

                                # If a set number of points are similarly related, then the user has successfully signed the base image that we compared it to
                                if(count >= count_dict2[lesson_letter3]): #decreased to 15, can increase for similar hand signs
                                    #print("Counts that matched: " + str(count))
                                    print(lesson_letter + " signed correctly")
                                    matched = True
                                    matched_letter = lesson_letter_base
                                    print("Congratulations, you signed the letter " + lesson_letter_base + " correctly!")
                                    UserSign().stage = 1
                                    return lesson_letter_base
                                #else:
                                    #print("Counts that matched: " + str(count))
                                    #print(lesson_letter + " was not a match")

                        # If matched has been flagged, then the user has successfully signed the lesson letter and outputs a message accordingly
                        #if(matched == True and lesson_letter == matched_letter):
                            #print("Congratulations, you signed the letter " + lesson_letter_base + " correctly!")
                            #UserSign().stage = 1
                            #return lesson_letter_base
                        #else:
                            #matched = True
                            #print("Sorry, you did not correctly sign the letter " + lesson_letter + ", please try again!")
                            #return None
        
        #for Z                
        if lesson_letter in four_stage:

            matched_letter = ""
            matched = False

            # Grabs user letter input, will have to change to accomodate for several different images
            user_arr, xy_arr = self.user_arr_xy()

            if type(user_arr) == type(None): 
                print("user arr was none")
                return

            if len(user_arr)==21:
                #print(user_arr)
                has_none = False

                if None in user_arr:
                    has_none = True

                if has_none == False:
                    #print("poggers")
                    
                    if UserSign().stage == 1:
                        print("stage 1")

                        base_arr_all = self.base_arr_function(lesson_letter) #lesson_letter

                        base_arr_all = np.array(base_arr_all)
                        #print(base_arr_all)

                        for num_base_letters in range(len(base_arr_all)):

                            base_arr = base_arr_all[num_base_letters]

                            #print("User Calculations")

                            #for i in range(int(np.size(user_arr))):
                            covariance = self.compute_covariance_matrix(user_arr)
                            pcs, L = self.find_pcs(covariance)
                            Z_star = self.project_data(user_arr, pcs, L)
                            #print(Z_star)
                            #print(base_arr)

                            # Grabs the difference between the user's z star points and saves them to Z_star_user_arr
                            Z_star_user_arr = []

                            for i in range(len(Z_star) - 1):
                                temp = Z_star[i] - Z_star[i + 1]
                                Z_star_user_arr.append(temp)

                            # Run a relational algorithm and see if user input matches letter A
                            # (compares Z_star_base_arr with Z_star_user_arr)
                             
                            # Declare count here so it resets every base letter  
                            count = 0

                            # Debug print function to label the match percentages
                            #print("Complete Match Percentage for base letter " + lesson_letter + " No. " + str(num_base_letters + 1))

                            # Checks if user letter matches base letter
                            for i in range(len(Z_star_user_arr)):
                                temp_count = 0
                                temp = (Z_star_user_arr[i] / base_arr[i]) * 100
                                if ((temp >= 60 and temp <= 140) or (temp <= -60 and temp >= -140)): #change these values/original was 60, 140
                                    count += 1

                                #print("[{}]: {}".format(i,count))

                                # Debug print functions to label and print the match percentages per point
                                # ------------------------------------------------------------------------              
                                #print(temp)
                                # ------------------------------------------------------------------------ 

                            #STATE 0 = no hand detected, 1 = hand detected but no sign, 2 = hand detected with sign

                            if lesson_letter in count_dict2:

                                # If a set number of points are similarly related, then the user has successfully signed the base image that we compared it to
                                if(count >= count_dict2[lesson_letter]): #decreased to 15, can increase for similar hand signs
                                    print("Counts that matched: " + str(count))
                                    print(lesson_letter + " signed correctly")
                                    #matched = True
                                    #matched_letter = lesson_letter
                                    UserSign.base_xy_arr1 = xy_arr
                                    UserSign().stage = 2
                                    return "Z_1"
                                #else:
                                    #print("Counts that matched: " + str(count))
                                    #print(lesson_letter + " was not a match")

                    if UserSign().stage == 2:
                        print("stage 2")
                        
                        base_arr_all = self.base_arr_function(lesson_letter) #lesson_letter

                        base_arr_all = np.array(base_arr_all)
                        #print(base_arr_all)

                        for num_base_letters in range(len(base_arr_all)):

                            base_arr = base_arr_all[num_base_letters]

                            #print("User Calculations")

                            #for i in range(int(np.size(user_arr))):
                            covariance = self.compute_covariance_matrix(user_arr)
                            pcs, L = self.find_pcs(covariance)
                            Z_star = self.project_data(user_arr, pcs, L)
                            #print(Z_star)
                            #print(base_arr)

                            # Grabs the difference between the user's z star points and saves them to Z_star_user_arr
                            Z_star_user_arr = []

                            for i in range(len(Z_star) - 1):
                                temp = Z_star[i] - Z_star[i + 1]
                                Z_star_user_arr.append(temp)

                            # Run a relational algorithm and see if user input matches letter A
                            # (compares Z_star_base_arr with Z_star_user_arr)
                             
                            # Declare count here so it resets every base letter  
                            count = 0

                            # Debug print function to label the match percentages
                            #print("Complete Match Percentage for base letter " + lesson_letter + " No. " + str(num_base_letters + 1))

                            # Checks if user letter matches base letter
                            for i in range(len(Z_star_user_arr)):
                                temp_count = 0
                                temp = (Z_star_user_arr[i] / base_arr[i]) * 100
                                if ((temp >= 60 and temp <= 140) or (temp <= -60 and temp >= -140)): #change these values/original was 60, 140
                                    for i in range(len(xy_arr)):
                                        #print(UserSign().base_xy_arr1)
                                        #print(xy_arr)
                                        if (xy_arr[i][1] >= (UserSign().base_xy_arr1[i][1] - 30)) and (xy_arr[i][1] <= (UserSign().base_xy_arr1[i][1] + 30)): #possibly change these values for x/y coordinates
                                            #print("BOOM")
                                            if(xy_arr[i][0] > (UserSign().base_xy_arr1[i][0] + 50)): #might need to change this value too
                                                #print("BOOM")
                                                temp_count += 1
                                #print(temp_count)
                                if temp_count == 4:
                                    count += 1
                                #print("[{}]: {}".format(i,count))

                                # Debug print functions to label and print the match percentages per point
                                # ------------------------------------------------------------------------              
                                #print(temp)
                                # ------------------------------------------------------------------------ 

                            #STATE 0 = no hand detected, 1 = hand detected but no sign, 2 = hand detected with sign

                            if lesson_letter in count_dict2:

                                # If a set number of points are similarly related, then the user has successfully signed the base image that we compared it to
                                if(count >= 10): #decreased to 15, can increase for similar hand signs
                                    print("Counts that matched: " + str(count))
                                    print(lesson_letter + " signed correctly")
                                    #matched = True
                                    #matched_letter = lesson_letter
                                    UserSign().base_xy_arr2 = xy_arr
                                    UserSign().stage = 3
                                    return "Z_2"
                                #else:
                                    #print("Counts that matched: " + str(count))
                                    #print(lesson_letter + " was not a match")
                        

                    if UserSign().stage == 3:
                        print("stage 3")

                        base_arr_all = self.base_arr_function(lesson_letter) #lesson_letter

                        base_arr_all = np.array(base_arr_all)
                        #print(base_arr_all)

                        for num_base_letters in range(len(base_arr_all)):

                            base_arr = base_arr_all[num_base_letters]

                            #print("User Calculations")

                            #for i in range(int(np.size(user_arr))):
                            covariance = self.compute_covariance_matrix(user_arr)
                            pcs, L = self.find_pcs(covariance)
                            Z_star = self.project_data(user_arr, pcs, L)
                            #print(Z_star)
                            #print(base_arr)

                            # Grabs the difference between the user's z star points and saves them to Z_star_user_arr
                            Z_star_user_arr = []

                            for i in range(len(Z_star) - 1):
                                temp = Z_star[i] - Z_star[i + 1]
                                Z_star_user_arr.append(temp)

                            # Run a relational algorithm and see if user input matches letter A
                            # (compares Z_star_base_arr with Z_star_user_arr)
                             
                            # Declare count here so it resets every base letter  
                            count = 0

                            # Debug print function to label the match percentages
                            #print("Complete Match Percentage for base letter " + lesson_letter + " No. " + str(num_base_letters + 1))

                            # Checks if user letter matches base letter
                            for i in range(len(Z_star_user_arr)):
                                temp_count = 0
                                temp = (Z_star_user_arr[i] / base_arr[i]) * 100
                                if ((temp >= 60 and temp <= 140) or (temp <= -60 and temp >= -140)): #change these values/original was 60, 140
                                    for i in range(len(xy_arr)):
                                        if (xy_arr[i][0] >= (UserSign().base_xy_arr1[i][0] - 30)) and (xy_arr[i][0] <= (UserSign().base_xy_arr1[i][0] + 30)): #possibly change these values for x/y coordinates
                                            if(xy_arr[i][1] > (UserSign().base_xy_arr1[i][1] + 50)):
                                                temp_count += 1
                                if temp_count == 4:
                                    count += 1
                                #print("[{}]: {}".format(i,count))

                                # Debug print functions to label and print the match percentages per point
                                # ------------------------------------------------------------------------              
                                #print(temp)
                                # ------------------------------------------------------------------------ 

                            #STATE 0 = no hand detected, 1 = hand detected but no sign, 2 = hand detected with sign

                            if lesson_letter in count_dict2:

                                # If a set number of points are similarly related, then the user has successfully signed the base image that we compared it to
                                if(count >= 10): #decreased to 15, can increase for similar hand signs
                                    print("Counts that matched: " + str(count))
                                    print(lesson_letter + " signed correctly")
                                    #matched = True
                                    #matched_letter = lesson_letter_base
                                    UserSign().base_xy_arr3 = xy_arr
                                    UserSign().stage = 4
                                    return "Z_3"
                                #else:
                                    #print("Counts that matched: " + str(count))
                                    #print(lesson_letter + " was not a match")

                    if UserSign().stage == 4:
                        print("stage 4")

                        base_arr_all = self.base_arr_function(lesson_letter) #lesson_letter

                        base_arr_all = np.array(base_arr_all)
                        #print(base_arr_all)

                        for num_base_letters in range(len(base_arr_all)):

                            base_arr = base_arr_all[num_base_letters]

                            #print("User Calculations")

                            #for i in range(int(np.size(user_arr))):
                            covariance = self.compute_covariance_matrix(user_arr)
                            pcs, L = self.find_pcs(covariance)
                            Z_star = self.project_data(user_arr, pcs, L)
                            #print(Z_star)
                            #print(base_arr)

                            # Grabs the difference between the user's z star points and saves them to Z_star_user_arr
                            Z_star_user_arr = []

                            for i in range(len(Z_star) - 1):
                                temp = Z_star[i] - Z_star[i + 1]
                                Z_star_user_arr.append(temp)

                            # Run a relational algorithm and see if user input matches letter A
                            # (compares Z_star_base_arr with Z_star_user_arr)
                             
                            # Declare count here so it resets every base letter  
                            count = 0

                            # Debug print function to label the match percentages
                            #print("Complete Match Percentage for base letter " + lesson_letter + " No. " + str(num_base_letters + 1))

                            # Checks if user letter matches base letter
                            for i in range(len(Z_star_user_arr)):
                                temp_count = 0
                                temp = (Z_star_user_arr[i] / base_arr[i]) * 100
                                if ((temp >= 60 and temp <= 140) or (temp <= -60 and temp >= -140)): #change these values/original was 60, 140
                                    for i in range(len(xy_arr)):
                                        if (xy_arr[i][1] >= (UserSign().base_xy_arr3[i][1] - 30)) and (xy_arr[i][1] <= (UserSign().base_xy_arr3[i][1] + 30)): #possibly change these values for x/y coordinates
                                            if(xy_arr[i][0] > (UserSign().base_xy_arr3[i][0] + 50)):
                                                temp_count += 1
                                if temp_count == 4:
                                    count += 1
                                #print("[{}]: {}".format(i,count))

                                # Debug print functions to label and print the match percentages per point
                                # ------------------------------------------------------------------------              
                                #print(temp)
                                # ------------------------------------------------------------------------ 

                            #STATE 0 = no hand detected, 1 = hand detected but no sign, 2 = hand detected with sign

                            if lesson_letter in count_dict2:

                                # If a set number of points are similarly related, then the user has successfully signed the base image that we compared it to
                                if(count >= 10): #decreased to 15, can increase for similar hand signs
                                    print("Counts that matched: " + str(count))
                                    print(lesson_letter + " signed correctly")
                                    matched = True
                                    matched_letter = lesson_letter
                                    print("Congratulations, you signed the letter " + lesson_letter + " correctly!")
                                    UserSign().stage = 1
                                    return lesson_letter
                                #else:
                                    #print("Counts that matched: " + str(count))
                                    #print(lesson_letter + " was not a match")


                        # If matched has been flagged, then the user has successfully signed the lesson letter and outputs a message accordingly
                        #if(matched == True and lesson_letter == matched_letter):
                            #print("Congratulations, you signed the letter " + lesson_letter + " correctly!")
                            #UserSign().stage = 1
                            #return lesson_letter
                        #else:
                            #matched = True
                            #print("Sorry, you did not correctly sign the letter " + lesson_letter + ", please try again!")
                            #return None

    #EOF