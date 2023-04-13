#currently not in use, changes image to black and white

#from PIL import Image
import cv2
import numpy as np
import matplotlib.image as mat

img = cv2.imread(r"C:\Users\pccin\source\repos\point_map_stuff\point_map_stuff\hand_images\b4222d1e-752d-11ed-9cfe-98bb1e1c8ac8.jpg")

#cv2.imshow("original image", img)
n = 128
new_dim = (n, n) #changes dimensions
img_resize = cv2.resize(img, new_dim, interpolation = cv2.INTER_AREA)
cv2.imshow("resized image", img_resize)

arr_i = []
arr_j = []

#i=x coordinate, j=y coordinate
for i in range(n):
    for j in range(n):
        b, g, r = img_resize[j][i]
        if r>200:
            if b<10 and g<10:
                img_resize[j][i] = [255, 255, 255]
                arr_i.append(i)
                arr_j.append(j)
            else:
                img_resize[j][i] = [0, 0, 0]
        else:
            img_resize[j][i] = [0, 0, 0]

print(arr_i)
print(arr_j)

cv2.imshow("new image", img_resize)

cv2.waitKey(0)