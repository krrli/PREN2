#OpenCV3
#07.03.17
#main

import cv2
import numpy as np
import sys
import crop


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

while(True):
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
                    # Only save Rectangles with height of 250+
                    if rect[3] >= 150:
                        rectangleList.append(rect)
                        barCount += 1

        # Only if exactly 2 Red bars were found, save them to the Picture array
        if barCount == 2:

            print('found')

            if(i == 1):
                cv2.imwrite("romannumber1.tiff", frame)
                i = i+1
            elif(i == 2):
                cv2.imwrite("romannumber2.tiff", frame)
                i = i+1
            elif(i == 3):
                cv2.imwrite("romannumber3.tiff", frame)
                i = i+1
            elif (i == 4):
                cv2.imwrite("romannumber4.tiff", frame)
                i = i + 1
            elif (i == 5):
                cv2.imwrite("romannumber5.tiff", frame)
                i = i + 1
            elif(i == 6):
                break

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break


############################################
# CROP 5 the Pictures
############################################

##Picture 1
img = cv2.imread("romannumber1.tiff")
width = 800
height = 600
colorFilter = crop.ColorFilter(img)
colorFilter.filterRed()
colorFilter.closing(colorFilter.mask)
#colorFilter.showImg('closing',colorFilter.closing)
shapeD = crop.ShapeDetecter(img, colorFilter.closing)
shapeD.analyse()
cv2.imwrite('cropped1.tiff', shapeD.cropped)

##Picture 2
img = cv2.imread("romannumber2.tiff")
width = 800
height = 600
colorFilter = crop.ColorFilter(img)
colorFilter.filterRed()
colorFilter.closing(colorFilter.mask)
#colorFilter.showImg('closing',colorFilter.closing)
shapeD = crop.ShapeDetecter(img, colorFilter.closing)
shapeD.analyse()
cv2.imwrite('cropped2.tiff', shapeD.cropped)

##Picture 3
img = cv2.imread("romannumber3.tiff")
width = 800
height = 600
colorFilter = crop.ColorFilter(img)
colorFilter.filterRed()
colorFilter.closing(colorFilter.mask)
#colorFilter.showImg('closing',colorFilter.closing)
shapeD = crop.ShapeDetecter(img, colorFilter.closing)
shapeD.analyse()
cv2.imwrite('cropped3.tiff', shapeD.cropped)

##Picture 4
img = cv2.imread("romannumber4.tiff")
width = 800
height = 600
colorFilter = crop.ColorFilter(img)
colorFilter.filterRed()
colorFilter.closing(colorFilter.mask)
#colorFilter.showImg('closing',colorFilter.closing)
shapeD = crop.ShapeDetecter(img, colorFilter.closing)
shapeD.analyse()
cv2.imwrite('cropped4.tiff', shapeD.cropped)

##Picture 5
img = cv2.imread("romannumber5.tiff")
width = 800
height = 600
colorFilter = crop.ColorFilter(img)
colorFilter.filterRed()
colorFilter.closing(colorFilter.mask)
#colorFilter.showImg('closing',colorFilter.closing)
shapeD = crop.ShapeDetecter(img, colorFilter.closing)
shapeD.analyse()
cv2.imwrite('cropped5.tiff', shapeD.cropped)


############################################
# analyse 5 Pictures
############################################



cv2.waitKey(0)