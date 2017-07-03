import numpy as np
import cv2
from kamerad_schwungrad.debug import show_debug_frame, wait_for_input


class TrafficLightDetector:
    def __init__(self):
        pass

    def cut_frame(self, frame):
        cut_width = len(frame[0]) // 2
        return frame[:, 0:cut_width]

    def detect_red_traffic_light(self, frame):
        return self.count_color("red", frame, [150, 100, 200], [200, 255, 255]) > 100

    def detect_green_traffic_light(self, frame):
        return self.count_color("green", frame, [35, 150, 145], [78, 255, 255]) > 70

    def count_color(self, color, frame, lower, upper):
        # cv2.imwrite(img=frame, filename=(color + "-orig.png"))
        show_debug_frame('TrafficLight orig', frame)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        # find the colors within the specified boundaries and apply the mask
        mask = cv2.inRange(hsv, lower, upper)
        res = cv2.bitwise_and(frame, frame, mask=mask)



        show_debug_frame("TrafficLight " + color, res)
        countcolor = cv2.countNonZero(mask)
        # wait_for_input()
        print(color + ": ", countcolor)
        return countcolor
