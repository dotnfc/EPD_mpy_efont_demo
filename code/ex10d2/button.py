"""
    User Button Input [.NFC 2023/12/18]
"""
import board, sys, time

try:
    from machine import Pin
except ImportError:
    from usdl2_pin import *

class Button(object):
    IDLE = const(0)
    SHORT_PRESS_DETECT = const(1)
    LONG_PRESS_DETECT = const(2)
    WAIT_FOR_RELEASE = const(3)

    SHORT_PRESS_START = const(80)
    SHORT_PRESS_LIMIT = const(200)
    LONG_PRESS_START = const(2000)

    def __init__(self, pin, action_id = 0):
        self.pin = pin
        self.action_id = action_id   # caller provideded action identifier
        self.action_cb = None # action_callback(action_id, is_long_press)
        self.current_state = self.IDLE
        
    def is_pressed(self) -> bool:
        return self.pin.value() == 0

    def set_callback(self, callback=None):
        self.action_cb = callback
        
    def on_short_press(self):
        if self.action_cb is not None:
            self.action_cb(self.action_id, False)

    def on_long_press(self):
        if self.action_cb is not None:
            self.action_cb(self.action_id, True)
            
    def update_state(self):
        button_state = self.pin.value()
        if self.current_state == self.IDLE:
            if button_state == 0:
                self.button_down_time = time.ticks_ms()
                self.current_state = self.SHORT_PRESS_DETECT
        elif self.current_state == self.SHORT_PRESS_DETECT:
            if button_state == 1:
                # released
                button_press_duration = time.ticks_ms() - self.button_down_time
                if button_press_duration >= self.SHORT_PRESS_START:
                    self.on_short_press()
                    self.current_state = self.IDLE
            else:
                # hold
                button_press_duration = time.ticks_ms() - self.button_down_time
                if button_press_duration >= self.SHORT_PRESS_LIMIT:
                    self.current_state = self.LONG_PRESS_DETECT
        elif self.current_state == self.LONG_PRESS_DETECT:
            if button_state == 1:
                # released
                self.current_state = self.IDLE
            else:
                # hold
                button_press_duration = time.ticks_ms() - self.button_down_time
                if button_press_duration >= self.LONG_PRESS_START:
                    self.on_long_press()
                    self.current_state = self.WAIT_FOR_RELEASE
        elif self.current_state == self.WAIT_FOR_RELEASE:
            if button_state == 1:
                # released
                self.current_state = self.IDLE
        else:
            self.current_state = self.IDLE
            
if sys.platform == 'linux':
    KeyA = Button(Pin(SDL_SCANCODE_W), 1)
    KeyB = Button(Pin(SDL_SCANCODE_S), 2)
else:
    KeyA = Button(board.KEY_USER, 1)
    KeyB = Button(board.KEY_IO0, 2)