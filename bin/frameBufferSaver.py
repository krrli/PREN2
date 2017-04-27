###ask for number
import sys
import cv2
import time
import queue


sys.path.append(".") # make script callable from project directory
sys.path.append("..") # make script callable from bin directory

from kamerad_schwungrad.FrameBuffer import FrameBuffer

frameBuffer = FrameBuffer()

cap = cv2.VideoCapture(0)

frameBuffer.set_camera(cap)
frameBuffer.start_capturing()

time.sleep(20)
frameBuffer.stop_capturing()

i = 0
while True:
    try:
        i = i + 1
        filename = '{0:03d}.png'.format(i)
        print("Saving '" + filename + "'")
        cv2.imwrite(filename, frameBuffer.frame_queue.get_nowait())
    except queue.Empty:
        break