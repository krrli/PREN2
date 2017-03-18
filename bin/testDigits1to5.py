import RPi.GPIO as GPIO
import time

# passt nonig so rechtig zu de mainbitch
# bruchi github nur schnell as backup :D

allSegments = (7,11,13,15,29,31,33)
segments1 = (15, 33)
segments2 = (13, 15, 7, 29, 31)
segments3 = (13, 15, 7, 33, 31)
segments4 = (11, 7, 15, 33)
segments5 = (13, 11, 7, 33, 31)

# setMode of board
GPIO.setmode(GPIO.BOARD)

# setup pins as OUT
for segment in allSegments:
    GPIO.setup(segment, GPIO.OUT)

def printDigit(segments, noToPrint):
    for segment in segments:
        print("digit: ", noToPrint)
        GPIO.output(segment, 1)


def clearDigit(segments):
    # wait for 1sec
    time.sleep(1)
    for segment in segments:
        print("clear digit")
        GPIO.output(segment, 0)

printDigit(segments1, 1)
clearDigit(segments1)
printDigit(segments2, 2)
clearDigit(segments2)
printDigit(segments3, 3)
clearDigit(segments3)
printDigit(segments4, 4)
clearDigit(segments4)
printDigit(segments5, 5)
clearDigit(segments5)

for segment in allSegments:
    GPIO.cleanup(segment)
