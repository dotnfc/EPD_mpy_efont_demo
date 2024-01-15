'''
   Pin module for SDL2 simulator
   by .NFC
'''

from usdl2 import SDL_KeyRead

SDL_SCANCODE_A = const(4)   # KeyA
SDL_SCANCODE_D = const(7)   # KeyB
SDL_SCANCODE_W = const(26)
SDL_SCANCODE_S = const(22)

class Pin(object):
    IN = 1
    OUT = 2
    OPEN_DRAIN = 4
    PULL_DOWN = 1
    PULL_UP = 2
    
    IRQ_RISING = 1
    IRQ_FALLING = 2
    WAKE_LOW = 4
    WAKE_HIGH = 5    
    
    DRIVE_0 = 0
    DRIVE_1 = 1
    DRIVE_2 = 2
    DRIVE_3 = 3
    def __init__(self, id, mode=-1, pull=-1, *, value=None, drive=0, alt=-1):
        self._id = id
        self._value = 0
    
    def init(self, mode=-1, pull=-1, *, value=None, drive=0, alt=-1) -> None:
        """
        Re-initialise the pin using the given parameters.  Only those arguments that
        are specified will be set.  The rest of the pin peripheral state will remain
        unchanged.  See the constructor documentation for details of the arguments.

        Returns ``None``.
        """
        ...

    def on(self) -> None:
        """Set pin to "1" output level."""
        pass
    
    def off(self) -> None:
        """Set pin to "0" output level."""
        pass
    
    def __call__(self, value=None):
        if value is not None:
            self.set_state(value)
        else:
            return self.get_state()

    def set_state(self, value):
        if value in (0, 1):
            self._value = value
        else:
            raise ValueError("Value must be 0 or 1")

    def get_state(self):
        return self._value

    def value(self, x = None) -> int:
        if SDL_KeyRead(self._id):
            return 0
        else:
            return 1