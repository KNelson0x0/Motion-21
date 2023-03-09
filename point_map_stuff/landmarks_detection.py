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
def base_arr_function(letter):

    # Nonmovement Alphabet letters
    # ----------------------------------------------------------------------------------------------------------------------------------------------

    #pre-determined base image array for given letter (A in this case)
    A = [(70, 166), (103, 164), (134, 140), (146, 111), (138, 91), (122, 103), (126, 79), (119, 105), (116, 116), (100, 100), (104, 79), (100, 111), 
         (99, 116), (80, 100), (82, 81), (82, 111), (82, 119), (59, 102), (62, 87), (64, 109), (65, 117)]
    
    B = [(84, 185), (113, 176), (130, 145), (114, 120), (91, 114), (126, 108), (126, 76), (124, 56), (120, 38), (106, 103), (108, 67), (107, 42), 
         (106, 21), (89, 106), (90, 71), (91, 48), (91, 28), (70, 115), (71, 86), (73, 67), (73, 50)]

    C = [(70, 153), (92, 150), (118, 135), (138, 128), (157, 125), (100, 91), (118, 74), (136, 75), (149, 81), (91, 88), (115, 67), (135, 70), 
          (149, 80), (85, 90), (109, 68), (131, 71), (147, 79), (82, 97), (105, 81), (123, 79), (137, 81)]

    D = [(75, 168), (103, 163), (125, 153), (125, 130), (104, 116), (130, 103), (136, 72), (140, 51), (140, 33), (110, 97), (116, 68), (111, 95), 
          (110, 110), (91, 97), (94, 68), (93, 92), (92, 111), (71, 105), (75, 83), (79, 99), (81, 114)]

    E = [(56, 141), (84, 138), (106, 123), (99, 98), (76, 92), (110, 85), (120, 57), (111, 71), (104, 85), (92, 75), (101, 48), (92, 72), (88, 85), 
         (75, 71), (80, 44), (76, 65), (73, 81), (55, 76), (59, 54), (62, 66), (62, 81)]

    F = [(71, 167), (96, 163), (120, 153), (136, 140), (129, 129), (120, 105), (132, 89), (131, 100), (125, 114), (102, 93), (115, 65), (125, 47), 
         (133, 29), (82, 90), (83, 58), (85, 36), (88, 17), (61, 96), (52, 68), (46, 51), (43, 35)]

    G = []

    H = []

    I = []

    K = []

    L = []

    M = []

    N = []

    O = []

    P = []

    Q = []

    R = []

    S = []

    T = []

    U = []

    V = []

    W = []

    X = []

    Y = []
    
    # Movement Alphabet letters
    # ----------------------------------------------------------------------------------------------------------------------------------------------

    J = []

    Z = []

    # Returns the base array for the given letter (only non-movement for now)
    if letter == "A":
        return A
    elif letter == "B":
        return B
    elif letter == "C":
        return C
    elif letter == "D":
        return D
    elif letter == "E":
        return E
    elif letter == "F":
        return F
    elif letter == "G":
        return G
    elif letter == "H":
        return H
    elif letter == "I":
        return I
    elif letter == "K":
        return K
    elif letter == "L":
        return L
    elif letter == "M":
        return M
    elif letter == "N":
        return N
    elif letter == "O":
        return O
    elif letter == "P":
        return P
    elif letter == "Q":
        return Q
    elif letter == "R":
        return R
    elif letter == "S":
        return S
    elif letter == "T":
        return T
    elif letter == "U":
        return U
    elif letter == "V":
        return V
    elif letter == "W":
        return W
    elif letter == "X":
        return X
    elif letter == "Y":
        return Y
# Creates our user array
def user_arr_function():

    #need to test every letter against A to see if there are any false flags

    #different groups of images (small-large, different skin colors), compare user's images to our own set
    #if a match is found, flag it

    for images in os.listdir(directory): #NOTE: ONLY DO ONE IMAGE

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

            #cv2.imshow("img", image)

            #cv2.waitKey(0)

            print(coordinates_arr)
            coordinates_arr = np.array(coordinates_arr)

            user_arr = coordinates_arr

            #print(user_arr)

            #should be equal to the number of hand images
            #print(int(np.size(user_arr)/2)) #need to divide by 2 since size function works weird

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
directory = r"C:\Users\jason\OneDrive\Documents\GitHub\Motion-21\hand_images" #change path to user's directory
directory2 = r"C:\Users\jason\OneDrive\Documents\GitHub\Motion-21\hand_edits" #change path to user's directory
 
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
    # Letter only contains non-movement letters for now
    letter = ["A", "B"] #, "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y"]

    # Grabs user letter input
    user_arr = user_arr_function()

    # For loop that checks through all our base letters
    for num_letters in range(len(letter)):

        chosen_letter = letter[num_letters]

        base_arr = base_arr_function(chosen_letter)

        base_arr = np.array(base_arr)

        # Finds our Z_star of our base A to compare with user's Z_star
        covarianceBase = compute_covariance_matrix(base_arr)
        pcsBase, LBase = find_pcs(covarianceBase)
        Z_star_base = project_data(base_arr, pcsBase, LBase)

        # Finds the difference between each point to use for comparison with user letters as the distance between each z star point will be similar
        Z_star_base_arr = []

        for i in range(len(Z_star_base) - 1):
            temp = Z_star_base[i] - Z_star_base[i+1]
            Z_star_base_arr.append(temp)

        #for i in range(int(np.size(user_arr))):
        covariance = compute_covariance_matrix(user_arr)
        pcs, L = find_pcs(covariance)
        Z_star = project_data(user_arr, pcs, L)

        # Grabs the difference between the user's z star points and saves them to Z_star_user_arr
        Z_star_user_arr = []

        for i in range(len(Z_star) - 1):
            temp = Z_star[i] - Z_star[i + 1]
            Z_star_user_arr.append(temp)

        print("User Calculations")
        print("Base Letter 2D Hand Map Array")
        print(base_arr)
        print("Base Letter 1D Z-star Array")
        print(Z_star)
        print("User 1D Point Relationship Array")
        print(Z_star_user_arr)

        print("Letter " + chosen_letter + " Calculations")
        print("Letter " + chosen_letter + " 1D Point Relationship Array")
        print(Z_star_base_arr)
        

        # Run a relational algorithm and see if user input matches letter A
        # (compares Z_star_base_arr with Z_star_user_arr)
        count = 0

        print("Complete Match Percentage")

        # Checks if user letter matches base letter
        for i in range(len(Z_star_user_arr)):
            temp = (Z_star_user_arr[i] / Z_star_base_arr[i]) * 100
            print(temp)
            if ((temp >= 60 and temp <= 140) or (temp <= -60 and temp >= -140)): #change these values
                count += 1

        # If all the points are similarly related, then the user has successfully signed the base image that we compared it to
        if(count >= 15): #decreased to 15, can increase for similar hand signs
            print("You have correctly signed " + chosen_letter + "!")
            matched = True
            break
        else:
            print("Counts that matched: " + str(count))

    show_plot(user_arr, Z_star)
    matched = True

#EOF