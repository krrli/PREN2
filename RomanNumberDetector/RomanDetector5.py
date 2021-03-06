#OpenCV3
#21.05.17
#main

import cv2
import numpy as np
from RomanNumberDetector import crop, analyse

import sys

sys.path.append(".") # make script callable from project directory
sys.path.append("..") # make script callable from bin directory

class RomanDetector5():

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
        self.detectedRomanBars.clear()

        if not self.hasCharacterBeenEvaluated:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # define range of red color in HSV

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

            kernel = np.ones((5, 5), np.uint8)
            opening = cv2.morphologyEx(red_hue_image, cv2.MORPH_OPEN, kernel, iterations = 2)
            #closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations = 5)

            blur = cv2.GaussianBlur(opening, (5, 5), 0)
            ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            edges = cv2.Canny(blur, ret / 2, ret)
            edges = cv2.dilate(edges, kernel, iterations=3)
            edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=10)

            # Get Contours
            _, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            barCount = 0

            # cv2.imshow('test', edges)

            # cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
            rectangleList = []

            # Loop Through Found contours
            for foundRectangle in contours:
                if barCount <= 2:

                    area = cv2.contourArea(foundRectangle)

                    # calculate center and radius of minimum enclosing circle
                    (x, y), radius = cv2.minEnclosingCircle(foundRectangle)

                    approxDistance = cv2.arcLength(foundRectangle, True) * 0.02
                    approxCurve = cv2.approxPolyDP(foundRectangle, approxDistance, True)

                    #TODO: check Values
                    # Only look for rectangles
                    if (area > 1000):
                        rect = cv2.boundingRect(approxCurve)
                        #print(area)
                        # Only save Rectangles with height of 200+ or radius of 100+
                        if radius >= 80 or rect[3] >= 120:
                        #if rect[3] >= 200:
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
    '''
    def analyse(self):

        self.detectedNumber.clear()

        #return analyse.analyseNumber(self.cropped[0])

        for abc in self.cropped:
            self.detectedNumber.append(analyse.analyseNumber(abc))

        #print(self.detectedNumber)

        for abc in self.detectedNumber:

            if (abc == 1):
                return 1
            if (abc == 2):
                return 2
            if (abc == 3):
                return 3
            if (abc == 4):
                return 4
            if (abc == 5):
                return 5

        return 0


