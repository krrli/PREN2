###ask for number
import cv2
import datetime
import time

cap = cv2.VideoCapture(1)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    name = str(datetime.datetime.now()) + ".png"
    cv2.imwrite(name, frame)
    print("saved '" + name + "'")
    # cv2.imshow("preview", frame)
    # cv2.waitKey(1) #  & 0xFF != ord("q"):
    #     pass

    # cv2.destroyWindow("preview")


cap.realease()
