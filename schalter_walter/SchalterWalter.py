import sys

sys.path.append(".") # make script callable from project directory
sys.path.append("..") # make script callable from bin directory

from kamerad_schwungrad.debug import wait_for_input


from kamerad_schwungrad.MainBitch import MainBitch
from schalter_walter.Unbuffered import Unbuffered
import RPi.GPIO as GPIO
import time

# make stdout unbuffered
sys.stdout = Unbuffered(sys.stdout)
sys.stderr = Unbuffered(sys.stderr)

GPIO_PIN = 3


def waitForLeverToBe(expectedState):
    while GPIO.input(GPIO_PIN) != expectedState:
        time.sleep(0.1)


print("DEMN: setting up GPIO pin for start lever")
GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIO_PIN, GPIO.IN)

waitForLeverToBe(GPIO.LOW)

# with daemon_context:
while True:
    print("DEMN: waiting for start lever ... ")
    waitForLeverToBe(GPIO.HIGH)

    print("DEMN: start lever detected")
    try:
        main_bitch = MainBitch()
        main_bitch.run_parcour()
    except Exception as e:
        print("D3MN: The bitch crashed!")
        print(e)

    print("DEMN: waiting for lever to go to off state ... ")
    waitForLeverToBe(GPIO.LOW)
