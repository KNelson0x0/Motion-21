import cv2
import mediapipe
import os
from os import listdir
import shutil
import numpy as np
import matplotlib.pyplot as plot

#eigenvalues/eigenvector stuff

#- Research Notes for Hand ML Algorithm
#
#- Issue with our current code, when resizing window it causes it to crash (unable to find a compatible hand since its distorted)
#	- Solutions: Prevent window from distorting hand (stretching, shrinking, etc)
#		     Delete the resizing function (solution we are trying thus far)
#	
#- The 21 points when pulled and placed into a PCA algorithm returns wildly varying values based on position within the screenshot
#	- The values seem to retain a structure (similar difference between point values 1, 2, 3, etc)
#	- Solutions: We need to find a way to compare this relationship with test images and classify which letter it is most similar to

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
#pre-determined base image array for given letter (A in this case)
base_arr = [(147, 522), (282, 484), (364, 390), (408, 278), (371, 206), (301, 217), (320, 108), (329, 181), (316, 245), (228, 198), (247, 87), (263, 198),
            (250, 248), (149, 206), (163, 96), (189, 194), (183, 249), (71, 238), (87, 140), (123, 204), (127, 245)]

# Finds our Z_star of our base A to compare with user's Z_star
covarianceBase = compute_covariance_matrix(base_arr)
pcsBase, LBase = find_pcs(covarianceBase)
Z_starBase = project_data(base_arr, pcsBase, LBase)

#print(len(base_arr))

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
 
        if results.multi_hand_landmarks != None:
            for handLandmarks in results.multi_hand_landmarks:
                x_max = 0
                y_max = 0
                x_min = imageWidth
                y_min = imageHeight
                for lm in handLandmarks.landmark:
                    x, y = int(lm.x * imageWidth), int(lm.y * imageHeight)
                    if x > x_max:
                        x_max = x
                    if x < x_min:
                        x_min = x
                    if y > y_max:
                        y_max = y
                    if y < y_min:
                        y_min = y
                
                #might have to edit values based on resolution of image
                x_min -= 30
                y_min -= 30
                x_max += 30
                y_max += 30
                cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 0, 0), 2)
    
        #new downscaled image with just hand
        image = image[y_min:y_max, x_min:x_max]
        image = cv2.resize(image, (480, 640)) #works consistently when y value is greater than x
        cv2.imshow("img", image)
        results2 = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        imageHeight, imageWidth, _ = image.shape
    
        if results2.multi_hand_landmarks != None:
            for handLandmarks in results2.multi_hand_landmarks:
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

        np_coordinates = np.array(coordinates_arr)

        print(np_coordinates)

        #should be equal to the number of hand images
        print(int(np.size(np_coordinates)/2)) #need to divide by 2 since size function works weird

        #for i in range(int(np.size(np_coordinates))):
        covariance = compute_covariance_matrix(np_coordinates)
        pcs, L = find_pcs(covariance)
        Z_star = project_data(np_coordinates, pcs, L)
        print(Z_star)
        show_plot(np_coordinates, Z_star)

        # Run a relational algorithm and see if user input matches letter A
        Z_starRelation = []

        for i in Z_starBase:
            Z_starRelation[i] = Z_starBase[i]/Z_star[i]

        print(Z_starRelation)

#print(full_arr)
print(counter)
for i in range(counter):
    lower_bound = i*21
    total_diff_x = 0
    total_diff_y = 0
    for j in range(20):
        difference_x = base_arr[j][0] - full_arr[lower_bound+j][0]
        difference_y = base_arr[j][1] - full_arr[lower_bound+j][1]
        total_diff_x += abs(difference_x)
        total_diff_y += abs(difference_y)
    percent_diff_x = total_diff_x/(480)*100 #x dimension
    percent_diff_y = total_diff_y/(640)*100 #y dimension
    #print(str(percent_diff_x))
    #print(str(percent_diff_y))
    
    avg_percent_sim = round((100 - ((percent_diff_x*(480/(480+640)) + percent_diff_y*(640/(480+640))))), 2)
    if avg_percent_sim < 0:
        avg_percent_sim = 0

    if percent_diff_x <= 30 and percent_diff_y <= 30:
        print("Letter detected as A, with " + str(avg_percent_sim) + "% similarity to the base image\n")
    else:
        print("Letter not detected, with " + str(avg_percent_sim) + "% similarity to the base image\n")

#EOF