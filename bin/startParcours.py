#!/usr/bin/env python3
import sys
sys.path.append(".") # make script callable from project directory
sys.path.append("..") # make script callable from bin directory

from kamerad_schwungrad.MainBitch import MainBitch

main_bitch = MainBitch()
main_bitch.runParcour()
