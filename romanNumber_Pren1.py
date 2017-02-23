#OpenCV3
#05.12.16

import cv2
import numpy as np
from PIL import Image
import pytesseract



print(cv2.__version__)

def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect


def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return the warped image
    return warped

class ShapeDetecter():
    frame = ''
    mask = ''
    cnts = 0
    center = 0
    c = 0
    M = 0
    radius = 0
    x = 0
    y = 0
    w = 0
    h = 0

    booleanFlag = False

    rect_x = ''
    rect_y = ''
    rect_w = ''
    rect_h = ''


    def __init__(self, frame, mask):
        self.frame=frame
        self.mask=mask


    def analyse(self):
        image, contours, _ = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 1:

            areaArray = []

            for i, c in enumerate(contours):
                area = cv2.contourArea(c)
                areaArray.append(area)

            sorteddate = sorted(zip(areaArray, contours), key=lambda x: x[0], reverse=True)

            largestcontour = sorteddate[0][1]
            secondlagestcontour = sorteddate[1][1]


            # find minimum area
            rect = cv2.minAreaRect(largestcontour)
            # calculate coordinates of the minimum area rectangle
            box = cv2.boxPoints(rect)
            # normalize coordinates to integers
            box_1 = np.int0(box)

            # draw contours
            cv2.drawContours(self.frame, [box_1], 0, (0, 0, 255), 3)
            # calculate center and radius of minimum enclosing circle
            #(x, y), radius = cv2.minEnclosingCircle(c)
            # cast to integers
            #center = (int(x), int(y))
            #radius = int(radius)
            # draw the circle
            #img = cv2.circle(self.frame, center, radius, (0, 255, 0), 2)

            #cv2.drawContours(self.frame, contours, -1, (255, 0, 0), 1)

            # find minimum area
            rect = cv2.minAreaRect(secondlagestcontour)
            # calculate coordinates of the minimum area rectangle
            box = cv2.boxPoints(rect)
            # normalize coordinates to integers
            box_2 = np.int0(box)

            # draw contours
            cv2.drawContours(self.frame, [box_2], 0, (0, 0, 255), 3)
            # calculate center and radius of minimum enclosing circle
            #(x, y), radius = cv2.minEnclosingCircle(c)
            # cast to integers
            #center = (int(x), int(y))
            #radius = int(radius)
            # draw the circle
            #img = cv2.circle(self.frame, center, radius, (0, 255, 0), 2)

            #cv2.drawContours(self.frame, contours, -1, (255, 0, 0), 1)

            #a = np.array(largestcontour)
            #b = np.array(secondlagestcontour)

            pts = np.vstack((box_1, box_2)).squeeze()

            warped = four_point_transform(self.frame, pts)

            cv2.imshow("warped", warped)

            colorFilter.filterBlack(warped)



    def showImg(self, WindowName, which):
        cv2.imshow(WindowName, which)



class ColorFilter():
    frame = ''
    hsv = ''
    mask = ''
    res  = ''
    blurred = ''

    #lower_red = np.array([170, 50, 50])
    #upper_red = np.array([180, 255, 255])

    l_black = np.array([0, 0, 0])
    u_black = np.array([220, 50, 100])

    lower_red = np.array([170, 100, 100])
    upper_red = np.array([180, 255, 255])

    def __init__(self, frame):
        self.frame = frame

    def resizeImg(self):
        self.frame = cv2.resize(self.frame, (400, 400))

    def filterRed(self):
        self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        self.mask = cv2.inRange(self.hsv, self.lower_red, self.upper_red)
        self.res = cv2.bitwise_and(self.frame, self.frame, mask=self.mask)

    def filterBlack(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.l_black, self.u_black)
        res = cv2.bitwise_and(img,img, mask=mask)

        ####
        kernel = np.ones((15,15),np.uint8)
        closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        ####


        #print(pytesseract.image_to_string(closing))

        cv2.imshow('blacked', closing)


    def smothAndBlur(self, which):
        self.blurred = cv2.GaussianBlur(which, (5, 5), 0)

    def showImg(self, WindowName ,which):
        cv2.imshow(WindowName, which)


#Change to 1 for USB Cam
camera = cv2.VideoCapture(0)

while(1):
    (grabbed, frame) = camera.read()

    colorFilter = ColorFilter(frame)
    #redFiler.resizeImg()
    colorFilter.filterRed()

    colorFilter.smothAndBlur(colorFilter.mask)

    colorFilter.showImg('blured', colorFilter.blurred)

    shapeD = ShapeDetecter(colorFilter.frame, colorFilter.blurred)
    shapeD.analyse()
    shapeD.showImg('detected', shapeD.frame)

    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break



