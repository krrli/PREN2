#OpenCV3
#30.04.17
#main

import cv2
import numpy as np
from RomanNumberDetector import crop, analyse

class RomanDetector4():

    frame = None
    cropped = []
    detectedNumber = []
    hasCharacterBeenEvaluated = False

    detectedRomanBars = []

    '''
    To be called for Number
    '''
    def startNumberDetection(self, frame):
        self.frame = frame
        return self.capture(self.frame)

    '''
    Search for 2 RedBars and take a picture
    when the first picture is taken, set timeout
    after 5 pictures taken or 2 seconds return
    '''
    def capture(self,frame):

        if not self.hasCharacterBeenEvaluated:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

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
            test = cv2.GaussianBlur(red_hue_image, (9, 9), 0)
            # test = cv2.GaussianBlur(mask, (9,9), 0)

            ###
            kernel = np.ones((5, 5), np.uint8)
            opening = cv2.morphologyEx(test, cv2.MORPH_OPEN, kernel)

            ret, thresh = cv2.threshold(opening, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # cv2.imshow('OTSU', thresh)
            ###


            # Get Contours
            _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            barCount = 0

            rectangleList = []

            # Loop Through Found contours
            for foundRectangle in contours:
                if barCount <= 2:
                    approxDistance = cv2.arcLength(foundRectangle, True) * 0.02

                    approxCurve = cv2.approxPolyDP(foundRectangle, approxDistance, True)

                    # Only look for rectangles
                    if len(approxCurve) == 4:
                        rect = cv2.boundingRect(approxCurve)
                        # Only save Rectangles with height of 150+
                        if rect[3] >= 80:
                            rectangleList.append(rect)
                            barCount += 1

            # Only if exactly 2 Red bars were found, save them to the Picture array
            if barCount == 2:

                print('found ')

                self.detectedRomanBars.append(frame)

                return self.crop()

    '''
    This function will perform several operations on every image taken from folder numbers.
    The main goal is to calculate 4 inner coordinates for a picture resize without the RedBars.
    LeftBar (topLeft, bottomRight), RightBar (TopLeft, BottomLeft)
    The cropped images are finally stored in an array
    Further descriptions in crop.py
    '''
    def crop(self):

        self.cropped.clear()

        for image in self.detectedRomanBars:
            img = image

            colorFilter = crop.ColorFilter(img)
            colorFilter.filterRed()
            colorFilter.closing(colorFilter.mask)
            # colorFilter.showImg('closing',colorFilter.closing)
            shapeD = crop.ShapeDetecter(img, colorFilter.closing)
            self.cropped.append(shapeD.analyse())

            return self.analyse()

    '''
    This function analyses all available cropped pictures in cropped array.
    A counter will be increased by one for every detected number.
    The number with the highest count will be returned at least 0.
    '''
    def analyse(self):

        self.detectedNumber.clear()

        '''
        return analyse.analyseNumber(self.cropped[0])

        '''
        for abc in self.cropped:
            self.detectedNumber.append(analyse.analyseNumber(abc))

        #print(self.detectedNumber)

        count = [0] * 5

        for abc in self.detectedNumber:

            if (abc == 1):
                count[0] = count[0] + 1
            if (abc == 2):
                count[1] = count[1] + 1
            if (abc == 3):
                count[2] = count[2] + 1
            if (abc == 4):
                count[3] = count[3] + 1
            if (abc == 5):
                count[4] = count[4] + 1

        c = 5

        while (c > 0):
            if (count[0] == c):
                return 1
            if (count[1] == c):
                return 2
            if (count[2] == c):
                return 3
            if (count[3] == c):
                return 4
            if (count[4] == c):
                return 5
            c = c - 1

        return 0
