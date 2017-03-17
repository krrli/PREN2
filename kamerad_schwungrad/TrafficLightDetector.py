import numpy as np
import cv2


class TrafficLightDetector:
    def __init__(self):
        pass

    def detect_red_traffic_light(self, frame):
        return self.count_color(frame, [150, 100, 200], [200, 255, 255]) > 100

    def detect_green_traffic_light(self, frame):
        return self.count_color(frame, [35, 73, 145], [78, 255, 255]) > 100

    def count_color(self, frame, lower, upper):
        ident = lower[0]
        # cv2.imshow('orig', frame)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        # find the colors within the specified boundaries and apply the mask
        mask = cv2.inRange(hsv, lower, upper)
        res = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('maskcolor'+str(ident), mask)
        cv2.imshow('rescolor'+str(ident), res)
        countcolor = cv2.countNonZero(mask)
        # while cv2.waitKey() & 0xFF == 'q':
        #    pass
        print(countcolor)
        return countcolor
