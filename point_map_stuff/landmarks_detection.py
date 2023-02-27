import cv2
import mediapipe
import os
from os import listdir
import shutil
import numpy as np
import matplotlib.pyplot as plot

#eigenvalues/eigenvector stuff

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

# Creates our base arrays
def base_arr_function(base_arr, letter):
    #pre-determined base image array for given letter (A in this case)
    A = [(147, 522), (282, 484), (364, 390), (408, 278), (371, 206), (301, 217), (320, 108), (329, 181), (316, 245), (228, 198), (247, 87), (263, 198),
                (250, 248), (149, 206), (163, 96), (189, 194), (183, 249), (71, 238), (87, 140), (123, 204), (127, 245)]
    
    B = [(81, 170), (107, 166), (124, 141), (108, 117), (85, 112), (123, 106), (126, 78), (125, 60), (123, 43), (107, 99), (109, 66), (110, 43), (109, 23),
             (91, 100), (93, 68), (94, 46), (94, 28), (74, 108), (75, 82), (77, 65), (77, 49)]
    
    # Returns the base array for the given letter
    if letter == "A":
        return A
    elif letter == "B":
        return B
    
# Creates our user array
def user_arr_function():

    #need to test every letter against A to see if there are any false flags

    #different groups of images (small-large, different skin colors), compare user's images to our own set
    #if a match is found, flag it

    for images in os.listdir(directory):

        coordinates_arr = [] #array to store x,y coordinates
        #print(coordinates_arr)

        if (images.endswith(".jpg")):
            print("\n"+ images + "\n")
            path = os.path.join(directory, images)

        with handsModule.Hands(static_image_mode=True) as hands:
        
            #finds initial landmarks to detect just image of hand
            image = cv2.imread(path)
            #cv2.imshow("img", image)
            #cv2.waitKey(0)
            results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            imageHeight, imageWidth, _ = image.shape

            cv2.imshow("img", image)
    
            if results.multi_hand_landmarks != None:
                for handLandmarks in results.multi_hand_landmarks:
                    for point in handsModule.HandLandmark:
    
                        drawingModule.draw_landmarks(image, handLandmarks, handsModule.HAND_CONNECTIONS)

                        normalizedLandmark = handLandmarks.landmark[point]
                        pixelCoordinatesLandmark = drawingModule._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, imageWidth, imageHeight)
    
                        print(point) #name of landmark

                        #note: name of landmarks is in the same order as mediapipe framework

                        print(str(pixelCoordinatesLandmark)) #coordinates of landmark
                        #for i in range(21):
                            #coordinates_arr[i] = pixelCoordinatesLandmark
                        coordinates_arr.append(pixelCoordinatesLandmark)

                        
                        full_arr.append(pixelCoordinatesLandmark)
                        #print(normalizedLandmark)
            
            #need to find which function generates/stores points
            #keep in order for later reference (avoid false flagging with similar hand signs)

            path2 = os.path.join(directory2, images)
            cv2.imwrite(path2, image)

            counter += 1

            #cv2.imshow("img", image)

            #cv2.waitKey(0)

            print(coordinates_arr)

            user_arr = np.array(coordinates_arr)

            print(user_arr)

            #should be equal to the number of hand images
            print(int(np.size(user_arr)/2)) #need to divide by 2 since size function works weird

            return user_arr

# Outputs the single axis data
def show_plot(Z, Z_star):

    # Plots our original data points
    plot.scatter(Z[:, 0], Z[:, 1])

    # Plots our Z_stars
    plot.scatter(Z_star, np.zeros(len(Z_star)))
    
    # Outputs the plot
    plot.show()

if os.path.exists('hand_edits'):
    shutil.rmtree('hand_edits')
os.mkdir('hand_edits')

#Get directory
directory = r"C:\Users\pccin\source\repos\point_map_stuff\point_map_stuff\hand_images" #change path to user's directory
directory2 = r"C:\Users\pccin\source\repos\point_map_stuff\point_map_stuff\hand_edits" #change path to user's directory
 
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

counter = 0
full_arr = []

# Checks to see if user input is matched with any of our base letters
matched = False

# While loop to check through all our base letters
# Might not be needed
while not matched:

    # Variable declarations
    letter = ["A", "B"]

    # Grabs user letter input
    user_arr = user_arr_function()

    # For loop that checks through all our base letters
    for i in len(letter):

        chosen_letter = letter[i]

        base_arr = base_arr_function(base_arr, chosen_letter)

        base_arr = np.array(base_arr)

        # Finds our Z_star of our base A to compare with user's Z_star
        covarianceBase = compute_covariance_matrix(base_arr)
        pcsBase, LBase = find_pcs(covarianceBase)
        Z_star_base = project_data(base_arr, pcsBase, LBase)

        # Finds the difference between each point to use for comparison with user letters as the distance between each z star point will be similar
        Z_star_base_arr = []

        for i in range(len(Z_star_base - 1)):
            temp = Z_star_base[i] - Z_star_base[i+1]
            Z_star_base_arr.append(temp)

        #for i in range(int(np.size(user_arr))):
        covariance = compute_covariance_matrix(user_arr)
        pcs, L = find_pcs(covariance)
        Z_star = project_data(user_arr, pcs, L)
        print(Z_star)
        show_plot(user_arr, Z_star)

        # Grabs the difference between the user's z star points and saves them to Z_star_user_arr
        Z_star_user_arr = []

        for i in range(len(Z_star - 1)):
            temp = Z_star[i] - Z_star[i + 1]
            Z_star_user_arr.append(temp)

        # Run a relational algorithm and see if user input matches letter A
        # (compares Z_star_base_arr with Z_star_user_arr)
        count = 0

        # Checks if user letter matches base letter
        for i in range(len(Z_star_user_arr)):
            temp = (Z_star_user_arr[i] / Z_star_base_arr[i]) * 100
            if ((temp >= 60 and temp <= 140) or (temp >= -60 and temp <= -140)): #change these values
                count += 1

        # If all the points are similarly related, then the user has successfully signed the base image that we compared it to
        if(count >= 15): #decreased to 15, can increase for similar hand signs
            print("You have correctly signed " + chosen_letter + "!")
        else:
            print("Counts that matched: " + str(count))

        print("Z Star base array")
        print(Z_star_base_arr)
        print("Z Star user array")
        print(Z_star_user_arr)
        print("Z star array")
        print(Z_star)
        show_plot(user_arr, Z_star)
        for i in range(len(Z_star_user_arr)):
            temp = (Z_star_user_arr[i] / Z_star_base_arr[i]) * 100
            if ((75 >= temp and temp <= 125) or (-125 >= temp and temp <= -75)):
                count += 1

        # If all the points are similarly related, then the user has successfully signed the base image that we compared it to
        if(count == 20):
            print("You have correctly signed A!")
            #Put whatever we want in here to trigger that
        else:
            print("Counts that matched: " + count)

#EOF