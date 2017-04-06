#!/usr/bin/env python3
import sys
import cv2
sys.path.append(".") # make script callable from project directory
sys.path.append("..") # make script callable from bin directory
import time

from kamerad_schwungrad import TrafficLightDetector

sys.path.append(".") # make script callable from project directory
sys.path.append("..") # make script callable from bin directory

from kamerad_schwungrad.TrafficLightDetector import TrafficLightDetector

traffic_light = TrafficLightDetector()

cap = cv2.VideoCapture((int)(sys.argv[1]))

while True:
    ret, frame = cap.read()
    if traffic_light.detect_red_traffic_light(frame):
        print("RED")
    elif traffic_light.detect_green_traffic_light(frame):
        print("GREEN")
    else:
        print("NONE")
    # time.sleep(0.1)
    while cv2.waitKey() & 0xFF == 'q':
        pass


cap.release()
cv2.destroyAllWindows()
