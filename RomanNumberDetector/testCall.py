###ask for number
import sys
import cv2


sys.path.append(".") # make script callable from project directory
sys.path.append("..") # make script callable from bin directory

from RomanNumberDetector.RomanDetector4 import RomanDetector4

test = RomanDetector4()

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    detectedNumber = test.startNumberDetection(frame)
    print(detectedNumber)

    #if detectedNumber != None:
    #    break

    #frame = cv2.resize(frame, (400,400))

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break




'''
from RomanNumberDetector.RomanDetector import RomanDetector

test = RomanDetector(0)

detectedNumber = test.startNumberDetection()

print(detectedNumber)
'''