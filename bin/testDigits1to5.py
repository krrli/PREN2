import RPi.GPIO as GPIO
import time

# passt nonig so rechtig zu de mainbitch
# bruchi github nur schnell as backup :D

allSegments = (7,11,13,15,29,31,33, 35)
segments1 = (33,31)
segments2 = (29,33,7,11,15)
segments3 = (29,33,7,31,15)
segments4 = (13,7,33,31)
segments5 = (29,13,7,31,15)
segmentsJuhuu = (35,15,11,13,29,33,31)

# setMode of board
GPIO.setmode(GPIO.BOARD)

# setup pins as OUT
for segment in allSegments:
    # Setup
    GPIO.setup(segment, GPIO.OUT)

def printDigit(segments, noToPrint):
    print("digit: ", noToPrint)
    for segment in segments:
        GPIO.output(segments, 1)


def clearDigit(segments):
    # wait for 1sec
    time.sleep(1)
    for segment in segments:
        print("clear digit")
        GPIO.output(segment, 0)

def blinki(segments):
    for segment in segments:
        print("digit: ", segment)
        GPIO.output(segment, 1)
        time.sleep(1/8)
        print("clear digit ", segment)
        GPIO.output(segment, 0)

c=15
while (c > 0):
    blinki(segmentsJuhuu)
    if 0xFF == ord('q'):
        break
    c = c - 1


'''
blinki(segmentsJuhuu)
blinki(segmentsJuhuu)
blinki(segmentsJuhuu)
'''
print(" ----------- YOLO ----------- ")
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
