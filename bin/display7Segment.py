#!/usr/bin/env python3
import sys
import time
sys.path.append(".")  # make script callable from project directory
sys.path.append("..")  # make script callable from bin directory

from kamerad_schwungrad.RomanDisplay import RomanDisplay

inputInt = int(input("Enter a number to display: "))
# print(inputInt)

if inputInt > 5 or inputInt < 1:
    print("dont. bigger than 5 or smaller than 1!", inputInt)

display = RomanDisplay()

number_to_display = inputInt
print("Displaying number", inputInt)

display.display_number(inputInt)
time.sleep(5)


display.cleanupAll()