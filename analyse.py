#analyse the cropped Images
#to be done

import cv2
import pytesseract
import numpy as np
from PIL import Image
import random
import roi_number


def countConnectedComponents(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Threshold it so it becomes binary
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    #cv2.imshow('test', thresh)

    # You need to choose 4 or 8 for connectivity type
    connectivity = 8
    # Perform the operation
    output = cv2.connectedComponentsWithStats(thresh, connectivity, cv2.CV_32S)
    # Get the results
    # The first cell is the number of labels
    num_labels = output[0]
    # The second cell is the label matrix
    labels = output[1]
    # The third cell is the stat matrix
    stats = output[2]
    # The fourth cell is the centroid matrix
    centroids = output[3]

    ###also counts the background, so -1
    #print(num_labels -1)

    count = num_labels -1
    countedComponents.append(count)


#####
countedComponents = []


image_array = []

image_array.append(cv2.imread('cropped1.tiff'))
image_array.append(cv2.imread('cropped2.tiff'))
image_array.append(cv2.imread('cropped3.tiff'))
image_array.append(cv2.imread('cropped4.tiff'))
image_array.append(cv2.imread('cropped5.tiff'))

i = 4
numberOfImages = 5

while(i < numberOfImages):
    height, width, _ = image_array[i].shape

    crop_i = []

    #img[y: y + h, x: x + w]
    '''
    cropImg_top_top = image_array[i][0:(int)(height/4), 0:width]
    cropImg_top = image_array[i][(int)(height/4):(int)(height/2), 0:width]
    cropImg_bottom = image_array[i][(int)(height / 2):(int)(height*3 / 4), 0:width]
    cropImg_bottom_bottom = image_array[i][(int)(height*3/4):height,0:width]
    '''

    ###roi
    crop_Array = []
    crop_Array = roi_number.cropNumber(image_array[i])


    countConnectedComponents(crop_Array[0])
    countConnectedComponents(crop_Array[1])
    countConnectedComponents(crop_Array[2])
    countConnectedComponents(crop_Array[3])


    cv2.imshow('test1', crop_Array[0])
    cv2.imshow('test2', crop_Array[1])
    cv2.imshow('test3', crop_Array[2])
    cv2.imshow('test4', crop_Array[3])

    #print(i)

    i = i+1

print(countedComponents)

if(countedComponents[1] == 3 and countedComponents[3] == 2):
    print(4)
elif(countedComponents[1] == 2 and countedComponents[2] == 1):
    print(5)
elif(countedComponents[1] == 1 and countedComponents[2] == 1):
    print(1)
elif (countedComponents[1] == 2 and countedComponents[2] == 2):
    print(2)
elif (countedComponents[1] == 3 and countedComponents[2] == 3):
    print(3)
else:
    randomNumb = (str)(random.randint(1, 5))
    print("random "+randomNumb)

cv2.waitKey(0)




#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#l_black = np.array([0, 0, 0])
#u_black = np.array([220, 50, 100])

#hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#mask = cv2.inRange(hsv, l_black, u_black)
#res = cv2.bitwise_and(img,img, mask=mask)


###open-closing
#kernel = np.ones((15,15),np.uint8)
#closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

#opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

#blurred = cv2.GaussianBlur(opening, (5, 5), 0)

#hsv2 = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
#mask2 = cv2.inRange(hsv2, l_black, u_black)

#cv2.imshow("imgCompl", blurred)

### pytesseract
#cv2.imwrite("fortesseract.jpg", blurred)
#A = Image.open("fortesseract.jpg")
#print(pytesseract.image_to_string(A))
###



#crop_img_oben = blurred[0:(int)(height/2), 0:width]
#crop_img_unten = blurred[(int)(height/2):height,0:width]

#crop_img = img[200:400, 100:300]
# Crop from x, y, w, h -> 100, 200, 300, 400
# NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
#cv2.imshow("cropped_1", crop_img_oben)
#cv2.imshow("cropped_2,", crop_img_unten)


#cv2.waitKey(0)