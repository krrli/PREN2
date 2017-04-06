
from kamerad_schwungrad.FreedomInterface import FreedomInterface
from kamerad_schwungrad.TrafficLightDetector import TrafficLightDetector
from RomanNumberDetector.RomanDetector import RomanDetector
from kamerad_schwungrad.RomanDisplay import RomanDisplay
import random
import time

"""
This is the Main class that gets started
It handles the complete Process of driving on the parcours.
Most of the things are delegated to subcomponents but the
procedure of the parcours is handled here
"""


class MainBitch:
    def __init__(self):
        self._trafficLightDetector = TrafficLightDetector()
        self._cameraToUse = 1
        self._freedomInterface = FreedomInterface('/dev/ttyS0')
        self._romanDetector = RomanDetector(0)
        self._romanDisplay = RomanDisplay()
        self._romanDigit = 1

    """
    Drive the whole Parcours.
    """
    def run_parcour(self):
        while not self.wait_for_traffic_light():
            pass

        self._freedomInterface.send_start_signal()
        while True:
            self.handle_freedom_interface()
            self.handle_roman_numeral_detection()

    """
    Handles the communication with the Freedom Board
    """
    def handle_freedom_interface(self):
        if not self._freedomInterface.no_command_received():
            self._freedomInterface.wait_for_command()

        if self._freedomInterface.roman_numeral_requested():
            self._freedomInterface.send_roman_numeral(self._romanDigit)

        if self._freedomInterface.curve_signaled():
            self._freedomInterface.send_acknowledge()

        if self._freedomInterface.invalid_command_received():
            self._freedomInterface.send_error()

    """
    Detect then a roman numeral is on the camera
    and stop to take a picture.
    """
    def handle_roman_numeral_detection(self):
        # send a stop signal every five seconds for 2 seconds
        # just to test the thing
        # if int(time.time()) % 5 == 0:
        #   self._freedomInterface.send_stop_signal()
        #    time.sleep(2)
        # TODO: maybe stop to take pictures
        digit = self._romanDetector.startNumberDetection()
        if digit != 0:
            self._romanDigit =digit
            self._romanDisplay.printDigit(self._romanDigit)
        #     self._freedomInterface.send_start_signal()

    """
    Blocks until the traffic light is green.
    """
    def wait_for_traffic_light(self):
        was_red = False
        with cv2.VideoCapture(self._cameraToUse) as camera:
            ret, frame = camera.read()
            if frame is None:
                print("ERROR: no camera picture :(")
                return False

            is_red = traffic_light.detect_red_traffic_light(frame)
            is_green = traffic_light.detect_green_traffic_light(frame)

            if is_green and not red and was_red:
                return True

            was_red = is_red
            time.sleep(0.1)