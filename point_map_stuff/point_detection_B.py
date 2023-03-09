import cv2
import numpy as np
import os
from statistics import mean

img = cv2.imread(r"C:\Users\jason\OneDrive\Documents\GitHub\Motion-21\point_map_stuff\base_images\base_image_B.jpg") #base image, change directory to user
#cv2.imshow('image', img)
arr_i = []
arr_j = []

#i=x coordinate, j=y coordinate
for i in range(300):
    for j in range(300):
        b, g, r = img[j][i]
        if r>130:
            if b<40 and g<40:
                #print(i, j)
                #print(b, g, r)
                #print("\n")
                arr_i.append(i)
                arr_j.append(j)

#print(arr_i)
#print(arr_j)
#print(len(arr_i))
arr = np.empty(shape=(len(arr_i), 2))
for n in range(len(arr_i)):
    arr[n][0] = arr_i[n]
    arr[n][1] = arr_j[n]

#print(arr)
print("Length of initial array: " + str(len(arr)) + "\n")

#arrays for each point
arr_x_1 = []
arr_y_1 = []
arr_x_2 = []
arr_y_2 = []
arr_x_3 = []
arr_y_3 = []
arr_x_4 = []
arr_y_4 = []
arr_x_5 = []
arr_y_5 = []
arr_x_6 = []
arr_y_6 = []
arr_x_7 = []
arr_y_7 = []
arr_x_8 = []
arr_y_8 = []
arr_x_9 = []
arr_y_9 = []
arr_x_10 = []
arr_y_10 = []
arr_x_11 = []
arr_y_11 = []
arr_x_12 = []
arr_y_12 = []
arr_x_13 = []
arr_y_13 = []
arr_x_14 = []
arr_y_14 = []
arr_x_15 = []
arr_y_15 = []
arr_x_16 = []
arr_y_16 = []
arr_x_17 = []
arr_y_17 = []
arr_x_18 = []
arr_y_18 = []
arr_x_19 = []
arr_y_19 = []
arr_x_20 = []
arr_y_20 = []
arr_x_21 = []
arr_y_21 = []

#format:
    #if arr[i][0]>= and arr[i][0]<=:
        #if arr[i][1]>= and arr[i][1]<=:
            #arr_x_.append(arr[i][0])
            #arr_y_.append(arr[i][1])

#BASE DATA SET FOR A
for i in range(len(arr)):

#110-113, 115-117 
    if arr[i][0]>=110 and arr[i][0]<=113:
        if arr[i][1]>=115 and arr[i][1]<=117:
            arr_x_1.append(arr[i][0])
            arr_y_1.append(arr[i][1])


#111-113, 157-159
    if arr[i][0]>=111 and arr[i][0]<=113:
        if arr[i][1]>=157 and arr[i][1]<=159:
            arr_x_2.append(arr[i][0])
            arr_y_2.append(arr[i][1])

#113-115, 86-89
    if arr[i][0]>=113 and arr[i][0]<=115:
        if arr[i][1]>=86 and arr[i][1]<=89:
            arr_x_3.append(arr[i][0])
            arr_y_3.append(arr[i][1])

#116-117, 62
    if arr[i][0]>=116 and arr[i][0]<=117:
        if arr[i][1]>=62 and arr[i][1]<=62:
            arr_x_4.append(arr[i][0])
            arr_y_4.append(arr[i][1])

#125-127, 158-161
    if arr[i][0]>=125 and arr[i][0]<=127:
        if arr[i][1]>=158 and arr[i][1]<=161:
            arr_x_5.append(arr[i][0])
            arr_y_5.append(arr[i][1])

#132-135, 281-283
    if arr[i][0]>=132 and arr[i][0]<=135:
        if arr[i][1]>=281 and arr[i][1]<=283:
            arr_x_6.append(arr[i][0])
            arr_y_6.append(arr[i][1])

#134-137, 144-146
    if arr[i][0]>=134 and arr[i][0]<=137:
        if arr[i][1]>=144 and arr[i][1]<=146:
            arr_x_7.append(arr[i][0])
            arr_y_7.append(arr[i][1])

#138-141, 90-93
    if arr[i][0]>=138 and arr[i][0]<=141:
        if arr[i][1]>=90 and arr[i][1]<=93:
            arr_x_8.append(arr[i][0])
            arr_y_8.append(arr[i][1])

#142-145, 54-57
    if arr[i][0]>=142 and arr[i][0]<=145:
        if arr[i][1]>=54 and arr[i][1]<=57:
            arr_x_9.append(arr[i][0])
            arr_y_9.append(arr[i][1])

#144-145, 28-30
    if arr[i][0]>=144 and arr[i][0]<=145:
        if arr[i][1]>=28 and arr[i][1]<=30:
            arr_x_10.append(arr[i][0])
            arr_y_10.append(arr[i][1])

#157-159, 167-169
    if arr[i][0]>=157 and arr[i][0]<=159:
        if arr[i][1]>=167 and arr[i][1]<=169:
            arr_x_11.append(arr[i][0])
            arr_y_11.append(arr[i][1])

#158-160, 140-143
    if arr[i][0]>=158 and arr[i][0]<=160:
        if arr[i][1]>=140 and arr[i][1]<=143:
            arr_x_12.append(arr[i][0])
            arr_y_12.append(arr[i][1])

#164-166, 85-87
    if arr[i][0]>=164 and arr[i][0]<=166:
        if arr[i][1]>=85 and arr[i][1]<=87:
            arr_x_13.append(arr[i][0])
            arr_y_13.append(arr[i][1])

#165-167, 48-49
    if arr[i][0]>=165 and arr[i][0]<=167:
        if arr[i][1]>=48 and arr[i][1]<=49:
            arr_x_14.append(arr[i][0])
            arr_y_14.append(arr[i][1])

#166-167, 16-17
    if arr[i][0]>=166 and arr[i][0]<=167:
        if arr[i][1]>=16 and arr[i][1]<=17:
            arr_x_15.append(arr[i][0])
            arr_y_15.append(arr[i][1])

#166-167, 257-259
    if arr[i][0]>=166 and arr[i][0]<=167:
        if arr[i][1]>=257 and arr[i][1]<=259:
            arr_x_16.append(arr[i][0])
            arr_y_16.append(arr[i][1])

#182-185, 149-151
    if arr[i][0]>=182 and arr[i][0]<=185:
        if arr[i][1]>=149 and arr[i][1]<=151:
            arr_x_17.append(arr[i][0])
            arr_y_17.append(arr[i][1])

#183-185, 46-48
    if arr[i][0]>=183 and arr[i][0]<=185:
        if arr[i][1]>=46 and arr[i][1]<=48:
            arr_x_18.append(arr[i][0])
            arr_y_18.append(arr[i][1])

#184-187, 207-209
    if arr[i][0]>=184 and arr[i][0]<=187:
        if arr[i][1]>=207 and arr[i][1]<=209:
            arr_x_19.append(arr[i][0])
            arr_y_19.append(arr[i][1])

#186-189, 72-73
    if arr[i][0]>=186 and arr[i][0]<=189:
        if arr[i][1]>=72 and arr[i][1]<=73:
            arr_x_20.append(arr[i][0])
            arr_y_20.append(arr[i][1])

#188-191, 101-104
    if arr[i][0]>=188 and arr[i][0]<=191:
        if arr[i][1]>=101 and arr[i][1]<=104:
            arr_x_21.append(arr[i][0])
            arr_y_21.append(arr[i][1])

total_length = len(arr_x_1) + len(arr_x_2) + len(arr_x_3) + len(arr_x_4) + len(arr_x_5) + len(arr_x_6) + len(arr_x_7) + len(arr_x_8) + len(arr_x_9) + len(arr_x_10) + len(arr_x_11) + len(arr_x_12) + len(arr_x_13) + len(arr_x_14) + len(arr_x_15) + len(arr_x_16) + len(arr_x_17) + len(arr_x_18) + len(arr_x_19) + len(arr_x_20) + len(arr_x_21)
print("Total length of parsed array (should be the same as first number): " + str(total_length) + "\n")

mean_x_1 = round(mean(arr_x_1), 2)
mean_y_1 = round(mean(arr_y_1), 2)
mean_x_2 = round(mean(arr_x_2), 2)
mean_y_2 = round(mean(arr_y_2), 2)
mean_x_3 = round(mean(arr_x_3), 2)
mean_y_3 = round(mean(arr_y_3), 2)
mean_x_4 = round(mean(arr_x_4), 2)
mean_y_4 = round(mean(arr_y_4), 2)
mean_x_5 = round(mean(arr_x_5), 2)
mean_y_5 = round(mean(arr_y_5), 2)
mean_x_6 = round(mean(arr_x_6), 2)
mean_y_6 = round(mean(arr_y_6), 2)
mean_x_7 = round(mean(arr_x_7), 2)
mean_y_7 = round(mean(arr_y_7), 2)
mean_x_8 = round(mean(arr_x_8), 2)
mean_y_8 = round(mean(arr_y_8), 2)
mean_x_9 = round(mean(arr_x_9), 2)
mean_y_9 = round(mean(arr_y_9), 2)
mean_x_10 = round(mean(arr_x_10), 2)
mean_y_10 = round(mean(arr_y_10), 2)
mean_x_11 = round(mean(arr_x_11), 2)
mean_y_11 = round(mean(arr_y_11), 2)
mean_x_12 = round(mean(arr_x_12), 2)
mean_y_12 = round(mean(arr_y_12), 2)
mean_x_13 = round(mean(arr_x_13), 2)
mean_y_13 = round(mean(arr_y_13), 2)
mean_x_14 = round(mean(arr_x_14), 2)
mean_y_14 = round(mean(arr_y_14), 2)
mean_x_15 = round(mean(arr_x_15), 2)
mean_y_15 = round(mean(arr_y_15), 2)
mean_x_16 = round(mean(arr_x_16), 2)
mean_y_16 = round(mean(arr_y_16), 2)
mean_x_17 = round(mean(arr_x_17), 2)
mean_y_17 = round(mean(arr_y_17), 2)
mean_x_18 = round(mean(arr_x_18), 2)
mean_y_18 = round(mean(arr_y_18), 2)
mean_x_19 = round(mean(arr_x_19), 2)
mean_y_19 = round(mean(arr_y_19), 2)
mean_x_20 = round(mean(arr_x_20), 2)
mean_y_20 = round(mean(arr_y_20), 2)
mean_x_21 = round(mean(arr_x_21), 2)
mean_y_21 = round(mean(arr_y_21), 2)

#with landmark numbers
arr_B = np.array([[mean_x_1, mean_y_1],  #18
               [mean_x_2, mean_y_2],     #17
               [mean_x_3, mean_y_3],     #19
               [mean_x_4, mean_y_4],     #20
               [mean_x_5, mean_y_5],     #4
               [mean_x_6, mean_y_6],     #0
               [mean_x_7, mean_y_7],     #13
               [mean_x_8, mean_y_8],     #14
               [mean_x_9, mean_y_9],     #15
               [mean_x_10, mean_y_10],   #16
               [mean_x_11, mean_y_11],   #3
               [mean_x_12, mean_y_12],   #9
               [mean_x_13, mean_y_13],   #10
               [mean_x_14, mean_y_14],   #11
               [mean_x_15, mean_y_15],   #12
               [mean_x_16, mean_y_16],   #1
               [mean_x_17, mean_y_17],   #5
               [mean_x_18, mean_y_18],   #8
               [mean_x_19, mean_y_19],   #2
               [mean_x_20, mean_y_20],   #76
               [mean_x_21, mean_y_21]])  #6

print("X,Y points for base image array (letter B):")
print(arr_B)
print("\n")
print("Number of Hand Landmarks: " + str(len(arr_B)) +"\n")

base_counter = 0
for i in range(len(arr)):
    for j in range(len(arr_B)):
        if arr[i][0]>=(arr_B[j][0]-4) and arr[i][0]<=(arr_B[j][0]+4):
            if arr[i][1]>=(arr_B[j][1]-4) and arr[i][1]<=(arr_B[j][1]+4):
                base_counter += 1

print("Points matched from base image (should be same as first number): " + str(base_counter) + "\n")


directory = r"C:\Users\pccin\source\repos\point_map_stuff\point_map_stuff\hand_edits" #change path to user's directory
for images in os.listdir(directory):
    if (images.endswith(".jpg") and images!="base_image.jpg"):
        print("Name of image: " + images)
        path = os.path.join(directory, images)
        img = cv2.imread(path)
        #cv2.imshow('image', img)
        arr_i = []
        arr_j = []

        #i=x coordinate, j=y coordinate
        for i in range(300):
            for j in range(300):
                b, g, r = img[j][i]
                if r>130:
                    if b<40 and g<40:
                        #print(i, j)
                        #print(b, g, r)
                        #print("\n")
                        arr_i.append(i)
                        arr_j.append(j)

        #print(arr_i)
        #print(arr_j)
        #print(len(arr_i))
        arr = np.empty(shape=(len(arr_i), 2))
        for n in range(len(arr_i)):
            arr[n][0] = arr_i[n]
            arr[n][1] = arr_j[n]

        counter = 0

        for i in range(len(arr)):
            for j in range(len(arr_B)):
                if arr[i][0]>=(arr_B[j][0]-3) and arr[i][0]<=(arr_B[j][0]+3):
                    if arr[i][1]>=(arr_B[j][1]-3) and arr[i][1]<=(arr_B[j][1]+3):
                        counter += 1

        print(counter)

        similarity_to_base = round((counter/base_counter)*100, 1)

        if counter>=30:
            print("Letter detected as B")
            print("Similarity to base image is " + str(similarity_to_base) + "%\n")
        else:
            print("Letter not detected")
            print("Similarity to base image is " + str(similarity_to_base) + "%\n")

#cv2.waitKey(0)
#cv2.destroyAllWindows()

#EOF