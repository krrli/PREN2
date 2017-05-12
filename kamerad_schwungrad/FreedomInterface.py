import serial
import binascii


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
    PAUSE = b'\xC0'
    RESUME = b'\x60'

    """
    Initiate the Freedom Interface by opening the Serial-Port
    9600 baudrate 8 bits for a byte
    even parity
    1 stop bit
    """
    def __init__(self, serialPortDevice):
        self._serial_port_device = serialPortDevice
        self._serial = None
        self.last_async_command = None

    def open_port(self):
        self._serial = serial.Serial(self._serial_port_device, 9600,
                                     bytesize=serial.EIGHTBITS,
                                     parity=serial.PARITY_NONE,
                                     stopbits=serial.STOPBITS_ONE,
                                     timeout=0)
        self._serial.nonblocking()
        self._serial.read_all()

    def close_port(self):
        self._serial.close()

    """
    Receive an Acknowledge from the Freedom Board
    """
    def _get_acknowledge(self):
        x = self._serial.read()
        if x == FreedomInterface.ERROR:
            print("WARN: Received ERROR from Freedom Board:", binascii.hexlify(x))
            return False
        if x == FreedomInterface.ACKNOWLEDGE:
            print("DEBUG: Received ACKNOWLEDGE from Freedom Board:", binascii.hexlify(x))
            return True
        else:
            print("WARN: Received Garbage from Freedom Board:", binascii.hexlify(x), x)
            return None # garbage was sent

    """
    This method is called in a thread by self.check_command_received
    it waits for a single command from the Freedom Board
    """
    def _wait_for_single_command(self):
        if self._serial_lock.acquire(False):
            try:
                # temporalily remove timeout so the thread blocks until something
                # is received
                self._serial.timeout = None
                self.last_async_command = None
                print("F3DM: waiting for async command")
                self.last_async_command = self._serial.read()
                print("F3DM: received async command from Freedom Board: ", self.last_async_command)
                self._serial.timeout = 1
            finally:
                self._serial_lock.release()

    """
    Send an acknowledge to the Freedom Board.
    This should only used after the raspi received
    a curve command.

    """
    def send_acknowledge(self):
        self._serial.write(FreedomInterface.ACKNOWLEDGE)
        self._serial.flush()

    """
    Send an error to the Freedom Board.
    Should be used if an invalid command is received.
    """
    def send_error(self):
        self._serial.write(FreedomInterface.ERROR)
        self._serial.flush()

    """
    Send a start signal to the Freedom Board.
    This should happen after the Traffic Light was green
    """
    def send_start_signal(self):
        self._serial.write(FreedomInterface.START)
        self._serial.flush()
        return self._get_acknowledge()

    """
     Send a stop signal to the Freedom Board.
     Send this signal if a picture has been taken and the roman numeral
     could be detected
    """
    def send_resume_signal(self):
        self._serial.write(FreedomInterface.RESUME)
        self._serial.flush()
        return self._get_acknowledge()

    """
     Send a stop signal to the Freedom Board.
     The raspi does this to stop to take a picture.
    """
    def send_stop_signal(self):
        self._serial.write(FreedomInterface.STOP)
        self._serial.flush()
        return self._get_acknowledge()

    """
    Send the roman numeral to the Freedom Board.
    """
    def send_roman_numeral(self, roman_numeral):
        data_to_send = roman_numeral.to_bytes(1, byteorder='little')
        self._serial.write(data_to_send)
        self._serial.flush()
        return self._get_acknowledge()

    """
    After the start signal was sent the Raspi should call
    This checks if a command has been received from the freedom board. This is done asynchronously.
    You should check if the roman_numeral_requested, curve_signaled, invalid_command_received
    methods whether a command has been received. After a command has been receieved
    call this method again to check for more commands.
    """
    def check_command_received(self):
        self.last_async_command = None
        if self._serial.in_waiting > 0:
            self.last_async_command = self._serial.read()
            print("F3DM: async command received", binascii.hexlify(self.last_async_command ), self.last_async_command)

    def clear_command(self):
        self.last_async_command = None

    """
    Call only after check_command_received has been called.
    Check if the Freedom Board requested the roman numeral
    """
    def roman_numeral_requested(self):
        return self.last_async_command == FreedomInterface.ROMAN_NUMERAL_REQUEST

    """
    Call only after check_command_received has been called.
    Check if the Freedom Board signaled that the curve has happend. The camera should be swapped in this case.
    (From Left to right)
    """
    def curve_signaled(self):
        return self.last_async_command == FreedomInterface.CURVE

    """
    Call only after check_command_received has been called.
    Check if the Freedom Board has sent an invalid command.
    """
    def invalid_command_received(self):
        return (not self.no_command_received()) and (not self.curve_signaled()) and (not self.roman_numeral_requested())

    """
    Call only after check_command_received has been called.
    Check if no command has been received yet.
    """
    def no_command_received(self):
        return self.last_async_command is None


