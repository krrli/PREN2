import sys

sys.path.append(".") # make script callable from project directory
sys.path.append("..") # make script callable from bin directory

from kamerad_schwungrad.debug import wait_for_input


from kamerad_schwungrad.MainBitch import MainBitch
import RPi.GPIO as GPIO
import time



GPIO_PIN = 3
GPIO_ON = 1
GPIO_OFF = 0 if GPIO_ON == 1 else 1


def waitForLeverToBe(expectedState):
    while GPIO.input(GPIO_PIN) != expectedState:
        time.sleep(0.1)


print("DEMN: setting up GPIO pin for start lever")
GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIO_PIN, GPIO.IN)

# with daemon_context:
while True:
    print("DEMN: waiting for start lever ... ")
    waitForLeverToBe(GPIO_ON)

    print("DEMN: start lever detected")
    try:
        main_bitch = MainBitch()
        main_bitch.run_parcour()
    except:
        print("D3MN: The bitch crashed!")

    print("DEMN: waiting for lever to go to off state ... ")
    waitForLeverToBe(GPIO_OFF)