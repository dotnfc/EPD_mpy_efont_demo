#-*- coding:utf-8 -*-
# panel driver, based on {github}/mcauser/micropython-waveshare-epaper/epaper7in5b.py
# FPC Label: HINK-E075A01-A8
# Panel    : GDEW075Z09 (640 x 384)
# IC       : IL0371
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

BUSY = const(0)  # 0=busy, 1=idle

class EPD(FrameBuffer):
    # Display resolution
    WIDTH  = const(640)
    HEIGHT = const(384)
    BUF_SIZE = const(WIDTH * HEIGHT // 4)
    
    def __init__(self):
        self.spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=EPD_PIN_SCK, mosi=EPD_PIN_SDA)
        self.spi.init()
        
        self.cs = EPD_PIN_CS
        self.dc = EPD_PIN_DC
        self.rst = EPD_PIN_RST
        self.busy = EPD_PIN_BUSY
        
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        self.busy.init(self.busy.IN)
        
        self.width = self.WIDTH
        self.height = self.HEIGHT

        self.buf = bytearray(self.BUF_SIZE)
        super().__init__(self.buf, self.WIDTH, self.HEIGHT, GS2_HMSB)
       
    def _command(self, command, data=None):
        self.cs(1) # according to LOLIN_EPD
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
        self.cs(1) # according to LOLIN_EPD
        self.dc(1)
        self.cs(0)
        if isinstance(data, int):
            data = bytearray([data])
        self.spi.write(data)
        self.cs(1)
            
    def power_on(self):
        self._command(0x04)
        self.wait_until_idle()
        
    def power_off(self):
        self._command(0x02)
        self.wait_until_idle()
    
    def refresh(self, buf = None, full=True):
        '''Update screen contents.
        
        Args:
            - buf: dummy, only internal buffer
            - full: dummy, only full more
        '''
        if not full:
            return
        
        self._command(0x10)
        data = []
        ba_ref = self.buf
        for i in range(0, self.BUF_SIZE):
            temp1 = ba_ref[i] # bit-order: GS2_HMSB
            # temp1 = self.msb_to_lsb(self.buf[i])
            j = 0
            while (j < 4):
                if ((temp1 & 0x03) == 0x03):
                    temp2 = 0x03
                elif ((temp1 & 0xC0) == 0x00):
                    temp2 = 0x00
                else:
                    temp2 = 0x04
                temp2 = (temp2 << 4) & 0xFF
                temp1 = (temp1 >> 2) & 0xFF
                j += 1
                if ((temp1 & 0x03) == 0x03):
                    temp2 |= 0x03
                elif ((temp1 & 0xC0) == 0x00):
                    temp2 |= 0x00
                else:
                    temp2 |= 0x04
                temp1 = (temp1 >> 2) & 0xFF
                data.append(temp2)
                j += 1
        
        self._data(bytearray(data))
        self._command(0x12)
        sleep_ms(100)
        self.wait_until_idle(45000)
        
    def init(self):
        self.init_full()
        
    def init_panel(self, reset=True):
        if reset:
            self.reset()

        #  release flash sleep
        self._command(0x65, b'\x01')     # FLASH CONTROL
        self._command(0xab)
        self._command(0x65, b'\x00')     # FLASH CONTROL
        
        self._command(0x01, b'\x37\x00') # POWER_SETTING
        self._command(0x00, b'\xcf\x08') # PANEL_SETTING
        self._command(0x06, b'\xC7\xCC\x28') # BOOSTER_SOFT_START
        self._command(0x04)              # POWER_ON
        self.wait_until_idle()
        self._command(0x30, b'\x3C')     # PLL_CONTROL
        self._command(0x41, b'\x00')
        self._command(0x50, b'\x77')
        self._command(0x60, b'\x22')
        self._command(0x61, ustruct.pack(">HH", self.WIDTH, self.HEIGHT))
        self._command(0x82, b'\x1E')     # decide by LUT file
        self._command(0xE5, b'\x03')     # FLASH MODE
        
    def init_full(self):
        self.init_panel()
        self.power_on()
        
    def init_partial(self):
        self.init_panel()
        self.power_on()
        
    def update_full(self):
        self._command(0x12)
        self.wait_until_idle(45000)

    def update_partial(self):
        self._command(0x12)
        self.wait_until_idle(45000)
        
    def wait_until_idle(self, timeout=200):
            while self.busy.value() == BUSY:
                sleep_ms(100)
                timeout = timeout - 100
                if timeout <=0 :
                    raise RuntimeError("Timeout out for waiting busy signal")
       
    def reset(self):
        self.rst(0)
        sleep_ms(200)

        self.rst(1)
        sleep_ms(200)
        
    def sleep(self):
        self.power_off()        
        self._command(0x07, 0xa5)
        
def main():
    BLACK = 0
    RED = 1
    WHITE = 3
    
    epd = EPD()
    epd.init()
    epd.fill(WHITE)
    epd.text('Hello world', 10, 60, BLACK)
    epd.line(0, 10, 380, 10, BLACK)
    
    _start = time.ticks_ms()
    epd.refresh()
    _stop = time.ticks_ms()
    print("time used: %d ms" % (_stop - _start))
    
    epd.sleep()
    
    pass

if __name__ == "__main__":
    main()
