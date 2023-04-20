import cv2
import mediapipe
import os
from os import listdir
import shutil
import numpy as np
import matplotlib.pyplot as plot
from Utils.camera import Camera

class UserSign(object):

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(UserSign, self).__new__(self)

        return self.instance

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
        # Nonmovement Alphabet letters
        # ----------------------------------------------------------------------------------------------------------------------------------------------
        alpha_dict = {
            #pre-determined base image array for given letter (A in this case)
            "A": [(70, 166), (103, 164), (134, 140), (146, 111), (138, 91), (122, 103), (126, 79), (119, 105), (116, 116), (100, 100), (104, 79), (100, 111), 
            (99, 116), (80, 100), (82, 81), (82, 111), (82, 119), (59, 102), (62, 87), (64, 109), (65, 117)],
            "B": [(84, 185), (113, 176), (130, 145), (114, 120), (91, 114), (126, 108), (126, 76), (124, 56), (120, 38), (106, 103), (108, 67), (107, 42), 
            (106, 21), (89, 106), (90, 71), (91, 48), (91, 28), (70, 115), (71, 86), (73, 67), (73, 50)],
            "C" : [(70, 153), (92, 150), (118, 135), (138, 128), (157, 125), (100, 91), (118, 74), (136, 75), (149, 81), (91, 88), (115, 67), (135, 70), 
            (149, 80), (85, 90), (109, 68), (131, 71), (147, 79), (82, 97), (105, 81), (123, 79), (137, 81)],
            "D" : [(75, 168), (103, 163), (125, 153), (125, 130), (104, 116), (130, 103), (136, 72), (140, 51), (140, 33), (110, 97), (116, 68), (111, 95), 
            (110, 110), (91, 97), (94, 68), (93, 92), (92, 111), (71, 105), (75, 83), (79, 99), (81, 114)],
            "E" : [(56, 141), (84, 138), (106, 123), (99, 98), (76, 92), (110, 85), (120, 57), (111, 71), (104, 85), (92, 75), (101, 48), (92, 72), (88, 85), 
            (75, 71), (80, 44), (76, 65), (73, 81), (55, 76), (59, 54), (62, 66), (62, 81)],
            "F" : [(71, 167), (96, 163), (120, 153), (136, 140), (129, 129), (120, 105), (132, 89), (131, 100), (125, 114), (102, 93), (115, 65), (125, 47), 
            (133, 29), (82, 90), (83, 58), (85, 36), (88, 17), (61, 96), (52, 68), (46, 51), (43, 35)],
            "G" : [],
            "H" : [],
            "I" : [],
            "K" : [],
            "L" : [],
            "M" : [],
            "N" : [],
            "O" : [],
            "P" : [],
            "Q" : [],
            "R" : [],
            "S" : [],
            "T" : [],
            "U" : [],
            "V" : [],
            "W" : [],
            "X" : [],
            "Y" : [],
        # Movement Alphabet letters
        # ---------------------------------------------------------------------------------------------------------------------------------------------
            "J" : [],
            "Z" : [],
        }
        # pythonic'd this. idk how dict internals work but id assume its the same if not more efficient. - K
        # Returns the base array for the given letter (only non-movement for now)
        return alpha_dict[letter]

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

                Camera().frame_q.put(image)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                cv2.imshow("img", image_rgb)
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

    # Outputs the single axis data
    def show_plot(self, Z, Z_star):

        # Plots our original data points
        plot.scatter(Z[:, 0], Z[:, 1])

        # Plots our Z_stars
        plot.scatter(Z_star, np.zeros(len(Z_star)))
        
        # Outputs the plot
        plot.show()

    # Runs the comparison function between the user letter sign and the base letters
    def run_comparison(self):

        #print("it's working")
        # Checks to see if user input is matched with any of our base letters
        #matched = False

        # While loop to check through all our base letters
        # Might not be needed
        
        #return Camera().rgb_img_crop

        #while not matched:

        # Variable declarations
        # Letter only contains non-movement letters for now
        letter = ["A", "B", "C", "D", "E", "F"]#, "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y"]

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

                for i in range(len(letter)):

                    chosen_letter = letter[i]

                    base_arr = self.base_arr_function(chosen_letter)

                    base_arr = np.array(base_arr)

                    # Finds our Z_star of our base A to compare with user's Z_star
                    covarianceBase = self.compute_covariance_matrix(base_arr)
                    pcsBase, LBase = self.find_pcs(covarianceBase)
                    Z_star_base = self.project_data(base_arr, pcsBase, LBase)

                    # Finds the difference between each point to use for comparison with user letters as the distance between each z star point will be similar
                    Z_star_base_arr = []

                    for i in range(len(Z_star_base) - 1):
                        temp = Z_star_base[i] - Z_star_base[i+1]
                        Z_star_base_arr.append(temp)

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
                    count = 0

                    # Checks if user letter matches base letter
                    for i in range(len(Z_star_user_arr)):
                        temp = (Z_star_user_arr[i] / Z_star_base_arr[i]) * 100
                        #print(temp)
                        if ((temp >= 60 and temp <= 140) or (temp <= -60 and temp >= 140)): #change these values/original was 60, 140
                            count += 1

                    #STATE 0 = no hand detected, 1 = hand detected but no sign, 2 = hand detected with sign

                    # If all the points are similarly related, then the user has successfully signed the base image that we compared it to
                    if(count >= 10): #decreased to 15, can increase for similar hand signs
                        print("You have correctly signed " + chosen_letter + "!")
                        return chosen_letter
        return None
                        #break
                    #else:
                        #print("No sign detected") #Counts that matched: " + str(count))
            #else:
                #print("Full hand not detected")
        #else:
            #print("No hand detected")

    #EOF