from serial import Serial
from threading import Thread


"""
Methods for interacting with the Freedom Board
Note: be sure to call reset when the parcour is finished
because the startSignal
"""
class FreedomInterface:
    ACKNOWLEDGE = b'\x20'
    ERROR = b'\x10'
    START = b'\x80'
    ROMAN_NUMERAL_REQUEST = b'\x40'
    CURVE = b'\x08'

    """
    Initiate the Freedom Interface by opening the Serial-Port
    9600 baudrate 8 bits for a byte
    even parity
    1 stop bit
    """
    def __init__(self):
        self._serial = Serial('/dev/ttyS0', 9600, bytesize=EIGHTBITS, parity=PARITY_EVEN, stopbits=STOPBITS_ONE, timeout=1)
        self.thread = None
        self.last_async_command = None

    """
    Receive an Acknowledge from the Freedom Board
    """
    def _get_acknowledge(self):
        x = self._serial.read()
        if x == FreedomInterface.ERROR:
            return False
        if x == FreedomInterface.ACKNOWLEDGE:
            return True
        else:
            return None # garbage was sent

    """
    This method is called in a thread by self.wait_for_command
    it waits for a single command from the Freedom Board
    """
    def _wait_for_single_command(self):
        # temporalily remove timeout so the thread blocks until something
        # is received
        self._serial.timeout = None
        self.last_async_command = self._serial.read()
        self._serial.timeout = 1

    """
    Send an acknowledge to the Freedom Board.
    This should only used after the raspi received
    a curve command.

    """
    def send_acknowledge(self):
        self._serial.write(FreedomInterface.ACKNOWLEDGE)

    """
    Send an error to the Freedom Board.
    Should be used if an invalid command is received.
    """
    def send_error(self):
        self._serial.write(FreedomInterface.ERROR)

    """
    Send a start signal to the Freedom Board.
    This should happen after the Traffic Light was green
    """
    def send_start_signal(self):
        self._serial.write(FreedomInterface.START)
        return self._get_acknowledge()

    """
    Send the roman numeral to the Freedom Board.
    """
    def send_roman_numeral(self, roman_numeral):
        data_to_send = roman_numeral.to_bytes(1, byteorder='little')
        self._serial.write(data_to_send)

    """
    After the start signal was sent the Raspi should call
    this method to start waiting for a *single* command. This is done asynchronously.
    You should check if the roman_numeral_requested, curve_signaled, invalid_command_received
    methods whether a command has been received. After a command has been receieved
    call this method again to await more commands
    """
    def wait_for_command(self):
        self.last_async_command = None
        self.thread = Thread(target=self._wait_for_single_command, args(self))
        self.thread.start()

    """
    Call only after wait_for_command has been called once.
    Check if the Freedom Board requested the roman numeral
    """
    def roman_numeral_requested(self):
        return self.last_async_command == FreedomInterface.ROMAN_NUMERAL_REQUEST

    """
    Call only after wait_for_command has been called once.
    Check if the Freedom Board signaled that the curve has happend. The camera should be swapped in this case.
    (From Left to right)
    """
    def curve_signaled(self):
        return self.last_async_command == FreedomInterface.CURVE

    """
    Call only after wait_for_command has been called once.
    Check if the Freedom Board has sent an invalid command.
    """
    def invalid_command_received(self):
        return (not self.no_command_received()) and (not self.curve_signaled()) and (not self.roman_numeral_requested())

    """
    Call only after wait_for_command has been called once.
    Check if no command has been received yet (This means the background Thread still waits for a command)
    """
    def no_command_received(self):
        return self.last_async_command is None


