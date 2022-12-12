import cv2
import mediapipe
import os
from os import listdir
import shutil

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
#print(len(base_arr))

for images in os.listdir(directory):
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
 
                    print(point)
                    print(str(pixelCoordinatesLandmark))
                    
                    full_arr.append(pixelCoordinatesLandmark)

                    #print(normalizedLandmark)
        
        path2 = os.path.join(directory2, images)
        cv2.imwrite(path2, image)

        counter += 1
        #cv2.imshow("img", image)

        #cv2.waitKey(0)

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