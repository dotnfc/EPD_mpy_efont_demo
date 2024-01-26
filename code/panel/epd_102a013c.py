#-*- coding:utf-8 -*-
# panel driver, based on GDEQ102Z90 (B/W/R) code
# FPC Label: HINK-E102A01-A1
# Panel    : GDEQ102Z90 (960 x 640)
# IC       : SSD1677
# Product  : Stellar-XXXL
# by dotnfc, 2023/09/20
#----------------------------------------------------------------

from micropython import const
from machine import SPI, Pin
from time import sleep_ms
import time
from framebuf import *
from logger import *
from board import *
import ustruct

# RAM Black(0) & White(1)
RBW_BLACK = const(0)
RBW_WHITE = const(1)

# RAM Red(1) & White(0)
RRW_RED = const(1)
RRW_WHITE = const(0)

BUSY = const(1)  # 1=busy, 0=idle

class EPD(FrameBuffer):
    # Display resolution
    WIDTH  = const(960)
    HEIGHT = const(640)
    BUF_SIZE = const(WIDTH * HEIGHT // 8)

    def __init__(self):
        self.spi = SPI(1, baudrate=15000000, polarity=0, phase=0, sck=EPD_PIN_SCK, mosi=EPD_PIN_SDA)
        self.spi.init()
        
        self.cs = EPD_PIN_CS
        self.dc = EPD_PIN_DC
        self.rst = EPD_PIN_RST
        self.busy = EPD_PIN_BUSY
        
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        self.busy.init(self.busy.IN)

        self.buf_bw = bytearray(self.BUF_SIZE)
        self.buf_rw = bytearray(self.BUF_SIZE)
        self.fb_rw = FrameBuffer(self.buf_rw, self.WIDTH, self.HEIGHT, MONO_HLSB)
        super().__init__(self.buf_bw, self.WIDTH, self.HEIGHT, MONO_HLSB)
        
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
    
    def init_3c(self):
        self._command(0x12)   # sw reset
        self.wait_until_idle(3000)
        
        self._command(0x0C)   # set booster strength
        self._data(0xAE)
        self._data(0xC7)
        self._data(0xC3)
        self._data(0xC0)
        self._data(0xC0)
        
        # setting gate number: A0~A9: Width-1, B0/B1/B2 = 0
        self._command(0x01, ustruct.pack("<HB", self.WIDTH - 1, 0x00))
        
        self._command(0x11)   # set data entry sequence
        self._data(0x03)

        # setting X direction start/end position of RAM: XSA = 0, XEA = WIDTH -1
        self._command(0x44, ustruct.pack('<HH', 0x0000, self.WIDTH -1))

        # setting Y direction start/end position of RAM: XSA = 0, XEA = HEIGHT -1
        self._command(0x45, ustruct.pack('<HH', 0x0000, self.HEIGHT -1))

        self._command(0x3C)   # set border 
        self._data(0x01)      # 03 - red, 01 - white
        
        self._command(0x18)   # set internal sensor on
        self._data(0x80)      # use internal sensor
                
        self._command(0x4E)
        self._data(0x00)
        self._data(0x00)
        self._command(0x4F)
        self._data(0x7F)
        self._data(0x02)
    
    def init(self):
        self.reset()
        self.init_3c()
    
    def refresh(self, buf = None, full=True):
        '''Update screen contents.
        
        Args:
            - buf: dummy, only internal buffer
            - full: dummy, only full more
        '''
        if not full:
            return

        self._command(0x24)     # Write RAM for black (0)/white (1)
        self._data(self.buf_bw)

        self._command(0x26)     # Write RAM for red (1)/ white (0)
        self._data(self.buf_rw)

        # Display Update Control
        self._command(0x22)
        self._data(0xF7)

        # Activate Display Update Sequence
        self._command(0x20)
        self.wait_until_idle(30000)
        
        # Enter deep sleep
        self._command(0x10)
        self._data(0x01)
  
    def wait_until_idle(self, timeout=10000):
        while self.busy.value() == BUSY:
            sleep_ms(10)
            timeout = timeout - 10
            if timeout <=0 :
                raise RuntimeError("Timeout out for waiting busy signal")
        
        sleep_ms(2)
       
    def reset(self):
        self.rst(1)
        sleep_ms(30)
        
        self.rst(0)
        sleep_ms(30)

        self.rst(1)
        sleep_ms(30)
        
    def sleep(self):
        self._command(0x10, 0x03) # Enter Deep Sleep Mode
        
def main():
    epd = EPD()
    
    _start = time.ticks_ms()
    epd.init()
    _stop = time.ticks_ms()
    print("init used: %d ms" % (_stop - _start))
    
    epd.fill(RBW_WHITE)
    epd.text('Hello world! i am black color', 10, 20, RBW_BLACK)
    epd.line(0, 10, 380, 10, RBW_BLACK)
    
    epd.fb_rw.text('Hello world! i am red color', 10, 120, RRW_RED)
    epd.fb_rw.line(0, 110, 380, 110, RRW_RED)
    
    epd.refresh()
    
if __name__ == "__main__":
    main()
