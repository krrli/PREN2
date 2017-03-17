import cv2
import numpy as np

im = cv2.imread('cropped4.tiff')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# only keep the largest contours
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]


for c in contours:
    rect = cv2.boundingRect(c)
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    cv2.drawContours(im, [box], 0, (0, 0, 255), 2)

    (x, y), radius = cv2.minEnclosingCircle(c)


    c = max(contours, key=cv2.contourArea)

    # get min and max corrdinates
    minCord = np.amin(c, axis=0)
    maxCord = np.amax(c, axis=0)

    yStart = minCord[0][1]
    yEnd = maxCord[0][1]

    print(yStart, yEnd)


h_new = yEnd - yStart

print(box)
print(h_new)

_ , width, _ = im.shape


cropImg_top_top = im[(int)(yStart):(int)(yEnd-3*h_new/4), 0:width]

cropImg_top = im[(int)(yStart+h_new/4):(int)(yEnd-h_new/4), 0:width]


cropImg_bottom = im[(int)(yStart+h_new/4):(int)(yEnd-h_new/4), 0:width]
cropImg_bottom_bottom = im[((int)(yStart+(int)(h_new)))/2:(yEnd), 0:width]

#cv2.imshow('thresh', thresh)
cv2.imshow('contours', im)

cv2.waitKey(0)

cv2.imshow('toptop', cropImg_top_top)
cv2.imshow('top', cropImg_top)
cv2.imshow('bottom', cropImg_bottom)
cv2.imshow('bottombottom', cropImg_bottom_bottom)

cv2.waitKey(0)
