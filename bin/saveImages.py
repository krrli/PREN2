###ask for number
import cv2
import datetime
import time
import sys

sys.path.append(".") # make script callable from project directory
sys.path.append("..") # make script callable from bin directory

from kamerad_schwungrad.RaspiCamera import RaspiCamera

camera = RaspiCamera()
# cap = cv2.VideoCapture(1)

while(True):
    # Capture frame-by-frame
    # ret, frame = cap.read()
    frame = camera.capture()
    name = str(datetime.datetime.now()) + ".png"
    cv2.imwrite(name, frame)
    print("saved '" + name + "'")
    cv2.imshow("preview", frame)
    while cv2.waitKey(1) & 0xFF != ord("q"):
        pass

    cv2.destroyWindow("preview")


cap.realease()
