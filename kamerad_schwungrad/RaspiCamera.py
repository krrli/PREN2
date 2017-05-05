from picamera.array import PiRGBArray
from picamera import PiCamera

from kamerad_schwungrad.Camera import Camera
import cv2

class RaspiCamera(Camera):
    def __init__(self):
        super().__init__(None)
        self._raw_capture = PiRGBArray(self._camera)

    def create_camera(self, camspec):
        return PiCamera()

    def capture(self):
        self._raw_capture = PiRGBArray(self._camera)
        self._camera.capture(self._raw_capture, format="bgr")
        return self._raw_capture.array

    def free_camera(self):
        self._camera = None

