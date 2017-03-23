"""
Responsible for displaying the roman digit on a 7 segment display.
"""
import RPi.GPIO as GPIO
class RomanDisplay:

    def clearAllDigits(self):
        # setup pins as OUT
        for segment in self.allSegments:
            print("segment auf 0: ", segment)
            GPIO.setup(segment, 0)
            # GPIO.cleanup(segment)

    def cleanupAll(self):
        for segment in self.allSegments:
            GPIO.cleanup(segment)

    def __init__(self):
        self.allSegments = (7, 11, 13, 15, 29, 31, 33)
        self.segments1 = (15, 33)
        self.segments2 = (13, 15, 7, 29, 31)
        self.segments3 = (13, 15, 7, 33, 31)
        self.segments4 = (11, 7, 15, 33)
        self.segments5 = (13, 11, 7, 33, 31)

        # setMode of board
        GPIO.setmode(GPIO.BOARD)

        # setup pins as OUT
        for segment in self.allSegments:
            GPIO.setup(segment, GPIO.OUT)

        self.clearAllDigits();


    def printDigit(self, segments):
        # self.clearAllDigits()
        for segment in segments:
            print("segmänt: ", segment)
            GPIO.output(segment, 1)

    def clearDigit(self, segments):
        # wait for 1sec
        # time.sleep(1)
        for segment in segments:
            print("clear digit")
            GPIO.output(segment, 0)

    def display_number(self, number):
        if number == 1:
            print("zeig s ", number, "\n")
            self.printDigit(self.segments1)
            # self.clearDigit(self.segments1)
        if number == 2:
            print("zeig s ", number, "\n")
            self.printDigit(self.segments2)
        if number == 3:
            print("zeig s ", number, "\n")
            self.printDigit(self.segments3)
        if number == 4:
            print("zeig s ", number, "\n")
            self.printDigit(self.segments4)
        if number == 5:
            print("zeig s ", number, "\n")
            self.printDigit(self.segments5)



