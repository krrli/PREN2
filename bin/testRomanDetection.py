#!/usr/bin/env python3
import sys
import glob
import os

sys.path.append(".") # make script callable from project directory
sys.path.append("..") # make script callable from bin directory

from kamerad_schwungrad.MainBitch import MainBitch

main_bitch = MainBitch()
while True:
    # for file in glob.glob("RomanDetector/numbers/*.tiff"):
    #     os.unlink(file)
    main_bitch.handle_roman_numeral_detection()