"""
    User Button Input [.NFC 2023/12/18]
"""
import board, sys

try:
    from machine import Pin
except ImportError:
    from usdl2_pin import *

class Button(object):
    def __init__(self, pin):
        self.pin = pin
        
    def is_pressed(self) -> bool:
        return self.pin.value() == 0
    
    def is_holding(self) -> bool:
        return False

if sys.platform == 'linux':
    KeyA = Button(Pin(SDL_SCANCODE_A))
    KeyB = Button(Pin(SDL_SCANCODE_D))
else:
    KeyA = Button(board.KEY_USER)
    KeyB = Button(board.KEY_IO0)