###ask for number
import os
import sys
import cv2
import time

sys.path.append(".") # make script callable from project directory
sys.path.append("..") # make script callable from bin directory

from RomanNumberDetector.RomanDetector5 import RomanDetector5

from queue import Queue
from threading import Thread, Lock, Event


class FrameBuffer:
    def __init__(self):
        self.frame_queue = Queue()
        self._camera_lock = Lock()
        self._camera = None
        self._capture_stop_event = Event()
        self.RomanDetector = RomanDetector5()

    def set_camera(self, camera):
        with self._camera_lock:
            self._camera = camera

    def start_capturing(self):
        thread = Thread(args=(), target=self._capture)
        thread.start()

    def _capture(self):
        while not self._capture_stop_event.is_set():
            frame = None
            with self._camera_lock:
                ret, frame = self._camera.read()

            if not frame is None:
                self.frame_queue.put_nowait(frame)
                print(self.frame_queue.qsize())


    def stop_capturing(self):
        self._capture_stop_event.set()

    def start_analyse(self):

        thread = Thread(args=(), target=self._analyse())
        thread.start()

    def _analyse(self):

        detected = []

        while not self.frame_queue.empty() :
            analysed = self.RomanDetector.startNumberDetection(self.frame_queue.get_nowait())

            '''
            i = time.clock()
            ##test
            path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "numbers")
            completePath = path + "/" + str(i) + ".tiff"
            # store in folder
            cv2.imwrite(completePath, self.frame_queue.get_nowait())
            '''

            if analysed != None:
                detected.append(analysed)

        ###how many times should Number appear
        i = 5
        NumberHasBeenFound = False

        while i > 0:
            if detected.count(5) >= i:
                print("Number:" + "5")
                NumberHasBeenFound = True
                break
            elif detected.count(4) >= i:
                print("Number:" + "4")
                NumberHasBeenFound = True
                break
            elif detected.count(3) >= i:
                print("Number:" + "3")
                NumberHasBeenFound = True
                break
            elif detected.count(2) >= i:
                print("Number:" + "2")
                NumberHasBeenFound = True
                break
            else:
                i = i -1

        if detected.count(1) >= 1 and NumberHasBeenFound == False:
            print("Number:" + "1")
            NumberHasBeenFound = True

        if not NumberHasBeenFound:
            print("Random Number :(")

cap = cv2.VideoCapture(0)


####just to see something
'''
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break
'''



frameBuffer = FrameBuffer()

frameBuffer.set_camera(cap)
frameBuffer.start_capturing()

time.sleep(14)

frameBuffer.stop_capturing()

frameBuffer.start_analyse()










