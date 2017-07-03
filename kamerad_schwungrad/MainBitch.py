from serial.serialutil import SerialException

from kamerad_schwungrad.FreedomInterface import FreedomInterface
from kamerad_schwungrad.TrafficLightDetector import TrafficLightDetector
from RomanNumberDetector.RomanDetector5 import RomanDetector5
from kamerad_schwungrad.RomanDisplay import RomanDisplay
from kamerad_schwungrad.FrameBuffer import FrameBuffer
from kamerad_schwungrad.QueueWorker import QueueWorker
import random
import time
import cv2
import os

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
        # Kamera indexes für OpenCV [rechts, links]
        self._detectionCameras = ["/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.5:1.0-video-index0", "/dev/v4l/by-path/platform-3f980000.usb-usb-0:1.3:1.0-video-index0"]
        for idx, camera in enumerate(self._detectionCameras):
            self._detectionCameras[idx] = os.path.join(os.path.dirname(camera), os.readlink(camera))
            print("MAIN: using camera " + self._detectionCameras[idx])

        self._trafficLightCameraToUse = self._detectionCameras[0]
        self._detectionCameraToUseIndex = 0
        self._freedomInterface = FreedomInterface('/dev/ttyAMA0')
        self._romanDetector = RomanDetector5()
        self._queueWorker = QueueWorker(self._romanDetector)
        self._romanDisplay = RomanDisplay()
        self._romanDisplay.resetAllSegments()
        self._romanDigit = 1
        self._frameBuffers = []
        print("MAIN: init")

    """
    Drive the whole Parcours.
    """
    def run_parcour(self):
        print("MAIN: parcour was started, waiting for traffic light")
        self._was_red = False
        try:
            camera = cv2.VideoCapture(self._trafficLightCameraToUse)
            while not self.wait_for_traffic_light(camera):
               pass
        finally:
            if not camera is None:
                camera.release()


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
                    print("MAIN: Creating cameras for Roman Numeral Detection")
                    self.start_roman_numeral_detection()
                    print("MAIN: started")
                    parcours_finished = False
                    while not parcours_finished:
                        # self.handle_roman_numeral_detection()
                        # TODO: Queue Worker abfroge, öber scho e nommere hed
                        parcours_finished = self.handle_freedom_interface()
                        time.sleep(0.01)
                    break
            except SerialException:
                print("MAIN: Could not use Serial Port?")
            finally:
                self._freedomInterface.close_port()


    def start_roman_numeral_detection(self):
        self._frameBuffers = []

        for camera in self._detectionCameras:
            print("MAIN: creating framebuffer")
            frame_buffer = FrameBuffer()
            self._frameBuffers.append(frame_buffer)
            self._queueWorker.add_frame_buffer(frame_buffer)

        self.set_camera_for_framebuffer()

    """
    Handles the communication with the Freedom Board
    """
    def handle_freedom_interface(self):
        try:
            self._freedomInterface.check_command_received()
        except (SerialException, OSError) as ex:
            print(ex)
            print("F3DM: Error reading serial port")
            print("F3DM: trying to reopen serial port")
            self._freedomInterface.close_port()
            self._freedomInterface.open_port()

        if self._freedomInterface.acknowledge_received():
            pass

        if self._freedomInterface.error_received():
            self._freedomInterface.close_port()
            self._freedomInterface.open_port()

        if self._freedomInterface.roman_numeral_requested():
            print("F3DM: roman numeral requested")
            self.send_back_roman_digit()
            return True

        if self._freedomInterface.curve_signaled():
            print("F3DM: curve was signaled")
            self._freedomInterface.send_acknowledge()
            self.switch_camera()

        if self._freedomInterface.invalid_command_received():
            print("F3DM: invalid command received")
            self._freedomInterface.send_error()
        self._freedomInterface.clear_command()
        return False

    def send_back_roman_digit(self):
        print("MAIN: stopping frame buffers")
        for frameBuffer in self._frameBuffers:
            frameBuffer.stop_capturing()

        print("MAIN: starting queue worker")
        self._queueWorker.start_working()

        print("MAIN: waiting for queue worker to finish")
        while not self._queueWorker.idle:
            print("MAIN: still waiting ... ")
            self._romanDisplay.blinki()
            time.sleep(0.5)

        self._romanDisplay.resetAllSegments()

        digit = self._queueWorker.number_detected
        print("MAIN: displaying digit " + str(digit))
        if digit == 0:
            digit = random.randint(1, 5)
            print("MAIN: RANDOM DIGIT?!?!?!? ! " + str(digit))

        self._queueWorker.stop_capturing()
        self._romanDisplay.display_number(digit)
        self._freedomInterface.send_roman_numeral(digit)


    """
    Blocks until the traffic light is green.
    """
    def wait_for_traffic_light(self, camera):
        ret, frame = camera.read()
        if frame is None:
            print("ERROR: no camera picture :(")
            return False

        is_red = self._trafficLightDetector.detect_red_traffic_light(frame)
        is_green = self._trafficLightDetector.detect_green_traffic_light(frame)

        if is_green and not is_red and self._was_red:
            print("LGHT: red traffic light was seen")
            return True

        if is_red:
            print("LGHT: red traffic light was seen")
            self._was_red = is_red

    def switch_camera(self):
        print("MAIN: switching camera")
        self._detectionCameraToUseIndex = self._detectionCameraToUseIndex  + 1
        self._detectionCameraToUseIndex = self._detectionCameraToUseIndex % len(self._detectionCameras)
        self.set_camera_for_framebuffer()

    def set_camera_for_framebuffer(self):
        camera = self._detectionCameras[self._detectionCameraToUseIndex]
        for idx, frame_buffer in enumerate(self._frameBuffers):
            if idx == self._detectionCameraToUseIndex:
                frame_buffer.set_camera(cv2.VideoCapture(camera))
                frame_buffer.start_capturing()
            else:
                frame_buffer.stop_capturing()
                frame_buffer.set_camera(None)

