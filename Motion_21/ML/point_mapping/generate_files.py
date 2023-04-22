import cv2
import mediapipe
import os
from os import listdir
import shutil
import numpy as np
import matplotlib.pyplot as plot

class GenerateFiles:
    # Function that calculates the covariance matrix
    def compute_covariance_matrix(Z):
    
        # Uses numpy to calculate the covariance of Z
        covariance = np.cov(Z.T)

        return covariance

    # Function that calculates the PCS from the covariance matrix
    def find_pcs(cov):

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
    def project_data(Z, pcs, L):

        # Declaration of Z_star for manipulation
        Z_star = []

        # Grabs all the values from the first column
        data = pcs[:, 0]

        # Creates projection data and appends it to Z_star
        for i in Z:
            projection = np.dot(i, data)
            Z_star.append(projection)

        return Z_star

    ##################### CHANGE THIS FOR DIFFERENT LETTERS #########################
    control_letter = 'J_3'

    letter = control_letter
    letter_pca = letter + '_relation'

    dir = os.path.dirname(__file__)
    directory = dir + '\hand_images_' + letter
    #directory2 = r"C:\Users\pccin\source\repos\point_map_stuff\point_map_stuff\hand_edits" #change path to user's directory
    #filePath1 = os.path.dirname(os.path.abspath(__file__)) + "\\base_letters\\" + letter + ".txt"
    #filePath2 = os.path.dirname(os.path.abspath(__file__)) + "\\base_letters\\" + letter_pca + ".txt"
    filePath2 = r"C:\Users\pccin\OneDrive\Documents\Motion_21_Github\Motion_21\ML\base_letters\\" + letter + ".txt"
 
    drawingModule = mediapipe.solutions.drawing_utils
    handsModule = mediapipe.solutions.hands

    counter = 0
    full_arr = []

    #erases current contents
    f = open(filePath2, 'w')
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
                            #for i in range(21):
                                #coordinates_arr[i] = pixelCoordinatesLandmark
                            coordinates_arr.append(pixelCoordinatesLandmark)

                        
                            full_arr.append(pixelCoordinatesLandmark)
                            #print(normalizedLandmark)

                            base_arr = np.array(coordinates_arr)
            
                #need to find which function generates/stores points
                #keep in order for later reference (avoid false flagging with similar hand signs)

                #WRITES TO HAND EDITS FOLDER, might not be needed
                #path2 = os.path.join(directory2, images)
                #cv2.imwrite(path2, image)

                #cv2.imshow("img", image)

                #cv2.waitKey(0)

                #print(coordinates_arr)

                #writes in 2D coordinate arrays (might not be needed)
                #with open(filePath1, 'a') as f1:
                #    f1.write(str(coordinates_arr)+"\n")
                #f1.close()

                covarianceBase = compute_covariance_matrix(base_arr)
                pcsBase, LBase = find_pcs(covarianceBase)
                Z_star_base = project_data(base_arr, pcsBase, LBase)

                Z_star_base_arr = []

                for i in range(len(Z_star_base) - 1):
                    temp = Z_star_base[i] - Z_star_base[i+1]
                    Z_star_base_arr.append(temp)

                #writes in 1D arrays
                with open(filePath2, 'a') as f2:
                    f2.write(str(Z_star_base_arr)+"\n")
                f2.close()

                ###### FOR TESTING STUFF ######
                #letterArray = []
                #with open(filePath2, 'r') as f:

                    #contents = f.read().strip()
                    #arrays = contents.split('\n')

                    #for line in arrays:

                        #array = eval(line.strip())

                        #letterArray.append(array)
            
                #print(letterArray)