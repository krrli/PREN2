#!/usr/bin/env python3
import sys
import glob
import os
import cv2

sys.path.append(".") # make script callable from project directory
sys.path.append("..") # make script callable from bin directory

from kamerad_schwungrad.MainBitch import MainBitch

main_bitch = MainBitch()

    # for file in glob.glob("RomanDetector/numbers/*.tiff"):
    #     os.unlink(file)

camera = None
try:
    camera = cv2.VideoCapture(0)
    while True:
        main_bitch.handle_roman_numeral_detection(camera)
finally:
    if not camera is None:
        camera.release()