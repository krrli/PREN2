from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

class RaspiCamera(Camera):
    def __init(self):
        super().__init__()
        # This may need to be allocated on each capture
        self._raw_capture = PiRGBArray(self._camera)

    def create_camera(self, camspec):
        return PiCamera()

    def capture(self):
        self._camera.capture(self._raw_capture, format="bgr")
        return self._raw_capture.array

    def free_camera(self):
        self._camera = None
        self._raw_capture = None

