
"""
This is the Main class that gets started
It handles the complete Process of driving on the parcours.
Most of the things are delegated to subcomponents but the
procedure of the parcours is handled here
"""
class MainBitch:
    def __init__(self):
        self._trafficLightDetector = None
        self._freedomInterface = None
        self._romanDetector = None
        self._romanDisplay = None

    """
    Drive the whole Parcours.
    """
    def runParcour(self):
        self.waitForTrafficLight()

    """
    Blocks until the traffic light is green.
    """
    def waitForTrafficLight(self):
        pass
