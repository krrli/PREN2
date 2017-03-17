#!/usr/bin/env python3
import sys
sys.path.append(".")  # make script callable from project directory
sys.path.append("..")  # make script callable from bin directory

from kamerad_schwungrad.RomanDisplay import RomanDisplay

display = RomanDisplay()
if len(sys.argv) < 2:
    print("Please pass number to display as first command line argument\n\n")
    sys.exit(1)

number_to_display = sys.argv[1]
print("Displaying number", number_to_display + "\n")
display.display_number(number_to_display)
