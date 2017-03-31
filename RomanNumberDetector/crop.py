import cv2
import numpy as np


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


class ColorFilter():
    frame = ''
    hsv = ''
    mask = ''
    res  = ''
    blurred = ''
    closing = ''

    l_black = np.array([0, 0, 0])
    u_black = np.array([220, 50, 100])

    # lower mask (0-10)
    lower_red = np.array([0, 100, 10])
    upper_red = np.array([10, 255, 255])
    #mask0 = cv2.inRange(hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([170, 100, 100])
    upper_red = np.array([179, 255, 255])
    #mask1 = cv2.inRange(hsv, lower_red, upper_red)

    # Combine Masks
    #mask = mask0 + mask1
    #red_hue_image = cv2.addWeighted(mask0, 1.0, mask1, 1.0, 0.0)
    #test = cv2.GaussianBlur(red_hue_image, (9, 9), 0)


    def __init__(self, frame):
        self.frame = frame

    def resizeImg(self):
        self.frame = cv2.resize(self.frame, (400, 400))

    def filterRed(self):
        self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        #self.mask = cv2.inRange(self.hsv, self.lower_red, self.upper_red)
        mask0 = cv2.inRange(self.hsv, self.lower_red, self.upper_red)
        mask1 = cv2.inRange(self.hsv, self.lower_red, self.upper_red)
        mask = mask0 + mask1
        red_hue_image = cv2.addWeighted(mask0, 1.0, mask1, 1.0, 0.0)
        test = cv2.GaussianBlur(red_hue_image, (9, 9), 0)

        self.mask = test

        self.res = cv2.bitwise_and(self.frame, self.frame, mask=self.mask)

    def filterBlack(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.l_black, self.u_black)
        res = cv2.bitwise_and(img,img, mask=mask)

    def closing(self, img):
        kernel = np.ones((15,15),np.uint8)
        self.closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    def smothAndBlur(self, which):
        self.blurred = cv2.GaussianBlur(which, (5, 5), 0)

    def showImg(self, WindowName ,which):
        cv2.imshow(WindowName, which)



class ShapeDetecter():
    frame = ''
    mask = ''
    cnts = 0

    x1 = 0
    x2 = 0

    y1 = 0
    y2 = 0

    radius1 = 0
    radius2 = 0

    pts = 0

    # lower mask (0-10)
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 30])
    #mask0 = cv2.inRange(hsv, lower_black, upper_black)

    # upper mask (170-180)
    lower_black = np.array([0, 0, 20])
    upper_black = np.array([180, 255, 50])
    #mask1 = cv2.inRange(hsv, lower_black, upper_black)

    # Combine Masks
    #black_hue_image = cv2.addWeighted(mask0, 1.0, mask1, 1.0, 0.0)
    #test = cv2.GaussianBlur(black_hue_image, (9, 9), 0)

    mask2 = ''
    cropped = ''

    def __init__(self, frame, mask):
        self.frame = frame
        self.mask = mask

    def analyse(self):
        image, contours, _ = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #### change between 1 - 5
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
            #cv2.drawContours(self.frame, [box_1], 0, (0, 0, 255), 3)
            # calculate center and radius of minimum enclosing circle
            (x, y), radius = cv2.minEnclosingCircle(largestcontour)
            # cast to integers
            center = (int(x), int(y))
            self.x1 = x
            self.y1 = y
            radius = int(radius)
            self.radius1 = radius
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
            #cv2.drawContours(self.frame, [box_2], 0, (0, 0, 255), 3)
            # calculate center and radius of minimum enclosing circle
            (x, y), radius = cv2.minEnclosingCircle(secondlagestcontour)
            # cast to integers
            center = (int(x), int(y))
            self.x2 = x
            self.y2 = y
            radius = int(radius)
            self.radius2 = radius
            # draw the circle
            #img = cv2.circle(self.frame, center, radius, (0, 255, 0), 2)

            #cv2.drawContours(self.frame, contours, -1, (255, 0, 0), 1)

            ############

            box_1 = order_points(box_1)
            box_2 = order_points(box_2)

            if(self.x2 > self.x1):
                tl = box_1[1]
                bl = box_1[2]
                tr = box_2[0]
                br = box_2[3]

            else:
                tl = box_2[1]
                bl = box_2[2]
                tr = box_1[0]
                br = box_1[3]

            ############

            #pts = np.vstack((box_1, box_2)).squeeze()
            pts = np.vstack((tl,tr,bl,br)).squeeze()

            warped = four_point_transform(self.frame, pts)

            #Var1
            #warped = cv2.medianBlur(warped, 5)
            imgray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

            #cv2.imshow('imgray', imgray)
            #cv2.waitKey(0)

            #cv2.imshow('test',imgray)
            #ret, thresh = cv2.threshold(imgray, 50, 255, cv2.THRESH_BINARY_INV)

            ret, thresh = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


            #cv2.imshow('thresh', thresh)
            #cv2.waitKey(0)

            #cv2.imshow('test2', thresh)

            #th3 = cv2.adaptiveThreshold(imgray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

            ##Var2
            #hsv2 = cv2.cvtColor(warped, cv2.COLOR_BGR2HSV)
            #mask0 = cv2.inRange(hsv2, self.lower_black, self.upper_black)
            #mask1 = cv2.inRange(hsv2, self.lower_black, self.upper_black)
            #mask2 = cv2.inRange(hsv2, self.l_black, self.u_black)
            #black_hue_image = cv2.addWeighted(mask0, 1.0, mask1, 1.0, 0.0)
            #test = cv2.GaussianBlur(black_hue_image, (9, 9), 0)

            kernel = np.ones((5, 5), np.uint8)
            #Var2
            #closing = cv2.morphologyEx(black_hue_image, cv2.MORPH_CLOSE, kernel)
            #Var1

            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

            kernel = np.ones((5, 5), np.uint8)

            closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)



            #blurred = cv2.GaussianBlur(opening, (5, 5), 0)

            self.cropped = closing

            #cv2.imshow("opening", opening)

            height, width = closing.shape

            #print(height, width)

            #print(height, width)

            return closing




