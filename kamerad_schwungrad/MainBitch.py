from serial.serialutil import SerialException

from kamerad_schwungrad.FreedomInterface import FreedomInterface
from kamerad_schwungrad.TrafficLightDetector import TrafficLightDetector
from RomanNumberDetector.RomanDetector import RomanDetector
from RomanNumberDetector.RomanDetector2 import RomanDetector2
from kamerad_schwungrad.RomanDisplay import RomanDisplay
import random
import time
import cv2

"""
This is the Main class that gets started
It handles the complete Process of driving on the parcours.
Most of the things are delegated to subcomponents but the
procedure of the parcours is handled here
"""


class MainBitch:
    def __init__(self):
        self._was_red = False
        self._trafficLightDetector = TrafficLightDetector()
        self._cameraToUse = 0
        self._freedomInterface = FreedomInterface('/dev/ttyS0')
        self._romanDetector = RomanDetector2()
        self._romanDisplay = None# RomanDisplay()
        self._romanDigit = 1

    """
    Drive the whole Parcours.
    """
    def run_parcour(self):
        self._was_red = False
        while not self.wait_for_traffic_light():
            pass

        tries = 1
        while tries <= 3:
            try:
                print("MAIN: sending start signal (try " + str(tries) + ")")
                tries += 1
                self._freedomInterface.open_port()
                response = self._freedomInterface.send_start_signal()
                if response is None:
                    print("MAIN: start signal was not acknowledged (nothing received)")

                if not response:
                    print("MAIN: ERROR after start signal")

                if response:
                    print("MAIN: started")
                    parcours_finished = False
                    while not parcours_finished:
                        # self.handle_roman_numeral_detection()
                        parcours_finished = self.handle_freedom_interface()
                    break
            except SerialException:
                print("MAIN: Could not use Serial Port?")
            finally:
                self._freedomInterface.close_port()


    """
    Handles the communication with the Freedom Board
    """
    def handle_freedom_interface(self):
        try:
            self._freedomInterface.check_command_received()
        except (SerialException, OSError):
            print("F3DM: Error reading serial port")
            print("F3DM: trying to reopen serial port")
            self._freedomInterface.close_port()
            self._freedomInterface.open_port()

        if self._freedomInterface.roman_numeral_requested():
            print("F3DM: roman numeral requested")
            while not (self._freedomInterface.send_roman_numeral(self._romanDigit) == True):
                pass
            return True

        if self._freedomInterface.curve_signaled():
            print("F3DM: curve was signaled")
            self._freedomInterface.send_acknowledge()

        if self._freedomInterface.invalid_command_received():
            print("F3DM: invalid command received")
            self._freedomInterface.send_error()
        self._freedomInterface.clear_command()
        return False

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

        try:
            camera = cv2.VideoCapture(self._cameraToUse)
            ret, frame = camera.read()
            if frame is None:
                print("Error no camera picture :(")
                return False

            self._romanDigit = self._romanDetector.startNumberDetection(frame)

            if self._romanDigit != 0:
                self._romanDisplay.printDigit(self._romanDigit)

        finally:
            if not camera is None:
                camera.release()

        #digit = random.randint(1,5) # self._romanDetector.startNumberDetection()
        #if digit != 0:
        #self._romanDigit = digit

        #self._freedomInterface.send_start_signal()

    """
    Blocks until the traffic light is green.
    """
    def wait_for_traffic_light(self):
        try:
            camera = cv2.VideoCapture(self._cameraToUse)
            ret, frame = camera.read()
            print("next frame")
            if frame is None:
                print("ERROR: no camera picture :(")
                return False

            is_red = self._trafficLightDetector.detect_red_traffic_light(frame)
            is_green = self._trafficLightDetector.detect_green_traffic_light(frame)

            if is_green and not is_red and self._was_red:
                return True

            if is_red:
                print("was_red set")
                self._was_red = is_red
            time.sleep(0.1)
        finally:
            if not camera is None:
                camera.release()
