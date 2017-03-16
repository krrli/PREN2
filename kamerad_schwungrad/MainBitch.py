
from kamerad_schwungrad.FreedomInterface import FreedomInterface
import random

"""
This is the Main class that gets started
It handles the complete Process of driving on the parcours.
Most of the things are delegated to subcomponents but the
procedure of the parcours is handled here
"""


class MainBitch:
    def __init__(self):
        self._trafficLightDetector = None
        self._freedomInterface = FreedomInterface()
        self._romanDetector = None
        self._romanDisplay = None

    """
    Drive the whole Parcours.
    """
    def run_parcour(self):
        self.waitForTrafficLight()
        self._freedomInterface.send_start_signal()
        while True:
            self.handle_freedom_interface()

    """
    Handles the communication with the Freedom Board
    """
    def handle_freedom_interface(self):
        if not self._freedomInterface.no_command_received():
            self._freedomInterface.wait_for_command()

        if self._freedomInterface.roman_numeral_requested():
            # TODO: replace this with actual roman numeral
            self._freedomInterface.send_roman_numeral(random.randint(1,5))

        if self._freedomInterface.curve_signaled():
            self._freedomInterface.send_acknowledge()

        if self._freedomInterface.invalid_command_received():
            self._freedomInterface.send_error()

    """
    Blocks until the traffic light is green.
    """
    def wait_for_traffic_light(self):
        pass
