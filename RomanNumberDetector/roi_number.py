import cv2
import numpy as np

def cropNumber(image):
    #im = cv2.imread(image)
    im = image
    #imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(im, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #only keep the largest contours
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

    for c in contours:
        rect = cv2.boundingRect(c)
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        (x, y), radius = cv2.minEnclosingCircle(c)

        c = max(contours, key=cv2.contourArea)

        # get min and max corrdinates
        yStart = np.amin(c, axis=0)[0][1]
        yEnd = np.amax(c, axis=0)[0][1]

        h_new = yEnd - yStart

    try:
        _ ,width = im.shape
    except:
        width = 0

    cropArray = []

    try:
        cropImg_top_top = im[(int)(yStart):(int)(yEnd - 3 * h_new / 4), 0:width]

        cropImg_top = im[(int)(yStart + h_new / 4):(int)(yEnd - h_new / 2), 0:width]

        cropImg_bottom = im[(int)(yStart + h_new / 2):(int)(yEnd - h_new / 4), 0:width]
        cropImg_bottom_bottom = im[((int)(yStart + (int)(3 * h_new / 4))):(yEnd), 0:width]

        cropArray.append(cropImg_top_top)
        cropArray.append(cropImg_top)
        cropArray.append(cropImg_bottom)
        cropArray.append(cropImg_bottom_bottom)

        return cropArray

    except:
        return cropArray






