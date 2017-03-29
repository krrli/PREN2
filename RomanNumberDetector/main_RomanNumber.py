#OpenCV3
#07.03.17
#main

import os, os.path
import time
import cv2
import numpy as np

from RomanNumberDetector import crop, analyse

'''
#call: python main_RomanNumber.py 1
# 0 for first camera | 1 for second camera

whichCamera = sys.argv[1]

if(whichCamera != ''):
    camera = cv2.VideoCapture(whichCamera)

else:
    #Change to 1 for USB Cam
    camera = cv2.VideoCapture(0)
'''

############################################
# CAPTURE 5 Pictures
############################################

#Change to 0 for USB Cam
cap = cv2.VideoCapture(0)

hasCharacterBeenEvaluated = False
RomanPictures = []
CharacterEval = [0]*100

i = 1

#Timeout
timeout = 2
timeLeft = 0
timeStored = 0
timeOutSet = 0
#

while(True):

    if(timeStored == 1 and timeOutSet == 1 and time.time() > timeLeft):
        break

    # Capture frame-by-frame
    ret, frame = cap.read()

    if not hasCharacterBeenEvaluated:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # define range of blue color in HSV

        #lower_red = np.array([170, 100, 100])
        #upper_red = np.array([180, 255, 255])

        #mask = cv2.inRange(hsv, lower_red, upper_red)

        # lower mask (0-10)
        lower_red = np.array([0, 100, 10])
        upper_red = np.array([10, 255, 255])
        mask0 = cv2.inRange(hsv, lower_red, upper_red)

        # upper mask (170-180)
        lower_red = np.array([170, 100, 100])
        upper_red = np.array([179, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)

        # Combine Masks
        mask = mask0 + mask1
        red_hue_image = cv2.addWeighted(mask0, 1.0, mask1, 1.0, 0.0)
        test = cv2.GaussianBlur(red_hue_image, (9,9), 0)
        #test = cv2.GaussianBlur(mask, (9,9), 0)

        # Get Contours
        _, contours, hierarchy = cv2.findContours(test, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        barCount = 0

        # cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
        rectangleList = []

        # Loop Through Found contours
        for foundRectangle in contours:
            if barCount <= 2:
                approxDistance = cv2.arcLength(foundRectangle,True) * 0.02

                approxCurve = cv2.approxPolyDP(foundRectangle, approxDistance, True)

                # Only look for rectangles
                if len(approxCurve) == 4:
                    rect = cv2.boundingRect(approxCurve)
                    # Only save Rectangles with height of 150+
                    if rect[3] >= 100:
                        rectangleList.append(rect)
                        barCount += 1

        # Only if exactly 2 Red bars were found, save them to the Picture array
        if barCount == 2:

            ####TODO
            ####Stop Rover 1 Second and take so many Pictures as possible
            #####Stop Rover 1 second

            if(timeStored == 0):
                timeLeft = time.time() + timeout
                timeStored = 1

            print('found')

            if (i == 1):
                cv2.imwrite("./RomanNumberDetector/numbers/romannumber1.tiff", frame)
                timeout = time.time() + 2
                timeOutSet = 1
                i = i + 1
            elif (i == 2):
                cv2.imwrite("./RomanNumberDetector/numbers/romannumber2.tiff", frame)
                i = i + 1
            elif (i == 3):
                cv2.imwrite("./RomanNumberDetector/numbers/romannumber3.tiff", frame)
                i = i + 1
            elif (i == 4):
                cv2.imwrite("./RomanNumberDetector/numbers/romannumber4.tiff", frame)
                i = i + 1
            elif (i == 5):
                cv2.imwrite("./RomanNumberDetector/numbers/romannumber5.tiff", frame)
                i = i + 1
            elif (i == 6):
                break


    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break


############################################
# CROP Pictures
############################################

cropped = []

# image path and valid extensions
imageDir = "./RomanNumberDetector/numbers"  # specify your path here
image_path_list = []
valid_image_extensions = [".tiff"]  # specify your vald extensions here
valid_image_extensions = [item.lower() for item in valid_image_extensions]

# create a list all files in directory and
# append files with a vaild extention to image_path_list
for file in os.listdir(imageDir):
    extension = os.path.splitext(file)[1]
    if extension.lower() not in valid_image_extensions:
        continue
    image_path_list.append(os.path.join(imageDir, file))

# loop through image_path_list to open each image
for imagePath in image_path_list:
    img = cv2.imread(imagePath)

    colorFilter = crop.ColorFilter(img)
    colorFilter.filterRed()
    colorFilter.closing(colorFilter.mask)
    # colorFilter.showImg('closing',colorFilter.closing)
    shapeD = crop.ShapeDetecter(img, colorFilter.closing)
    cropped.append(shapeD.analyse())


############################################
# analyse Pictures
############################################

detectedNumber = []

for abc in cropped:
    detectedNumber.append(analyse.analyseNumber(abc))

print(detectedNumber)

cv2.waitKey(0)