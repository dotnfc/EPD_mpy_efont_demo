'''
   Pin module for SDL2 simulator
   by .NFC
'''

from usdl2 import SDL_KeyRead

SDL_SCANCODE_A = const(4)   # KeyA
SDL_SCANCODE_D = const(7)   # KeyB
SDL_SCANCODE_F = const(9)
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
        self.id = id
        pass
        
    def on(self) -> None:
        """Set pin to "1" output level."""
        pass
    
    def off(self) -> None:
        """Set pin to "0" output level."""
        pass
    
    def value(self, x = None) -> int:
        if SDL_KeyRead(self.id):
            return 0
        else:
            return 1