###ask for number
import cv2


from RomanNumberDetector.RomanDetector2 import RomanDetector2

test = RomanDetector2()

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    detectedNumber = test.startNumberDetection(frame)
    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    print(detectedNumber)


'''
from RomanNumberDetector.RomanDetector import RomanDetector

test = RomanDetector(0)

detectedNumber = test.startNumberDetection()

print(detectedNumber)
'''