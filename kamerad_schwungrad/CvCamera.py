from kamerad_schwungrad.Camera import Camera
import cv2


class CvCamera(Camera):
    def __init__(self, camspec):
        super().__init__(camspec)

    def create_camera(self, camspec):
        return cv2.VideoCapture(camspec)


    def capture(self):
        ret, frame = self._camera.read()
        return frame

    def free_camera(self):
        self._camera.release()