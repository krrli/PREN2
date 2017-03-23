import unittest
import cv2
from glob import glob
from kamerad_schwungrad.TrafficLightDetector import TrafficLightDetector


class TrafficLightDetectorTestCase(unittest.TestCase):

    def setUp(self):
        self.red_frames = [cv2.imread(image, 1) for image in glob('resources/traffic-lights/red/*')]
        self.green_frames = [cv2.imread(image, 1) for image in glob('resources/traffic-lights/green/*')]
        self._traffic_light_detector = TrafficLightDetector()

    def test_detect_red_traffic_light(self):
        for frame_num in range(0, len(self.red_frames)):
            with self.subTest(i=frame_num):
                self.assertTrue(self._traffic_light_detector.detect_red_traffic_light(self.red_frames[frame_num]))

    def test_detect_red_traffic_light_when_green(self):
        for frame_num in range(0, len(self.green_frames)):
            with self.subTest(i=frame_num):
                self.assertFalse(self._traffic_light_detector.detect_red_traffic_light(self.green_frames[frame_num]))




    def test_detect_green_traffic_light(self):
        for frame_num in range(0, 1): # len(self.green_frames)):
            with self.subTest(i=frame_num):
                self.assertTrue(self._traffic_light_detector.detect_green_traffic_light(self.green_frames[frame_num]))

    def test_detect_green_traffic_light_when_red(self):
        for frame_num in range(0, len(self.red_frames)):
            with self.subTest(i=frame_num):
                self.assertFalse(self._traffic_light_detector.detect_green_traffic_light(self.red_frames[frame_num]))

