import cv2
import numpy as np
import os
from statistics import mean

img = cv2.imread(r"C:\Users\jason\OneDrive\Documents\GitHub\Motion-21\point_map_stuff\hand_edits\base_image.jpg") #base image, change directory to user
#cv2.imshow('image', img)
arr_i = []
arr_j = []

#i=x coordinate, j=y coordinate
for i in range(300):
    for j in range(300):
        b, g, r = img[j][i]
        if r>150:
            if b<20 and g<20:
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

#format:
    #if arr[i][0]>= and arr[i][0]<=:
        #if arr[i][1]>= and arr[i][1]<=:
            #arr_x_.append(arr[i][0])
            #arr_y_.append(arr[i][1])

#BASE DATA SET
for i in range(len(arr)):

    #62-66, 116-121
    if arr[i][0]>=62 and arr[i][0]<=66:
        if arr[i][1]>=116 and arr[i][1]<=121:
            arr_x_1.append(arr[i][0])
            arr_y_1.append(arr[i][1])

    #72-76, 67-70
    if arr[i][0]>=72 and arr[i][0]<=76:
        if arr[i][1]>=67 and arr[i][1]<=70:
            arr_x_2.append(arr[i][0])
            arr_y_2.append(arr[i][1])

    #97-101, 179-184
    if arr[i][0]>=97 and arr[i][0]<=101:
        if arr[i][1]>=179 and arr[i][1]<=184:
            arr_x_3.append(arr[i][0])
            arr_y_3.append(arr[i][1])

    #101-106, 32-37
    if arr[i][0]>=101 and arr[i][0]<=106:
        if arr[i][1]>=32 and arr[i][1]<=37:
            arr_x_4.append(arr[i][0])
            arr_y_4.append(arr[i][1])

    #105-109, 99-104
    if arr[i][0]>=105 and arr[i][0]<=109:
        if arr[i][1]>=99 and arr[i][1]<=104:
            arr_x_5.append(arr[i][0])
            arr_y_5.append(arr[i][1])

    #110-114, 89-93
    if arr[i][0]>=110 and arr[i][0]<=114:
        if arr[i][1]>=89 and arr[i][1]<=93:
            arr_x_6.append(arr[i][0])
            arr_y_6.append(arr[i][1])

    #116-120, 114-119
    if arr[i][0]>=116 and arr[i][0]<=120:
        if arr[i][1]>=114 and arr[i][1]<=119:
            arr_x_7.append(arr[i][0])
            arr_y_7.append(arr[i][1])

    #147-151, 24-29
    if arr[i][0]>=147 and arr[i][0]<=151:
        if arr[i][1]>=24 and arr[i][1]<=29:
            arr_x_8.append(arr[i][0])
            arr_y_8.append(arr[i][1])

    #148-152, 91-96
    if arr[i][0]>=148 and arr[i][0]<=152:
        if arr[i][1]>=91 and arr[i][1]<=96:
            arr_x_9.append(arr[i][0])
            arr_y_9.append(arr[i][1])

    #148-152, 109-113
    if arr[i][0]>=148 and arr[i][0]<=152:
        if arr[i][1]>=109 and arr[i][1]<=113:
            arr_x_10.append(arr[i][0])
            arr_y_10.append(arr[i][1])

    #148-152, 241-245
    if arr[i][0]>=148 and arr[i][0]<=152:
        if arr[i][1]>=241 and arr[i][1]<=245:
            arr_x_11.append(arr[i][0])
            arr_y_11.append(arr[i][1])

    #185-189, 117-121
    if arr[i][0]>=185 and arr[i][0]<=189:
        if arr[i][1]>=117 and arr[i][1]<=121:
            arr_x_12.append(arr[i][0])
            arr_y_12.append(arr[i][1])

    #189-194, 97-101
    if arr[i][0]>=189 and arr[i][0]<=194:
        if arr[i][1]>=97 and arr[i][1]<=101:
            arr_x_13.append(arr[i][0])
            arr_y_13.append(arr[i][1])

    #197-202, 34-38
    if arr[i][0]>=197 and arr[i][0]<=202:
        if arr[i][1]>=34 and arr[i][1]<=38:
            arr_x_14.append(arr[i][0])
            arr_y_14.append(arr[i][1])

    #197-201, 271-275
    if arr[i][0]>=197 and arr[i][0]<=201:
        if arr[i][1]>=271 and arr[i][1]<=275:
            arr_x_15.append(arr[i][0])
            arr_y_15.append(arr[i][1])

    #218-222, 121-125
    if arr[i][0]>=218 and arr[i][0]<=222:
        if arr[i][1]>=121 and arr[i][1]<=125:
            arr_x_16.append(arr[i][0])
            arr_y_16.append(arr[i][1])

    #224-228, 102-106
    if arr[i][0]>=224 and arr[i][0]<=228:
        if arr[i][1]>=102 and arr[i][1]<=106:
            arr_x_17.append(arr[i][0])
            arr_y_17.append(arr[i][1])

    #230-234, 111-115
    if arr[i][0]>=230 and arr[i][0]<=234:
        if arr[i][1]>=111 and arr[i][1]<=115:
            arr_x_18.append(arr[i][0])
            arr_y_18.append(arr[i][1])

    #234-239, 65-70
    if arr[i][0]>=234 and arr[i][0]<=239:
        if arr[i][1]>=65 and arr[i][1]<=70:
            arr_x_19.append(arr[i][0])
            arr_y_19.append(arr[i][1])

total_length = len(arr_x_1) + len(arr_x_2) + len(arr_x_3) + len(arr_x_4) + len(arr_x_5) + len(arr_x_6) + len(arr_x_7) + len(arr_x_8) + len(arr_x_9) + len(arr_x_10) + len(arr_x_11) + len(arr_x_12) + len(arr_x_13) + len(arr_x_14) + len(arr_x_15) + len(arr_x_16) + len(arr_x_17) + len(arr_x_18) + len(arr_x_19)
#print(total_length)

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

arr_A = np.array([[mean_x_1, mean_y_1],
               [mean_x_2, mean_y_2],
               [mean_x_3, mean_y_3],
               [mean_x_4, mean_y_4],
               [mean_x_5, mean_y_5],
               [mean_x_6, mean_y_6],
               [mean_x_7, mean_y_7],
               [mean_x_8, mean_y_8],
               [mean_x_9, mean_y_9],
               [mean_x_10, mean_y_10],
               [mean_x_11, mean_y_11],
               [mean_x_12, mean_y_12],
               [mean_x_13, mean_y_13],
               [mean_x_14, mean_y_14],
               [mean_x_15, mean_y_15],
               [mean_x_16, mean_y_16],
               [mean_x_17, mean_y_17],
               [mean_x_18, mean_y_18],
               [mean_x_19, mean_y_19]])

print("X,Y points for base image array (letter A):")
print(arr_A)
print("\n")
#print(len(arr_A))

base_counter = 0
for i in range(len(arr)):
    for j in range(len(arr_A)):
        if arr[i][0]>=(arr_A[j][0]-6) and arr[i][0]<=(arr_A[j][0]+6):
            if arr[i][1]>=(arr_A[j][1]-6) and arr[i][1]<=(arr_A[j][1]+6):
                base_counter += 1

#print(base_counter)


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
                if r>150:
                    if b<20 and g<20:
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
            for j in range(len(arr_A)):
                if arr[i][0]>=(arr_A[j][0]-6) and arr[i][0]<=(arr_A[j][0]+6):
                    if arr[i][1]>=(arr_A[j][1]-6) and arr[i][1]<=(arr_A[j][1]+6):
                        counter += 1

        #print(counter)

        similarity_to_base = round((counter/base_counter)*100, 1)

        if counter>=30:
            print("Letter detected as A")
            print("Similarity to base image is " + str(similarity_to_base) + "%\n")
        else:
            print("Letter not detected")
            print("Similarity to base image is " + str(similarity_to_base) + "%\n")

#cv2.waitKey(0)
#cv2.destroyAllWindows()

#EOF