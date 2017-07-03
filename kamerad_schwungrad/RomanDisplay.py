"""
Responsible for displaying the roman digit on a 7 segment display.
"""
import RPi.GPIO as GPIO
import time




'''
TODO:
- Zahl zwösche 1 und 5
- Bispel för ufruef!
'''


"""
Use this class to display Roman Digits.
Possible Digits: 1-5; I-V
"""
class RomanDisplay:

    """
    Print Digit.
    param segment: segment 1 - 5, includes all pins to set to GPIO.HIGH (= azönde)
    """
    def printDigit(self, segments, number):
        print("print number: ", number)
        self.resetAllSegments()

        for segment in segments:
            GPIO.output(segment, GPIO.HIGH)

    """
    Setup Segments as GPIO out (define it as output pin).
    """
    def seuptAllSegments(self):
        # setup pins as OUT
        for segment in self.allSegments:
            GPIO.setup(segment, GPIO.OUT)

    """
    Set all Segments to GPIO.LOW (=0, ablösche).
    Reset all Segments
    """
    def cleanupAllSegments(self):
        print("-------- you called cleanupAllSegments --------")
        for segment in self.allSegments:
            GPIO.cleanup(segment)

    def resetAllSegments(self):
        print("-------- you called resetAllSegments --------")
        # Alli ablösche
        for segment in self.allSegments:
            print("clear digit", segment)
            GPIO.output(segment, 0)

    """
    Constructor.
    """
    def __init__(self):

        print("-------- you called __init__ --------")
        self.allSegments = (7, 11, 13, 15, 29, 31, 33)
        self.segments1 = (31, 33)
        self.segments2 = (7, 11, 15, 29, 33)
        self.segments3 = (7, 15, 29, 31, 33)
        self.segments4 = (7, 13, 31, 33)
        self.segments5 = (7, 13, 15, 29, 31)

        # setMode of board
        GPIO.setmode(GPIO.BOARD)
        self.seuptAllSegments()

        self.blinki_segments = (7, 11, 13, 15, 29, 31, 33)
        self.blinki_index = 0

    def blinki(self):
        GPIO.output(self.blinki_segments[self.blinki_index], GPIO.LOW)
        self.blinki_index += 1
        self.blinki_index %= len(self.blinki_segments)
        GPIO.output(self.blinki_segments[self.blinki_index], GPIO.HIGH)

    """
    Function which can be called to display digits on 7Segment.
    """
    def display_number(self, number):
        print("-------- you called display_number --------")
        print("zeig s ", number, "\n")
        segments =  {1: self.segments1,
                    2: self.segments2,
                    3: self.segments3,
                    4: self.segments4,
                    5: self.segments5,
                    }
        if(number in segments):
           self.printDigit(segments[number],number)

           # ond söscht so? --> abfo!
           #  evtl. eifach s füfi nä? oder random?

