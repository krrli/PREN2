#!/usr/bin/env python3
import sys
import cv2
sys.path.append(".") # make script callable from project directory
sys.path.append("..") # make script callable from bin directory

from kamerad_schwungrad import TrafficLightDetector

sys.path.append(".") # make script callable from project directory
sys.path.append("..") # make script callable from bin directory

from kamerad_schwungrad.TrafficLightDetector import TrafficLightDetector

traffic_light = TrafficLightDetector()

cap = cv2.VideoCapture((int)(sys.argv[1]))

while True:
    ret, frame = cap.read()
    traffic_light.detect_red_traffic_light(frame)
    traffic_light.detect_green_traffic_light(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
