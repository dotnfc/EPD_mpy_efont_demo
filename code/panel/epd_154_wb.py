#-*- coding:utf-8 -*-
# panel driver, 
# FPC Label: HINK-E0154A05-A2
# Panel    : GDEY0154D67 (200 x 200)
# IC       : SSD1681
# Product  : 
# by dotnfc, 2024/12/02
#----------------------------------------------------------------

from micropython import const
from machine import SPI, Pin
from time import sleep_ms
import time
from framebuf import *
from logger import *
from board import *
import ustruct

BUSY = const(1)  # 1=busy, 0=idle

class EPD(FrameBuffer):
    # Display resolution
    WIDTH  = const(200)
    HEIGHT = const(200)
    BUF_SIZE = const(WIDTH * HEIGHT // 4)
    
    def __init__(self):
        self.spi = SPI(1, baudrate=10000000, polarity=0, phase=0, sck=EPD_PIN_SCK, mosi=EPD_PIN_SDA)
        self.spi.init()
        
        self.cs = EPD_PIN_CS
        self.dc = EPD_PIN_DC
        self.rst = EPD_PIN_RST
        self.busy = EPD_PIN_BUSY
        
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        self.busy.init(self.busy.IN)
        
        self.black = 0x00
        self.white = 0xff
        
        self.width = self.WIDTH
        self.height = self.HEIGHT

        self.buffer = bytearray(self.height * self.width // 8)        
        super().__init__(self.buffer, self.WIDTH, self.HEIGHT, MONO_HLSB)
       
    def _command(self, command, data=None):

        self.dc(0)
        self.cs(0)
        if isinstance(command, int):
            command = bytearray([command])
        self.spi.write(command)
        self.cs(1)
        if data is not None:
            if isinstance(data, int):
                data = bytearray([data])
            self._data(data)

    def _data(self, data):
        self.dc(1)
        self.cs(0)
        if isinstance(data, int):
            data = bytearray([data])
        self.spi.write(data)
        self.cs(1)

    def display(self, buf):
        pass

    def display_partial(self, buf):
        pass

    def refresh(self, buf = None, full=False):
        self._command(0x24)
        self._data(self.buffer)

        self._command(0x22) # Display Update Control
        self._data(0xF7);   
        self._command(0x20) # Activate Display Update Sequence
        self.wait_until_idle() 
    
    def clear_screen(self):
        self.fill(self.white)
        self._command(0x24)
        self._data(self.buffer)

        self._command(0x22) # Display Update Control
        self._data(0xF7);   
        self._command(0x20) # Activate Display Update Sequence
        self.wait_until_idle() 

    def power_on(self):
        self.wait_until_idle()
        
    def power_off(self):
        self.wait_until_idle()
    
    def init(self):
        self.reset()

        self.wait_until_idle()
        self._command(0x12)  # SWRESET

        self.wait_until_idle()
        self._command(0x01)  # Driver output control
        self._data(0xC7)
        self._data(0x00)
        self._data(0x00) # //1 = Show mirror 

        self._command(0x11)  # data entry mode
        self._data(0x01)

        self._command(0x44)  # set Ram-X address start/end position
        self._data(0x00)
        self._data(0x18)  # 0x0C-->(18+1)*8=200

        self._command(0x45)  # set Ram-Y address start/end position
        self._data(0xC7)  # 0xC7-->(199+1)=200
        self._data(0x00)
        self._data(0x00)
        self._data(0x00)

        self._command(0x3C)  # BorderWavefrom
        self._data(0x05)

        self._command(0x18)  # Read built-in temperature sensor
        self._data(0x80)

        self._command(0x4E)  # set RAM x address count to 0
        self._data(0x00)
        self._command(0x4F)  # set RAM y address count to 0X199
        self._data(0xC7)
        self._data(0x00)
        self.wait_until_idle()

    def wait_until_idle(self, timeout=10000):
        while self.busy.value() == BUSY:
            sleep_ms(10)
            timeout = timeout - 10
            if timeout <=0 :
                raise RuntimeError("Timeout out for waiting busy signal")
        
        sleep_ms(2)

    def reset(self):
        '''reset panel'''
        self.rst(0)
        sleep_ms(12)

        self.rst(1)
        sleep_ms(12)
        
    def sleep(self):
        self._command(0x10); # enter deep sleep
        self._data(0x01); 
    
def main():
    BLACK = 0
    RED = 1
    WHITE = 3
    
    epd = EPD()
    
    _start = time.ticks_ms()
    epd.init()
    _stop = time.ticks_ms()
    print("init used: %d ms" % (_stop - _start))

    _start = time.ticks_ms()
    epd.clear_screen()
    _stop = time.ticks_ms()
    print("clear used: %d ms" % (_stop - _start))
    
    epd.fill(WHITE)
    epd.text('Hello world!', 10, 60, BLACK)
    epd.line(0, 10, 180, 10, BLACK)
    
    _start = time.ticks_ms()
    epd.refresh()
    _stop = time.ticks_ms()
    print("time used: %d ms" % (_stop - _start))
    
    epd.sleep()

if __name__ == "__main__":
    main()


